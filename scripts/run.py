#!/usr/bin/env python3
"""Bootstrap — assembles Orchestrator prompt from prompts/ directory and launches via Claude Code CLI.
Streams Orchestrator output to terminal and log file in real-time.
"""

import sys, os, json, signal, subprocess, threading, time
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPTS_DIR))
from stream_parser import parse_stream_event

PROMPTS_DIR = ROOT / "prompts"
SKILLS_DIR = PROMPTS_DIR / "skills"
SKILLS_DIR = PROMPTS_DIR / "skills"

CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
PIPELINE = CONFIG.get("pipeline", "standard")
MAX_CONCURRENT = CONFIG.get("max_concurrent_problems", 3)

# 读取当前 pipeline 的配置
PIPELINE_CONFIG = CONFIG.get("configs", {}).get(PIPELINE, {})
MODEL = PIPELINE_CONFIG.get("model", "sonnet")
TIMEOUT = PIPELINE_CONFIG.get("timeout_seconds", 600)
MAX_REVISIONS = PIPELINE_CONFIG.get("max_revisions", 2)
AGENT_MODELS = PIPELINE_CONFIG.get("agent_models", {})

# Pipeline-specific 配置
MAX_ITERATIONS = PIPELINE_CONFIG.get("max_iterations", 10)
MAX_ROUNDS = PIPELINE_CONFIG.get("max_rounds", 3)
NUM_PLANNERS = PIPELINE_CONFIG.get("num_planners", 3)
EPHEMERAL_TIMEOUT = PIPELINE_CONFIG.get("ephemeral_timeout", PIPELINE_CONFIG.get("calculation_timeout", 300))


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


def init_workspace_git(workspace):
    """Initialize git repo in workspace for version tracking."""
    git_dir = os.path.join(workspace, ".git")
    if os.path.exists(git_dir):
        print(f"[git] repo already exists in {workspace}")
        return

    # git init
    subprocess.run(["git", "init", workspace], check=True, capture_output=True)

    # Write .gitignore
    gitignore_path = os.path.join(workspace, ".gitignore")
    gitignore_content = """\
# Agent runtime artifacts
.*.log
.*.result
.*.metrics
.state
query_rag.py
__pycache__/
*.pyc
*.tmp
"""
    with open(gitignore_path, "w") as f:
        f.write(gitignore_content)

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
    elif PIPELINE in ["tree_search", "adaptive"]:
        agents_dict = {
            "planner": read_agent("planner"),
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

    return prompt


def main():
    global PIPELINE

    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Physics problem solver with multiple pipelines")
    parser.add_argument("workspace", nargs="?", default="problems/001", help="Problem workspace directory")
    parser.add_argument("--pipeline", choices=["standard", "parallel", "iterative", "debate", "tree_search", "adaptive"],
                       help="Override pipeline type from config.json")
    args = parser.parse_args()

    workspace = args.workspace

    # Override pipeline if specified on command line
    if args.pipeline:
        PIPELINE = args.pipeline

    # Copy RAG query script into workspace so agents can run it locally
    query_script = ROOT / "textbook" / "rag_build" / "query_rag.py"
    if query_script.exists():
        import shutil
        shutil.copy2(str(query_script), os.path.join(workspace, "query_rag.py"))

    # Set env vars so query_rag.py knows where model and data are
    os.environ["RAG_MODEL_DIR"] = str(ROOT / "textbook" / "models" / "bge-m3")
    os.environ["RAG_DATA_DIR"] = str(ROOT / "textbook" / "weaviate_data")

    # Initialize git repo in workspace
    init_workspace_git(workspace)

    orchestrator_prompt = assemble_orchestrator_prompt(workspace)
    agents_json = json.dumps({
        "Orchestrator": {
            "description": f"Orchestrator — {PIPELINE} pipeline",
            "prompt": orchestrator_prompt,
        }
    })

    # 绝对路径，避免 cwd 歧义
    workspace_abs = os.path.abspath(workspace)

    cmd = [
        "claude",
        "--print",
        "--output-format", "stream-json",
        "--verbose",
        "--permission-mode", "bypassPermissions",
        "--bare",
        "--agents", agents_json,
        "--agent", "Orchestrator",
        "--allowed-tools", "Bash,Read,Write",
        "--add-dir", workspace_abs,
        "--model", MODEL,
        f"请解决 {workspace_abs} 中的物理题目。\n"
        f"按照你的 system prompt 中的流程执行。\n"
        f"核心纪律：你不读题目、不做计算 — 只调度 sub-Agent，只读它们的 .result 汇报。\n"
        f"开始前先 cat {workspace_abs}/.state 确认是否有断点；没有则从第一阶段开始。\n"
        f"创建 sub-Agent：Bash 调用 python3 {SCRIPTS_DIR}/spawn.py <Role> {workspace_abs} <prompt_file> <task_file>\n"
        f"全部阶段完成后，将最终结果写入 {workspace_abs}/final_summary.md。\n"
        f"Workspace（绝对路径）: {workspace_abs}；你的 shell cwd 是项目根目录，所有文件操作请用上面的绝对路径。",
    ]

    # Stream output to terminal and log file
    log_path = os.path.join(workspace, ".orchestrator.log")
    start_time = time.time()

    with open(log_path, "w", encoding="utf-8") as log_file:
        print(f"[Orchestrator] pipeline={PIPELINE}, started at {time.strftime('%H:%M:%S')}", flush=True)
        log_file.write(f"[start] Orchestrator | pipeline={PIPELINE} | {time.strftime('%H:%M:%S')}\n")
        log_file.flush()

        # start_new_session=True：orchestrator 自成进程组，超时可整组杀掉而不伤及 run.py。
        # stderr 直接写日志文件而不用 PIPE，避免管道写满导致子进程阻塞。
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=log_file, text=True,
            start_new_session=True,
        )

        result_event = None

        def pump_stdout():
            nonlocal result_event
            for line in proc.stdout:
                line = line.strip()
                if not line:
                    continue
                etype, summary, event = parse_stream_event(line)
                if summary:
                    # Print concise progress to terminal
                    if etype == "tool_use":
                        print(f"  → {summary}", flush=True)
                    elif etype == "text":
                        # Only print first 100 chars of text to avoid spam
                        print(f"  [{etype}] {summary[:100]}{'...' if len(summary) > 100 else ''}", flush=True)
                    elif etype == "init":
                        print(f"  [{etype}] {summary}", flush=True)
                    elif etype == "result":
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
            sys.exit(1)

        # 已拿到结果：给进程一小段宽限期自行退出；若被孤儿子进程卡住，杀掉进程组。
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            print("[Orchestrator] 产出结果后 15s 未退出，杀掉进程组以继续")
            kill_process_group(proc)

        elapsed = time.time() - start_time

        if not result_event:
            print("[Orchestrator] error: no result event received")
            sys.exit(1)

        if result_event.get("is_error"):
            print(f"[Orchestrator] error: {result_event.get('result', 'Unknown')[:300]}")
            sys.exit(1)

        log_file.write(f"[done] Orchestrator | pipeline={PIPELINE} | {time.strftime('%H:%M:%S')} | elapsed={elapsed:.1f}s\n")

    print(f"\n[Orchestrator] done ({elapsed:.0f}s)")

    # Print summary
    summary_path = os.path.join(workspace, "final_summary.md")
    if os.path.exists(summary_path):
        print("\n" + "=" * 60)
        print(open(summary_path, encoding="utf-8").read())
    else:
        print("No summary file found.")


if __name__ == "__main__":
    main()
