#!/usr/bin/env python3
"""Helper script — spawn a sub-Agent via Claude Code CLI with streaming log.

Usage:
    spawn.py <role> <workspace> <prompt_file> <task_file> [--tools ...] [--timeout N] [--resume]

特性：
- **代码级阶段快照**：每次派活前、产出结果后自动 `git add -A && git commit`
  （任务文件、.state、Agent 产出全部入库，不依赖 Orchestrator 自觉）。
  并行 pipeline 会同时跑多个 spawn.py，用 flock 互斥。
- **断点续传**：每个子 Agent 的 session_id 记录在 `debug/` 的 `.session` 文件；
  带 `--resume` 时续接上次会话（用于超时/中断后重派），不带则全新开始（失败重做）。
- **运行时文件隔离**：`.log/.result/.metrics/.session/.progress` 在 `debug/`。
  新版 run.py 启动的会话设置 `SPAWN_RUNTIME_BY_TASK=1`，运行时文件按
  (Role, 任务名) 隔离为 `.{Role}_{任务名}.*` —— 同角色并行派活互不覆盖
  （旧方案按角色命名，靠禁止同角色并行回避冲突）；未设置该环境变量时
  退回按角色的 `.{Role}.*` 命名（过渡期兼容）。
- **自动心跳**：泵流时把 sub-Agent 的每个工具调用覆写进 `.progress`
  （Agent 自己写 k/N 进度时让位）——进度播报不再依赖模型自觉。
- **Workspace 布局**：任务文件在 `tasks/`（向后兼容：根目录的任务文件也能找到）。
"""

import sys, os, re, json, fcntl, signal, subprocess, threading, time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPTS_DIR.parent.resolve()
sys.path.insert(0, str(SCRIPTS_DIR))
import load_env  # noqa: F401 — 自动载入 .env（setup.sh 写入的 API 配置）
from stream_parser import parse_stream_event

CONFIG = json.loads((PROJECT_ROOT / "config.json").read_text(encoding="utf-8"))
# model / agent_models / timeout 都在 configs.<pipeline> 下，不在顶层。
# run.py 通过 SOLVER_PIPELINE 环境变量把 --pipeline 覆盖传过来，
# 保证 sub-agent 的模型/超时与 Orchestrator 用的是同一份配置。
PIPELINE = os.environ.get("SOLVER_PIPELINE") or CONFIG.get("pipeline", "standard")
PIPELINE_CONFIG = CONFIG.get("configs", {}).get(PIPELINE, {})
DEFAULT_MODEL = PIPELINE_CONFIG.get("model", CONFIG.get("model", "qwen3.6-plus"))
AGENT_MODELS = PIPELINE_CONFIG.get("agent_models", {})
TIMEOUT = PIPELINE_CONFIG.get("timeout_seconds", CONFIG.get("timeout_seconds", 600))

DEBUG_DIR = "debug"
TASKS_DIR = "tasks"

# 分支/路线 → 颜色：并行多路线时按任务键稳定着色，多路同跑一眼可辨。
# 索引用稳定的字符串哈希（内建 hash 每进程随机，跨进程会串色）。
BRANCH_COLORS = ["36", "33", "35", "32", "34", "31"]

ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def branch_color(key):
    h = 0
    for ch in key:
        h = (h * 31 + ord(ch)) % 1000000007
    return BRANCH_COLORS[h % len(BRANCH_COLORS)]


# 家务命令（读文件/状态查询/文件系统操作/shell 控制结构）——不上屏
HOUSEKEEPING_RE = re.compile(
    r"^(ls|cat|head|tail|wc|grep|find|echo|printf|pwd|git|sleep|cd|rm|mkdir|"
    r"mv|cp|touch|chmod|for|while|until|if|then|else|fi|do|done|wait|true"
    r"|seq|test|kill|ps|diff|sort|uniq|tr|cut|sed|awk|xargs|tee|date"
    r"|export|set|read|basename|dirname|realpath|stat|file|md5sum|sha256sum"
    r"|tar|zip|unzip)\b")

