#!/usr/bin/env python3
"""Bootstrap — assembles Orchestrator prompt from prompts/ directory and launches via Claude Code CLI.
Streams Orchestrator output to terminal and log file in real-time.
"""

import sys, os, json, signal, subprocess, threading, time
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPTS_DIR))
import load_env  # noqa: F401 — 自动载入 .env（setup.sh 写入的 API 配置）
from stream_parser import parse_stream_event
import memory_guard

PROMPTS_DIR = ROOT / "prompts"
SKILLS_DIR = PROMPTS_DIR / "skills"

CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
PIPELINE = CONFIG.get("pipeline", "standard")
MAX_CONCURRENT = CONFIG.get("max_concurrent_problems", 3)
MAX_DISPUTES = CONFIG.get("max_disputes", 2)          # 修订争议协议上限（全局）
MEMORY_GUARD_MODE = CONFIG.get("memory_guard", "quarantine")

# 当前 pipeline 的配置（导入时按 config 默认值初始化，--pipeline 覆盖时经
# apply_pipeline_config 重新派生；assemble/进度显示/超时均读这些全局量）
PIPELINE_CONFIG = {}
MODEL = "sonnet"
TIMEOUT = 600
MAX_REVISIONS = 2
AGENT_MODELS = {}
MAX_ITERATIONS = 10
MAX_ROUNDS = 3
NUM_PLANNERS = 3
EPHEMERAL_TIMEOUT = 300
DEEP_TIMEOUT = 1800
MAX_MOTIONS = 6


def apply_pipeline_config(name):
    """按 pipeline 名设置模块级配置变量。"""
    global PIPELINE, PIPELINE_CONFIG, MODEL, TIMEOUT, MAX_REVISIONS, AGENT_MODELS
    global MAX_ITERATIONS, MAX_ROUNDS, NUM_PLANNERS, EPHEMERAL_TIMEOUT, DEEP_TIMEOUT, MAX_MOTIONS
    PIPELINE = name
    PIPELINE_CONFIG = CONFIG.get("configs", {}).get(name, {})
    MODEL = PIPELINE_CONFIG.get("model", "sonnet")
    TIMEOUT = PIPELINE_CONFIG.get("timeout_seconds", 600)
    MAX_REVISIONS = PIPELINE_CONFIG.get("max_revisions", 2)
    AGENT_MODELS = PIPELINE_CONFIG.get("agent_models", {})
    MAX_ITERATIONS = PIPELINE_CONFIG.get("max_iterations", 10)
    MAX_ROUNDS = PIPELINE_CONFIG.get("max_rounds", 3)
    NUM_PLANNERS = PIPELINE_CONFIG.get("num_planners", 3)
    EPHEMERAL_TIMEOUT = PIPELINE_CONFIG.get("ephemeral_timeout",
                                            PIPELINE_CONFIG.get("calculation_timeout", 300))
    DEEP_TIMEOUT = PIPELINE_CONFIG.get("deep_timeout", 1800)
    MAX_MOTIONS = PIPELINE_CONFIG.get("max_motions", 6)


apply_pipeline_config(PIPELINE)

DEBUG_DIR = "debug"
TASKS_DIR = "tasks"

GITIGNORE_TEMPLATE = """\
# 运行时记录（.log/.result/.metrics/.state）已移入 debug/ 并提交入库（审计用）。
# 这里只忽略缓存与临时文件。
query_rag.py
__pycache__/
*.pyc
*.tmp
.claude/
"""


def read_prompt(name):
    """Read a prompt file from prompts/ directory."""
    path = PROMPTS_DIR / f"{name}.md"
    if not path.exists():
        print(f"Error: {path} not found")
        sys.exit(1)
    return path.read_text(encoding="utf-8").strip()


def read_skills():
    """Read all skill files from prompts/skills/ and concatenate."""
    if not SKILLS_DIR.exists():
        return ""
    parts = []
    for f in sorted(SKILLS_DIR.glob("*.md")):
        parts.append(f.read_text(encoding="utf-8").strip())
    return "\n\n".join(parts)


