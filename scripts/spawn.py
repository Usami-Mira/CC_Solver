#!/usr/bin/env python3
"""Helper script — spawn a sub-Agent via Claude Code CLI with streaming log.

Usage:
    spawn.py <role> <workspace> <prompt_file> <task_file> [--tools ...] [--timeout N] [--resume]

特性：
- **代码级阶段快照**：每次派活前、产出结果后自动 `git add -A && git commit`
  （任务文件、.state、Agent 产出全部入库，不依赖 Orchestrator 自觉）。
  并行 pipeline 会同时跑多个 spawn.py，用 flock 互斥。
- **断点续传**：每个子 Agent 的 session_id 记录在 `debug/.<role>.session`；
  带 `--resume` 时续接上次会话（用于超时/中断后重派），不带则全新开始（失败重做）。
- **Workspace 布局**：运行时文件（.log/.result/.metrics/.session/.progress）在 `debug/`，
  任务文件在 `tasks/`（向后兼容：根目录的任务文件也能找到）。
"""

import sys, os, json, fcntl, signal, subprocess, threading, time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPTS_DIR.parent.resolve()
sys.path.insert(0, str(SCRIPTS_DIR))
from stream_parser import parse_stream_event

CONFIG = json.loads((PROJECT_ROOT / "config.json").read_text(encoding="utf-8"))
# model / agent_models / timeout 都在 configs.<pipeline> 下，不在顶层
PIPELINE = CONFIG.get("pipeline", "standard")
PIPELINE_CONFIG = CONFIG.get("configs", {}).get(PIPELINE, {})
DEFAULT_MODEL = PIPELINE_CONFIG.get("model", CONFIG.get("model", "qwen3.6-plus"))
AGENT_MODELS = PIPELINE_CONFIG.get("agent_models", {})
TIMEOUT = PIPELINE_CONFIG.get("timeout_seconds", CONFIG.get("timeout_seconds", 600))

DEBUG_DIR = "debug"
TASKS_DIR = "tasks"

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


def run_session(cmd, log_file, timeout_sec, env, cwd):
    """启动一次 claude 会话并泵送流式输出。

    返回 (result_event, session_id, error)：
    - 正常：(event, sid, None)
    - 超时：(None, sid|None, "timeout after Ns")
    - 其他异常：(None|event, sid|None, 错误描述)
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

    system_prompt = open(prompt_file_abs, encoding="utf-8").read()
    if workspace:
        # 用绝对路径替换 {workspace}，因为下面会把 cwd 改成 workspace
        system_prompt = system_prompt.replace("{workspace}", workspace_abs)
    task = open(task_file_abs, encoding="utf-8").read()
    if workspace:
        task += f"\n\n**重要：** 所有文件操作必须在 `{workspace_abs}` 目录内进行，不要在项目根目录创建文件。"

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
        "--bare",
        "--agents", agents_json,
        "--agent", role,
        "--allowed-tools", allowed_tools,
        "--add-dir", workspace_abs or workspace,
        "--model", model,
    ]
    cmd_fresh = base_cmd + [task]

    # 运行时文件（全部在 debug/ 下）
    log_path = os.path.join(debug_dir, f".{role}.log")
    result_path = os.path.join(debug_dir, f".{role}.result")
    metrics_path = os.path.join(debug_dir, f".{role}.metrics")
    session_path = os.path.join(debug_dir, f".{role}.session")
    progress_path = os.path.join(debug_dir, f".{role}.progress")

    # 清理过期进度文件（进度是瞬态监控信息，不是审计记录，可删）
    try:
        os.remove(progress_path)
    except OSError:
        pass

    # 设置环境变量，让 hook 知道 workspace 路径
    env = os.environ.copy()
    env["WORKSPACE"] = os.path.abspath(workspace)
    cwd = workspace if os.path.isdir(workspace) else None

    # 派活前快照：归档 Orchestrator 刚写的任务文件 / .state
    git_snapshot(workspace, f"spawn {role} ({os.path.basename(task_file_abs)})")

    start_time = time.time()
    result_event = None
    session_id = None
    err = None

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
                log_file, timeout, env, cwd)
            if err:
                if err.startswith("timeout"):
                    # 超时不重试（重开会话会丢失已完成进度，交由上层决策）
                    print(f"[spawn:{role}] error: {err}")
                    if session_id:
                        open(session_path, "w", encoding="utf-8").write(session_id)
                    git_snapshot(workspace, f"{role} timeout ({os.path.basename(task_file_abs)})")
                    sys.exit(1)
                log_file.write(f"[warn] resume failed ({err}); falling back to fresh session\n")
                log_file.flush()
                result_event, session_id, err = None, None, None

        if result_event is None:
            log_file.write(f"\n===== [start] {role} | task={task_file} | {time.strftime('%H:%M:%S')} =====\n")
            log_file.flush()
            result_event, session_id, err = run_session(cmd_fresh, log_file, timeout, env, cwd)

        if session_id:
            try:
                open(session_path, "w", encoding="utf-8").write(session_id)
            except OSError:
                pass

        elapsed = time.time() - start_time

        if err or result_event is None:
            print(f"[spawn:{role}] error: {err}")
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

    # 产出后快照：归档 Agent 的产出文件与 result/metrics
    git_snapshot(workspace, f"{role} done ({os.path.basename(task_file_abs)})")

    print(f"[spawn:{role}] done ({elapsed:.0f}s, log: debug/.{role}.log)")


if __name__ == "__main__":
    main()