# 命令前缀包装器（timeout 120 python3 x.py 是 Agent 跑脚本的常态）——
# 分类前先剥掉，否则 "timeout" 会被误当成可执行文件上报
WRAPPER_RE = re.compile(
    r"^(?:sudo\s+)?(?:timeout\s+\S+|time|nohup|nice(?:\s+-n\s+\S+)?"
    r"|stdbuf\s+\S+|env(?:\s+\w+=\S+)*)\s+")


def _strip_wrappers(seg):
    while True:
        s = WRAPPER_RE.sub("", seg, count=1)
        if s == seg:
            return s
        seg = s


def describe_bash(cmd):
    """Bash 命令 → 人类可读的文字描述。返回 None 表示该命令不上屏（家务命令）。

    在 && / || / ; 链上**从后往前**找第一个非家务段作为主动作（链尾常是
    echo DONE 之类家务）；主动作段先剥掉 timeout/nohup/env 等前缀包装器
    再分类。脚本执行统一为 "script 执行：<描述>" 模板（与"失败：…"等
    全角冒号行文一致）：
    "timeout 120 python3 x.py" → script 执行：x.py；
    "python3 x.py && echo DONE" → script 执行：x.py；
    "for i in ...; do sleep 15; done" → 全段家务 → None。
    无法翻译的杂项命令不上屏（宁缺毋滥）。
    """
    if not cmd or not cmd.strip():
        return None
    if re.match(r"^\s*[\[\(!]", cmd):   # 条件测试/子 shell 开头的控制结构
        return None
    segs = re.split(r"\s*(?:&&|\|\||;)\s*", cmd.strip())
    last = ""
    for seg in reversed(segs):
        seg = _strip_wrappers(seg.strip())
        if seg and not HOUSEKEEPING_RE.match(seg) and not re.match(r"^[\[\(!]", seg):
            last = seg
            break
    if not last:
        return None
    m = re.match(r"(?:[A-Za-z_][\w/.-]*/)?python3?\s+(\S+)", last)
    if m:
        arg = m.group(1)
        if arg.startswith("-"):          # python3 -c / python3 -
            return "script 执行：内联 Python"
        script = os.path.basename(arg)
        if "query_rag" in script:
            return "script 执行：查询知识库"
        return f"script 执行：{script}"
    words = last.split()
    if words and words[0] in ("bash", "sh", "source") and len(words) > 1:
        return f"script 执行：{os.path.basename(words[1])}"
    head = words[0] if words else ""
    if re.fullmatch(r"[\w./-]+", head):
        return f"script 执行：{os.path.basename(head)}"
    return None


def heartbeat_text(summary):
    """.progress 心跳文字：与上屏行同一套文字化规则，不把原始命令泄漏进
    进度播报（监督者 ticker 与状态栏会原样引用它）。"""
    if summary.startswith("Bash: "):
        cmd = summary[6:].splitlines()[0][:150] if summary[6:] else ""
        return describe_bash(cmd) or "执行命令"
    if summary.startswith(("Write: ", "Edit: ")):
        base = os.path.basename(summary.split(": ", 1)[1])
        return f"写脚本 {base}" if base.endswith(".py") else f"写 {base}"
    return summary


def append_console(feed, text):
    """把一行（去色后）追加进工作区可见的 console.log（用户随时可看）。"""
    path = feed.get("console_file") if feed else None
    if not path or not text:
        return
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%m-%d %H:%M:%S')}] "
                    f"{ANSI_RE.sub('', text)}\n")
    except OSError:
        pass


def agent_event_line(role, branch, summary, workspace_abs=""):
    """把 sub-Agent 的一个工具调用渲染成控制台行（带路线颜色）。

    返回 "" 表示不上屏（读文件、家务命令、workspace 内写文档——
    脚本创建除外，它单独以"写脚本 …"上屏）。
    """
    text = ""
    if summary.startswith("Bash: "):
        cmd = summary[6:].splitlines()[0][:150] if summary[6:] else ""
        desc = describe_bash(cmd)
        if desc is None:
            return ""
        text = desc
    elif summary.startswith(("Write: ", "Edit: ")):
        path = summary.split(": ", 1)[1]
        base = os.path.basename(path)
        if base.endswith(".py"):
            text = f"写脚本 {base}"
        elif workspace_abs and path.startswith(workspace_abs):
            return ""   # workspace 内的 md/进度文件等：不上屏（结论看产出即可）
        else:
            text = summary[:100]
    else:
        return ""
    color = branch_color(branch or role)
    return f"\033[1;{color}m[{role}·{branch}]\033[0m {text}"