def ensure_workspace_layout(workspace):
    """创建 debug/ + tasks/ 子目录，并确保 .gitignore 为最新模板（幂等）。

    同时写入 .claude/settings.json：注册 path_guard PreToolUse hook。
    sub-agent 的 cwd 是 workspace（独立 git 仓库，即其"项目根"），
    Claude Code 从那里发现 .claude/ 配置——这是把硬封锁注入会话的唯一挂点。
    """
    os.makedirs(os.path.join(workspace, DEBUG_DIR), exist_ok=True)
    os.makedirs(os.path.join(workspace, TASKS_DIR), exist_ok=True)
    gitignore_path = os.path.join(workspace, ".gitignore")
    try:
        if not os.path.exists(gitignore_path) or open(gitignore_path).read() != GITIGNORE_TEMPLATE:
            with open(gitignore_path, "w") as f:
                f.write(GITIGNORE_TEMPLATE)
    except OSError:
        pass

    # path_guard hook（绝对路径，避免 git rev-parse 解析到 workspace 仓库的陷阱）
    settings = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Read|Write|Edit|NotebookEdit|NotebookRead|Glob|Grep|Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python3 \"{SCRIPTS_DIR / 'path_guard.py'}\"",
                        }
                    ],
                }
            ]
        }
    }
    try:
        claude_dir = os.path.join(workspace, ".claude")
        os.makedirs(claude_dir, exist_ok=True)
        settings_path = os.path.join(claude_dir, "settings.json")
        content = json.dumps(settings, indent=2) + "\n"
        if not os.path.exists(settings_path) or open(settings_path).read() != content:
            with open(settings_path, "w") as f:
                f.write(content)
    except OSError:
        pass


def init_workspace_git(workspace):
    """Initialize git repo in workspace for version tracking."""
    ensure_workspace_layout(workspace)
    git_dir = os.path.join(workspace, ".git")
    if os.path.exists(git_dir):
        print(f"[git] repo already exists in {workspace}")
        return

    # git init
    subprocess.run(["git", "init", workspace], check=True, capture_output=True)

    # Configure git user
    subprocess.run(["git", "-C", workspace, "config", "user.email", "agent@physics-solver"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", workspace, "config", "user.name", "Physics Agent"],
                   check=True, capture_output=True)

    # Initial commit
    subprocess.run(["git", "-C", workspace, "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", workspace, "commit", "-m", "init: workspace setup with problem files"],
        check=True, capture_output=True
    )
    print(f"[git] initialized repo in {workspace}")


def read_agent(name):
    """Read an agent file from prompts/agents/ directory."""
    path = PROMPTS_DIR / "agents" / f"{name}.md"
    if not path.exists():
        print(f"Warning: agent '{name}' not found at {path}")
        return ""
    return path.read_text(encoding="utf-8").strip()


def read_pipeline(name):
    """Read a pipeline config from prompts/pipelines/ directory."""
    path = PROMPTS_DIR / "pipelines" / f"{name}.md"
    if not path.exists():
        print(f"Error: pipeline '{name}' not found at {path}")
        sys.exit(1)
    return path.read_text(encoding="utf-8").strip()


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


VERDICT_ICON = {"PASS": "✅", "FAIL": "❌", "REVISE": "🔁", "SOUND": "🔍",
                "CONSENSUS": "🤝", "DISPUTED": "⚔️", "DONE": "🏁", "BRANCH": "🌿"}


def parse_state_file(path):
    """解析 .state：支持 'key: value' 多行、单单词、多行阶段列表三种格式。"""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError:
        return {}
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    kv_lines = [ln for ln in lines if ":" in ln]
    if kv_lines:
        d = {}
        for ln in kv_lines:
            k, v = ln.split(":", 1)
            d[k.strip()] = v.strip()
        return d
    if lines:
        return {"stage": lines[-1]}
    return {}


def find_state_file(workspace):
    """优先 debug/.state（新布局），回退 .state（旧布局）。"""
    for rel in (os.path.join(DEBUG_DIR, ".state"), ".state"):
        p = os.path.join(workspace, rel)
        if os.path.exists(p):
            return p
    return os.path.join(workspace, DEBUG_DIR, ".state")


def read_progress_lines(workspace):
    """读 debug/.*.progress（Agent 内部进度），返回 ["Builder 3/7: ...", ...]。"""
    segs = []
    d = os.path.join(workspace, DEBUG_DIR)
    try:
        for name in sorted(os.listdir(d)):
            if name.startswith(".") and name.endswith(".progress"):
                with open(os.path.join(d, name), encoding="utf-8", errors="replace") as f:
                    txt = f.read().strip()
                if txt:
                    role = name[1:-len(".progress")]
                    segs.append(f"{role} {txt.splitlines()[-1][:50]}")
    except OSError:
        pass
    return segs


def render_progress(state, start_time, progress=()):
    """把 .state 渲染成一行带进度条的状态文本。"""
    stage = state.get("stage", "?")
    iteration = state.get("iteration")
    verdict = state.get("last_verdict")
    nxt = state.get("next")
    elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    head = f"[progress {elapsed}] {PIPELINE} · {stage}"
    segs = []
    if iteration:
        try:
            n = int(iteration)
            # 修订阶段以 max_revisions 为分母，其余以 max_iterations 为分母
            total = MAX_REVISIONS if "revise" in str(stage) else MAX_ITERATIONS
            head += f" {n}/{total}" if total else f" {n}"
            if total:
                width = 10
                k = max(0, min(width, round(n / total * width)))
                segs.append("█" * k + "░" * (width - k))
        except ValueError:
            head += f" {iteration}"
    if verdict and verdict != "-":
        segs.append(f"{VERDICT_ICON.get(verdict, '')} {verdict}".strip())
    if nxt:
        segs.append(f"→ {nxt}")
    segs.extend(progress)
    return " ".join([head] + segs)


def resume_session_id(workspace):
    """若上次运行未完成且留有会话记录，返回可续接的 orchestrator session id。"""
    sess = os.path.join(workspace, DEBUG_DIR, ".orchestrator_session")
    try:
        with open(sess, encoding="utf-8") as f:
            sid = f.read().strip()
    except OSError:
        return None
    if not sid:
        return None
    st = parse_state_file(find_state_file(workspace))
    if str(st.get("stage", "")).lower() in ("complete", "done"):
        return None
    if os.path.exists(os.path.join(workspace, "final_summary.md")):
        return None
    return sid


def assemble_orchestrator_prompt(workspace):
    """Assemble the complete orchestrator system prompt from components."""
    # 读取通用 orchestrator
    template = read_prompt("orchestrator")

    # 读取 pipeline 配置
    pipeline_config = read_pipeline(PIPELINE)

    # 读取所需的 agents（根据 pipeline）
    agents_dict = {}
    if PIPELINE == "standard":
        agents_dict = {
            "planner": read_agent("planner"),
            "builder": read_agent("builder"),
            "evaluator": read_agent("evaluator"),
        }
    elif PIPELINE == "parallel":
        agents_dict = {
            "planner": read_agent("planner"),
            "meta_planner": read_agent("meta_planner"),
            "builder": read_agent("builder"),
            "evaluator": read_agent("evaluator"),
        }
    elif PIPELINE == "iterative":
        agents_dict = {
            "explorer": read_agent("explorer"),
            "builder": read_agent("builder"),
            "evaluator": read_agent("evaluator"),
        }
    elif PIPELINE == "debate":
        agents_dict = {
            "theorist": read_agent("theorist"),
            "computationalist": read_agent("computationalist"),
            "experimentalist": read_agent("experimentalist"),
            "critic": read_agent("critic"),
            "secretary": read_agent("secretary"),
            "builder": read_agent("builder"),
            "evaluator": read_agent("evaluator"),
        }
    elif PIPELINE == "tree_search":
        # Planner 用解除"一种方法"限制的深度规划版（agents/planner_deep.md）：
        # 树搜索要求根展开生成 ≥2 个结构不同分支、节点以 BRANCH 汇报，
        # 基础 planner.md 的"一种方法"纪律与此直接冲突。
        agents_dict = {
            "planner": read_agent("planner_deep"),
            "verifier": read_agent("verifier"),
            "builder": read_agent("builder"),
            "evaluator": read_agent("evaluator"),
        }
    elif PIPELINE == "adaptive":
        agents_dict = {
            "planner": read_agent("planner"),
            "verifier": read_agent("verifier"),
            "builder": read_agent("builder"),
            "evaluator": read_agent("evaluator"),
        }
    elif PIPELINE == "deep_search":
        # Planner 用解除"一种方法"限制的深度搜索专用版（agents/planner_deep.md）；
        # spawn 时 prompt_file 传 agents/planner_deep，角色仍是 Planner。
        # 阶段 3 辩论共识复用 Debate 流水线的专家与书记角色。
        agents_dict = {
            "planner": read_agent("planner_deep"),
            "theorist": read_agent("theorist"),
            "computationalist": read_agent("computationalist"),
            "experimentalist": read_agent("experimentalist"),
            "critic": read_agent("critic"),
            "secretary": read_agent("secretary"),
            "verifier": read_agent("verifier"),
            "builder": read_agent("builder"),
            "evaluator": read_agent("evaluator"),
        }
    else:
        print(f"Error: unknown pipeline '{PIPELINE}'")
        sys.exit(1)

    # 组装 agents 列表
    agents_list = "\n\n".join([
        f"### {name.replace('_', ' ').title()}\n\n{content}"
        for name, content in agents_dict.items()
    ])

    # 读取 skills
    skills = read_skills()

    # 组装完整 prompt
    prompt = template
    prompt = prompt.replace("{pipeline}", PIPELINE)
    prompt = prompt.replace("{pipeline_config}", pipeline_config)
    prompt = prompt.replace("{agents_list}", agents_list)
    prompt = prompt.replace("{skills}", skills)

    # 替换配置参数
    prompt = prompt.replace("{project_root}", str(ROOT))
    prompt = prompt.replace("{workspace}", os.path.abspath(workspace))
    prompt = prompt.replace("{timeout_seconds}", str(TIMEOUT))
    prompt = prompt.replace("{max_concurrent_problems}", str(MAX_CONCURRENT))
    prompt = prompt.replace("{max_revisions}", str(MAX_REVISIONS))
    prompt = prompt.replace("{max_iterations}", str(MAX_ITERATIONS))
    prompt = prompt.replace("{max_rounds}", str(MAX_ROUNDS))
    prompt = prompt.replace("{num_planners}", str(NUM_PLANNERS))
    prompt = prompt.replace("{ephemeral_timeout}", str(EPHEMERAL_TIMEOUT))
    prompt = prompt.replace("{deep_timeout}", str(DEEP_TIMEOUT))
    prompt = prompt.replace("{max_motions}", str(MAX_MOTIONS))
    prompt = prompt.replace("{max_disputes}", str(MAX_DISPUTES))

    return prompt


def main():
    global PIPELINE

    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Physics problem solver with multiple pipelines")
    parser.add_argument("workspace", nargs="?", default="problems/001", help="Problem workspace directory")
    parser.add_argument("--pipeline", choices=["standard", "parallel", "iterative", "debate", "tree_search", "adaptive", "deep_search"],
                       help="Override pipeline type from config.json")
    args = parser.parse_args()

    workspace = args.workspace

    # Override pipeline if specified on command line
    if args.pipeline:
        apply_pipeline_config(args.pipeline)

    # 传给 spawn.py：它需要从同一 pipeline 配置读模型/超时（顶层 config 可能是别的流水线）
    os.environ["SOLVER_PIPELINE"] = PIPELINE

    # Copy RAG query script into workspace so agents can run it locally
    query_script = ROOT / "textbook" / "rag_build" / "query_rag.py"
    if query_script.exists():
        import shutil
        shutil.copy2(str(query_script), os.path.join(workspace, "query_rag.py"))

    # Set env vars so query_rag.py knows where model and data are
    os.environ["RAG_MODEL_DIR"] = str(ROOT / "textbook" / "models" / "bge-m3")
    os.environ["RAG_DATA_DIR"] = str(ROOT / "textbook" / "weaviate_data")

    # Initialize git repo in workspace（并确保新布局：debug/ + tasks/）
    init_workspace_git(workspace)

    # 记忆防火墙：运行前基线（防止"前世记忆"影响解题）
    mg_pre = memory_guard.pre_run(workspace)
    print(f"[memory] {memory_guard.render(mg_pre)}")

    orchestrator_prompt = assemble_orchestrator_prompt(workspace)
    agents_json = json.dumps({
        "Orchestrator": {
            "description": f"Orchestrator — {PIPELINE} pipeline",
            "prompt": orchestrator_prompt,
        }
    })

    # 绝对路径，避免 cwd 歧义
    workspace_abs = os.path.abspath(workspace)
    sess_path = os.path.join(workspace_abs, DEBUG_DIR, ".orchestrator_session")

    def build_cmd(user_prompt, resume_sid=None):
        cmd = [
            "claude",
            "--print",
            "--output-format", "stream-json",
            "--verbose",
            "--permission-mode", "bypassPermissions",
            "--agents", agents_json,
            "--agent", "Orchestrator",
            "--allowed-tools", "Bash,Read,Write",
            "--add-dir", workspace_abs,
            "--model", MODEL,
        ]
        if resume_sid:
            cmd += ["--resume", resume_sid]
        cmd.append(user_prompt)
        return cmd

    # path_guard 封锁环境变量：WORKSPACE 激活 hook，ROLE 决定允许根
    # （注意：不再用 --bare——它会连同 hooks 一起跳过，使封锁失效；
    #   auto-memory 改由 memory_guard 运行期清空记忆目录来阻断）
    orch_env = os.environ.copy()
    orch_env["WORKSPACE"] = workspace_abs
    orch_env["WORKSPACE_ROLE"] = "orchestrator"

    fresh_prompt = (
        f"请解决 {workspace_abs} 中的物理题目。\n"
        f"按照你的 system prompt 中的流程执行。\n"
        f"核心纪律：你不读题目、不做计算 — 只调度 sub-Agent，只读它们的 .result 汇报。\n"
        f"开始前先 cat {workspace_abs}/debug/.state 确认是否有断点（旧布局可能在 {workspace_abs}/.state）；没有则从第一阶段开始。\n"
        f"创建 sub-Agent：Bash 调用 python3 {SCRIPTS_DIR}/spawn.py <Role> {workspace_abs} <prompt_file> <task_file>\n"
        f"全部阶段完成后，将最终结果写入 {workspace_abs}/final_summary.md。\n"
        f"Workspace（绝对路径）: {workspace_abs}；你的 shell cwd 就是该工作区，文件操作请一律用上面的绝对路径。"
    )
    resume_prompt_text = (
        f"断点续传：上次会话被中断。请先 cat {workspace_abs}/debug/.state 恢复进度，然后从中断处继续编排。\n"
        f"核心纪律不变：你不读题目、不做计算 — 只调度 sub-Agent，只读它们的 .result 汇报。\n"
        f"创建 sub-Agent：Bash 调用 python3 {SCRIPTS_DIR}/spawn.py <Role> {workspace_abs} <prompt_file> <task_file>\n"
        f"Workspace（绝对路径）: {workspace_abs}"
    )

    resume_sid = resume_session_id(workspace)

    # Stream output to terminal and log file
    log_path = os.path.join(workspace, DEBUG_DIR, ".orchestrator.log")
    start_time = time.time()

    with open(log_path, "a", encoding="utf-8") as log_file:
        mode_desc = f"resume={resume_sid[:8]}" if resume_sid else "fresh"
        print(f"[Orchestrator] pipeline={PIPELINE}, {mode_desc}, started at {time.strftime('%H:%M:%S')}", flush=True)
        log_file.write(f"[start] Orchestrator | pipeline={PIPELINE} | {mode_desc} | {time.strftime('%H:%M:%S')}\n")
        log_file.flush()

        def launch(cmd):
            """启动一次 Orchestrator 会话并泵送输出。超时则整组杀掉并退出。"""
            # start_new_session=True：orchestrator 自成进程组，超时可整组杀掉而不伤及 run.py。
            # stderr 直接写日志文件而不用 PIPE，避免管道写满导致子进程阻塞。
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=log_file, text=True,
                start_new_session=True, env=orch_env,
                # cwd=workspace：Orchestrator 的记忆 slug 与 sub-agent 一致
                # （工作区专属），主项目记忆目录全程不被触碰——用户在运行期间
                # 的交互式 CC 会话照常读写记忆。path_guard 封锁不受影响：
                # workspace/.claude/settings.json 由 ensure_workspace_layout 注入。
                cwd=workspace_abs,
            )

            result_event = None

            def pump_stdout():
                nonlocal result_event
                for line in proc.stdout:
                    line = line.strip()
                    if not line:
                        continue
                    etype, summary, event = parse_stream_event(line)
                    if etype == "init" and event and event.get("session_id"):
                        try:
                            with open(sess_path, "w", encoding="utf-8") as sf:
                                sf.write(event["session_id"])
                        except OSError:
                            pass
                    if summary:
                        # Print concise progress to terminal
                        if etype == "tool_use":
                            print(f"  → {summary}", flush=True)
                        elif etype == "text":
                            # Only print first 100 chars of text to avoid spam
                            print(f"  [{etype}] {summary[:100]}{'...' if len(summary) > 100 else ''}", flush=True)
                        elif etype in ("init", "result"):
                            print(f"  [{etype}] {summary}", flush=True)
                        # Write full summary to log
                        log_file.write(f"[{etype}] {summary}\n")
                        log_file.flush()
                    if etype == "result" and event:
                        result_event = event
                        return  # 拿到结果即返回，不等 EOF（进程可能被孤儿子进程卡住而不退出）

            pump_thread = threading.Thread(target=pump_stdout, daemon=True)
            pump_thread.start()
            pump_thread.join(timeout=TIMEOUT)

            if pump_thread.is_alive():
                print(f"[Orchestrator] timeout after {TIMEOUT}s, killing process group...")
                kill_process_group(proc)
                progress_stop.set()
                sys.exit(1)

            # 已拿到结果：给进程一小段宽限期自行退出；若被孤儿子进程卡住，杀掉进程组。
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                print("[Orchestrator] 产出结果后 15s 未退出，杀掉进程组以继续")
                kill_process_group(proc)

            return result_event

        # 进度显示：每 5 秒轮询 .state（优先 debug/.state），变化时打印进度条（另每 5 分钟心跳）
        progress_stop = threading.Event()

        def progress_monitor():
            last_key = None
            last_print = 0.0
            while not progress_stop.wait(5):
                try:
                    st = parse_state_file(find_state_file(workspace))
                    if not st:
                        continue
                    key = json.dumps(st, sort_keys=True)
                    now = time.time()
                    if key != last_key or now - last_print >= 300:
                        line = render_progress(st, start_time, read_progress_lines(workspace))
                        print(line, flush=True)
                        log_file.write(line + "\n")
                        log_file.flush()
                        last_key = key
                        last_print = now
                except Exception:
                    pass  # 进度显示失败绝不影响主流程

        progress_thread = threading.Thread(target=progress_monitor, daemon=True)
        progress_thread.start()

        # 启动：有可续接会话则先 --resume；失败（非超时）则回退全新会话
        if resume_sid:
            result_event = launch(build_cmd(resume_prompt_text, resume_sid))
            if result_event is None or result_event.get("is_error"):
                log_file.write("[warn] resume failed; falling back to fresh session\n")
                log_file.flush()
                print("[Orchestrator] resume failed, starting fresh session")
                result_event = launch(build_cmd(fresh_prompt))
        else:
            result_event = launch(build_cmd(fresh_prompt))

        progress_stop.set()
        progress_thread.join(timeout=5)
        elapsed = time.time() - start_time

        if not result_event:
            print("[Orchestrator] error: no result event received")
            sys.exit(1)

        if result_event.get("is_error"):
            print(f"[Orchestrator] error: {result_event.get('result', 'Unknown')[:300]}")
            sys.exit(1)

        log_file.write(f"[done] Orchestrator | pipeline={PIPELINE} | {time.strftime('%H:%M:%S')} | elapsed={elapsed:.1f}s\n")

    print(f"\n[Orchestrator] done ({elapsed:.0f}s)")

    # 记忆防火墙：运行后审计（quarantine 模式会把运行期间的改动捕获并重置）
    mg_post = memory_guard.post_run(workspace, baselines=mg_pre.get("baselines"),
                                    baseline=mg_pre.get("baseline"))
    print(f"[memory] {memory_guard.render(mg_post)}")
    try:
        with open(os.path.join(workspace, DEBUG_DIR, ".memory_audit"), "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] pre: baseline={mg_pre.get('baseline', '-')} "
                    f"| post: {memory_guard.render(mg_post)}\n")
    except OSError:
        pass

    # Print summary
    summary_path = os.path.join(workspace, "final_summary.md")
    if os.path.exists(summary_path):
        # 追加记忆审计段（答题独立性的佐证之一）
        if not mg_post.get("skipped"):
            try:
                changed = mg_post.get("changed", False)
                with open(summary_path, "a", encoding="utf-8") as f:
                    f.write("\n## 记忆审计\n\n"
                            f"- 模式: {MEMORY_GUARD_MODE}\n"
                            f"- 运行前基线: `{mg_pre.get('baseline', '-')}`\n"
                            f"- 运行期间记忆目录改动: {'有（已捕获进 git 历史并重置回基线）' if changed else '无'}\n")
            except OSError:
                pass
        print("\n" + "=" * 60)
        print(open(summary_path, encoding="utf-8").read())
    else:
        print("No summary file found.")

    # 收尾提交：final_summary.md / 记忆审计等尾部写入入库（spawn.py 的快照覆盖不到运行结束后）
    try:
        subprocess.run(["git", "-C", workspace_abs, "add", "-A"], capture_output=True, timeout=120)
        subprocess.run(["git", "-C", workspace_abs, "commit", "-m",
                        f"{PIPELINE}: run complete (summary + memory audit)"],
                       capture_output=True, timeout=120)
    except Exception:
        pass


if __name__ == "__main__":
    main()