# Per-agent permission profiles
# Format: Claude Code --allowed-tools values
# Bash(pattern) restricts Bash to commands matching the pattern
_STANDARD_PROFILE = (
    "Read,"
    "Write,"
    "Edit,"
    "Bash(python3 *),"
    "Bash(source * && python3 *),"
    "Bash(git status*),"
    "Bash(git diff*),"
    "Bash(git log*),"
    "Bash(git add *)"
)
AGENT_PROFILES = {
    "Planner": _STANDARD_PROFILE,
    "Builder": _STANDARD_PROFILE,
    "Evaluator": _STANDARD_PROFILE,
    "Verifier": _STANDARD_PROFILE,
    # 非 adaptive pipeline 的角色（角色名须与 config.json 的 agent_models 键一致）
    "Explorer": _STANDARD_PROFILE,
    "Meta-Planner": _STANDARD_PROFILE,
    "Theorist": _STANDARD_PROFILE,
    "Computationalist": _STANDARD_PROFILE,
    "Experimentalist": _STANDARD_PROFILE,
    "Critic": _STANDARD_PROFILE,
    "Secretary": _STANDARD_PROFILE,
    "Assessor": _STANDARD_PROFILE,
}


def kill_process_group(proc):
    """杀掉子进程及其整个进程组（包括它派生的后台孤儿进程）。"""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        try:
            proc.kill()
        except ProcessLookupError:
            pass
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        pass


def _read_pipeline_name(workspace):
    """从 .state（优先 debug/.state）读 pipeline 名，用于提交消息前缀。"""
    for rel in (os.path.join(DEBUG_DIR, ".state"), ".state"):
        try:
            with open(os.path.join(workspace, rel), encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("pipeline:"):
                        return line.split(":", 1)[1].strip()
        except OSError:
            continue
    return ""


def git_snapshot(workspace, message):
    """代码级阶段快照：提交 workspace 当前全部变更（任何失败都不阻断派活）。

    派活前调用一次（归档 Orchestrator 写的任务文件/.state），
    产出结果后再调用一次（归档 Agent 产出）。
    并行 pipeline 的多个 spawn.py 并发时用 flock 互斥。
    """
    w = os.path.abspath(workspace)
    if not os.path.isdir(os.path.join(w, ".git")):
        return
    os.makedirs(os.path.join(w, DEBUG_DIR), exist_ok=True)
    lock_path = os.path.join(w, DEBUG_DIR, ".gitlock")
    pipeline = _read_pipeline_name(w)
    msg = f"{pipeline}: {message}" if pipeline else message
    try:
        with open(lock_path, "w") as lf:
            fcntl.flock(lf, fcntl.LOCK_EX)
            subprocess.run(["git", "-C", w, "add", "-A"], capture_output=True, timeout=120)
            r = subprocess.run(["git", "-C", w, "commit", "-m", msg],
                               capture_output=True, text=True, timeout=120)
            out = (r.stdout or "") + (r.stderr or "")
            if r.returncode != 0 and "nothing to commit" not in out:
                print(f"[spawn] git snapshot warning: {out.strip()[:200]}", file=sys.stderr)
    except Exception as e:
        print(f"[spawn] git snapshot warning: {e}", file=sys.stderr)


def write_failure_result(result_path, role, err):
    """spawn 层失败时写入失败标记，防止 Orchestrator 读到**上一次**成功运行的
    陈旧 .result（树类流水线里同一角色会被反复派活，陈旧汇报会误导路由）。

    用 BLOCKED 而非 FAIL：这是环境性失败（超时/无结果/进程错误），不是
    "路线走不通"——各流水线对 BLOCKED 的处理都是重试/跳过而非判死端。
    """
    try:
        with open(result_path, "w", encoding="utf-8") as f:
            f.write("HANDOFF\n"
                    "STATUS: BLOCKED\n"
                    "OUTPUT: -\n"
                    f"SUMMARY: spawn 层失败（非 {role} 本人汇报）：{err}。可重试或 --resume。\n"
                    f"ERROR: {err}\n")
    except OSError:
        pass


def resolve_task_file(workspace, task_file):
    """查找任务文件：优先 {workspace}/tasks/，再找根目录（兼容旧布局），最后当前目录。"""
    if os.path.isabs(task_file):
        return task_file
    candidates = [
        os.path.join(workspace, TASKS_DIR, f"{task_file}.md"),
        os.path.join(workspace, TASKS_DIR, task_file),
        os.path.join(workspace, f"{task_file}.md"),
        os.path.join(workspace, task_file),
        f"{task_file}.md",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return task_file


def task_key_of(task_file_abs):
    """任务键：任务文件基名去掉 .md，只保留文件名字符（运行时文件的隔离键）。"""
    base = os.path.basename(str(task_file_abs))
    base = re.sub(r"\.md$", "", base, flags=re.IGNORECASE)
    base = re.sub(r"[^A-Za-z0-9_-]", "_", base)
    return base or "task"


def runtime_paths(debug_dir, role, task_file_abs, keyed):
    """一次派活的运行时文件集合。

    keyed=True（新版 run.py 设置 SPAWN_RUNTIME_BY_TASK=1）：
      按 (Role, 任务名) 隔离 —— `.{Role}_{任务名}.log/.result/...`，
      同角色并行派活各写各的，互不覆盖。
    keyed=False（旧会话续传等过渡场景）：按角色命名 `.{Role}.*`。
    """
    stem = f".{role}_{task_key_of(task_file_abs)}" if keyed else f".{role}"
    return {name: os.path.join(debug_dir, stem + ext) for name, ext in (
        ("log", ".log"), ("result", ".result"), ("metrics", ".metrics"),
        ("session", ".session"), ("progress", ".progress"))}


def run_session(cmd, log_file, timeout_sec, env, cwd, progress_path=None, feed=None):
    """启动一次 claude 会话并泵送流式输出。

    返回 (result_event, session_id, error)：
    - 正常：(event, sid, None)
    - 超时：(None, sid|None, "timeout after Ns")
    - 其他异常：(None|event, sid|None, 错误描述)

    progress_path 非空时，把观察到的每个工具调用覆写进该文件作为心跳
    （进度播报由此保证，不再依赖 Agent 自觉）；一旦发现 Agent 自己在写
    进度文件（说明它遵守 k/N 进度协议），让位、停止覆写。
    feed 非空时（{role, branch, workspace_abs}），sub-Agent 的脚本创建与
    真正的计算命令直接上屏（带路线颜色）——监控关注的是 sub-Agent 层。
    """
    # start_new_session=True：子进程自成进程组，必要时可整组杀掉
    # （claude 常派生后台子进程；若有孤儿进程卡住，claude 本体不退出）。
    # stderr 直接写入日志文件而不用 PIPE，避免管道写满导致子进程阻塞。
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=log_file, text=True,
        cwd=cwd, env=env, start_new_session=True,
    )

    result_event = None
    session_id = None
    progress_name = os.path.basename(progress_path) if progress_path else None
    agent_writes_progress = [False]

    def pump_stdout():
        nonlocal result_event, session_id
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            etype, summary, event = parse_stream_event(line)
            if etype == "init" and event and event.get("session_id"):
                session_id = event["session_id"]
            if summary:
                log_file.write(f"[{etype}] {summary}\n")
                log_file.flush()
                if etype == "tool_use":
                    if feed:
                        line = agent_event_line(feed["role"], feed["branch"], summary,
                                                feed.get("workspace_abs", ""))
                        if line:
                            print(line, flush=True)
                            append_console(feed, line)
                    if progress_path:
                        if progress_name and progress_name in summary:
                            agent_writes_progress[0] = True
                        elif not agent_writes_progress[0]:
                            try:
                                with open(progress_path, "w", encoding="utf-8") as pf:
                                    pf.write(heartbeat_text(summary)[:50] + "\n")
                            except OSError:
                                pass
            if etype == "result" and event:
                result_event = event
                return  # 拿到结果即返回，不等 EOF（进程可能被孤儿子进程卡住而不退出）

    pump_thread = threading.Thread(target=pump_stdout, daemon=True)
    pump_thread.start()
    pump_thread.join(timeout=timeout_sec)

    if pump_thread.is_alive():
        log_file.write(f"[error] timeout after {timeout_sec}s, killing process group\n")
        log_file.flush()
        kill_process_group(proc)
        return None, session_id, f"timeout after {timeout_sec}s"

    # 已拿到结果：给进程一小段宽限期自行退出；
    # 若它因等待孤儿后台进程而不退出，直接杀掉整个进程组。
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        log_file.write("[warn] 产出结果后 15s 未退出，杀掉进程组以继续\n")
        log_file.flush()
        kill_process_group(proc)

    if not result_event:
        log_file.write("[error] no result event received\n")
        log_file.flush()
        return None, session_id, "no result event"

    if result_event.get("is_error"):
        err_msg = result_event.get("result", "Unknown")[:300]
        log_file.write(f"[error] {err_msg}\n")
        log_file.flush()
        return result_event, session_id, err_msg

    return result_event, session_id, None


def main():
    args = sys.argv[1:]
    positional = [a for a in args if not a.startswith("--")]
    flags = set(a for a in args if a.startswith("--"))
    if len(positional) < 4:
        print("Usage: spawn.py <role> <workspace> <prompt_file> <task_file> "
              "[--tools Read,Write,Edit,Bash] [--timeout N] [--resume]")
        sys.exit(1)

    role, workspace, prompt_file, task_file = positional[:4]
    resume_flag = "--resume" in flags

    # --timeout N 覆盖默认超时（临时 Agent 用）
    timeout = TIMEOUT
    for i, a in enumerate(args):
        if a == "--timeout" and i + 1 < len(args):
            try:
                timeout = int(args[i + 1])
            except ValueError:
                pass

    # 带数字后缀的角色（如 Planner_1）回退到基础角色（Planner）的配置
    base_role = role
    parts = role.rsplit("_", 1)
    if len(parts) == 2 and parts[1].isdigit():
        base_role = parts[0]

    # Select model for this agent (agent-specific > base role > default)
    model = AGENT_MODELS.get(role, AGENT_MODELS.get(base_role, DEFAULT_MODEL))

    # Determine allowed tools: CLI override > profile > generic default
    allowed_tools = "Read,Write,Edit,Bash"  # fallback default
    if role in AGENT_PROFILES:
        allowed_tools = AGENT_PROFILES[role]
    elif base_role in AGENT_PROFILES:
        allowed_tools = AGENT_PROFILES[base_role]
    for i, arg in enumerate(args):
        if arg == "--tools" and i + 1 < len(args):
            allowed_tools = args[i + 1]

    prompt_file_abs = str(PROJECT_ROOT / "prompts" / f"{prompt_file}.md")
    task_file_abs = resolve_task_file(workspace, task_file)

    workspace_abs = os.path.abspath(workspace) if workspace else ""
    debug_dir = os.path.join(workspace_abs, DEBUG_DIR)
    if workspace:
        os.makedirs(debug_dir, exist_ok=True)

    # 即时失败回执：角色 prompt / 任务文件缺失时立刻写 BLOCKED .result。
    # 后台派活（命令带 &）的 stderr 会被 shell 吞掉，Orchestrator 只认
    # .result——没有回执它会空转满整个轮询周期（I510 实测烧过 9.5 分钟）。
    # 注意这发生在清理旧 .result 之前：回执直接覆盖陈旧汇报，语义正确。
    missing = []
    if not os.path.isfile(prompt_file_abs):
        missing.append(f"角色 prompt 不存在：{prompt_file_abs}")
    if not os.path.isfile(task_file_abs):
        missing.append(f"任务文件不存在：{task_file_abs}（先写任务文件再派活）")
    if missing:
        err = "；".join(missing)
        print(f"[spawn:{role}] error: {err}", file=sys.stderr)
        if workspace:
            early = runtime_paths(debug_dir, role, task_file_abs,
                                  bool(os.environ.get("SPAWN_RUNTIME_BY_TASK")))
            write_failure_result(early["result"], role, err)
            append_console({"console_file": os.path.join(workspace_abs, "console.log")},
                           f"[{role}·{task_key_of(task_file_abs)}] 失败：{err}")
            git_snapshot(workspace, f"{role} missing files ({os.path.basename(task_file_abs)})")
        sys.exit(1)

    system_prompt = open(prompt_file_abs, encoding="utf-8").read()
    # 模板变量：{project_root} 永远替换（移植性）；{workspace} 用绝对路径
    # 替换（下面会把 cwd 改成 workspace）；{task} 用任务键替换
    # （供 agent prompt 里的按派活隔离路径使用，如进度文件名）。
    system_prompt = system_prompt.replace("{project_root}", str(PROJECT_ROOT))
    if workspace:
        system_prompt = system_prompt.replace("{workspace}", workspace_abs)
    system_prompt = system_prompt.replace("{task}", task_key_of(task_file_abs))
    task = open(task_file_abs, encoding="utf-8").read()
    if workspace:
        task += (f"\n\n**重要：** 所有文件操作必须在 `{workspace_abs}` 目录内进行，不要在项目根目录创建文件。"
                 "长时间运行的命令（脚本执行、计算）一律**前台同步**运行，不要加 `&` 放后台——"
                 "后台任务的输出文件在工作区之外，会被路径守卫拦截，读不到就只能重跑一遍。")

    # 断点续传提示词（--resume 时用；原任务已在会话历史里，不重发）
    resume_prompt = (
        "这是断点续传：你上次的会话被中断，现在继续。\n"
        "1. 先用 ls / 读文件快速盘点你已完成的部分；\n"
        "2. 从中断处继续，完成原任务（原任务内容见上方会话历史）；\n"
        "3. 完成后按原要求输出 HANDOFF。"
    )

    agents_json = json.dumps({role: {"description": f"{role} Agent", "prompt": system_prompt}})

    base_cmd = [
        "claude",
        "--print",
        "--output-format", "stream-json",
        "--verbose",
        "--permission-mode", "bypassPermissions",
        "--agents", agents_json,
        "--agent", role,
        "--allowed-tools", allowed_tools,
        "--add-dir", workspace_abs or workspace,
        "--model", model,
    ]
    cmd_fresh = base_cmd + [task]

    # 运行时文件（全部在 debug/ 下）。新版 run.py 设置 SPAWN_RUNTIME_BY_TASK=1
    # 时按 (Role, 任务名) 隔离——同角色并行派活各写各的，互不覆盖；
    # 未设置（旧会话续传的过渡期）退回按角色命名。
    task_keyed = bool(os.environ.get("SPAWN_RUNTIME_BY_TASK"))
    paths = runtime_paths(debug_dir, role, task_file_abs, task_keyed)
    log_path = paths["log"]
    result_path = paths["result"]
    metrics_path = paths["metrics"]
    session_path = paths["session"]
    progress_path = paths["progress"]

    # 清理过期进度文件（进度是瞬态监控信息，不是审计记录，可删）。
    # 旧命名有大小写两套（prompt 让 Agent 写小写 .{role}.progress），都要清。
    stale_progress = [progress_path]
    if not task_keyed:
        stale_progress.append(os.path.join(debug_dir, f".{role.lower()}.progress"))
    for p in stale_progress:
        try:
            os.remove(p)
        except OSError:
            pass

    # 清理上一次派活遗留的 .result/.metrics：Orchestrator 的轮询等待与断点续传
    # 以「.result 存在」作为「本次派活已完成」的信号，陈旧汇报会造成误判完成。
    # （.log/.session 保留：追加式审计记录与续传凭据。）
    for stale in (result_path, metrics_path):
        try:
            os.remove(stale)
        except OSError:
            pass

    # 设置环境变量：WORKSPACE 激活 path_guard hook（.claude/settings.json 由
    # run.py 写入工作区）；不再用 --bare —— 它会连同 hooks 一起跳过。
    # auto-memory 由 memory_guard 运行期清空记忆目录来阻断。
    env = os.environ.copy()
    env["WORKSPACE"] = os.path.abspath(workspace)
    env["WORKSPACE_ROLE"] = "agent"
    cwd = workspace if os.path.isdir(workspace) else None

    # 派活前快照：归档 Orchestrator 刚写的任务文件 / .state
    git_snapshot(workspace, f"spawn {role} ({os.path.basename(task_file_abs)})")

    start_time = time.time()
    result_event = None
    session_id = None
    err = None
    feed = {"role": role, "branch": task_key_of(task_file_abs),
            "workspace_abs": workspace_abs,
            "console_file": os.path.join(workspace_abs, "console.log")
            if workspace_abs else ""}

    with open(log_path, "a", encoding="utf-8") as log_file:
        # --resume：若存在上次会话记录，先尝试续接；失败（非超时）则回退全新会话
        resume_sid = None
        if resume_flag:
            try:
                resume_sid = open(session_path, encoding="utf-8").read().strip() or None
            except OSError:
                resume_sid = None

        if resume_sid:
            log_file.write(f"\n===== [resume] {role} | task={task_file} | "
                           f"sid={resume_sid[:8]} | {time.strftime('%H:%M:%S')} =====\n")
            log_file.flush()
            result_event, session_id, err = run_session(
                base_cmd + ["--resume", resume_sid, resume_prompt],
                log_file, timeout, env, cwd, progress_path, feed)
            if err:
                if err.startswith("timeout"):
                    # 超时不重试（重开会话会丢失已完成进度，交由上层决策）
                    print(f"[spawn:{role}] error: {err}")
                    append_console(feed, f"[{role}·{task_key_of(task_file_abs)}] 超时（{timeout}s），交由 Orchestrator 决策")
                    if session_id:
                        open(session_path, "w", encoding="utf-8").write(session_id)
                    write_failure_result(result_path, role, err)
                    git_snapshot(workspace, f"{role} timeout ({os.path.basename(task_file_abs)})")
                    sys.exit(1)
                log_file.write(f"[warn] resume failed ({err}); falling back to fresh session\n")
                log_file.flush()
                result_event, session_id, err = None, None, None

        if result_event is None:
            log_file.write(f"\n===== [start] {role} | task={task_file} | {time.strftime('%H:%M:%S')} =====\n")
            log_file.flush()
            result_event, session_id, err = run_session(
                cmd_fresh, log_file, timeout, env, cwd, progress_path, feed)

        if session_id:
            try:
                open(session_path, "w", encoding="utf-8").write(session_id)
            except OSError:
                pass

        elapsed = time.time() - start_time

        if err or result_event is None:
            print(f"[spawn:{role}] error: {err}")
            append_console(feed, f"[{role}·{task_key_of(task_file_abs)}] 失败：{err or 'no result event'}")
            write_failure_result(result_path, role, err or "no result event")
            git_snapshot(workspace, f"{role} failed ({os.path.basename(task_file_abs)})")
            sys.exit(1)

        log_file.write(f"[done] {role} | {time.strftime('%H:%M:%S')} | elapsed={elapsed:.1f}s\n")

    # Write result text for Orchestrator
    with open(result_path, "w", encoding="utf-8") as f:
        f.write(result_event.get("result", ""))

    # Write metrics for Orchestrator to collect
    metrics = {
        "role": role,
        "duration_ms": result_event.get("duration_ms", 0),
        "duration_api_ms": result_event.get("duration_api_ms", 0),
        "usage": result_event.get("usage", {}),
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False)

    # 派活完成：进度心跳是瞬态信息，删掉以免播报里残留已完成派活的行
    try:
        os.remove(progress_path)
    except OSError:
        pass

    # 产出后快照：归档 Agent 的产出文件与 result/metrics
    git_snapshot(workspace, f"{role} done ({os.path.basename(task_file_abs)})")

    print(f"[spawn:{role}:{task_key_of(task_file_abs)}] done "
          f"({elapsed:.0f}s, log: debug/{os.path.basename(log_path)})")
    append_console(feed, f"[{role}·{task_key_of(task_file_abs)}] 完成（{elapsed:.0f}s）")


if __name__ == "__main__":
    main()
