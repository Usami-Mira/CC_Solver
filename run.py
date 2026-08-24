#!/usr/bin/env python3
"""Bootstrap — assembles Orchestrator prompt from prompts/ directory and launches via Claude Code CLI.
Streams Orchestrator output to terminal and log file in real-time.
"""

import sys, os, json, subprocess, time
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT))
from stream_parser import parse_stream_event

PROMPTS_DIR = ROOT / "prompts"
SKILLS_DIR = PROMPTS_DIR / "skills"

CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
MODEL = CONFIG.get("model", "sonnet")
PIPELINE = CONFIG.get("pipeline", "standard")
TIMEOUT = CONFIG.get("timeout_seconds", 600)
MAX_CONCURRENT = CONFIG.get("max_concurrent_problems", 3)


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


def assemble_orchestrator_prompt():
    """Assemble the complete orchestrator system prompt from components."""
    # Select orchestrator template based on pipeline type
    if PIPELINE == "standard":
        template = read_prompt("orchestrator")
        architecture_extra = ""
    elif PIPELINE == "parallel":
        template = read_prompt("orchestrator_parallel")
        architecture_extra = read_prompt("architecture_parallel")
        meta_planner = read_prompt("meta_planner")
    elif PIPELINE == "iterative":
        template = read_prompt("orchestrator_iterative")
        architecture_extra = read_prompt("architecture_iterative")
        explorer = read_prompt("explorer")
    elif PIPELINE == "debate":
        template = read_prompt("orchestrator_debate")
        architecture_extra = read_prompt("architecture_debate")
        secretary = read_prompt("secretary")
    elif PIPELINE == "tree_search":
        template = read_prompt("orchestrator_tree_search")
        architecture_extra = read_prompt("architecture_tree_search")
        # strategist = read_prompt("strategist")
        # validator = read_prompt("validator")
    else:
        print(f"Error: unknown pipeline '{PIPELINE}'")
        sys.exit(1)

    architecture = read_prompt("architecture")
    planner = read_prompt("planner")
    builder = read_prompt("builder")
    evaluator = read_prompt("evaluator")
    skills = read_skills()

    # Combine base architecture with pipeline-specific architecture
    full_architecture = architecture + "\n\n" + architecture_extra if architecture_extra else architecture

    # Step 1: Insert all sections into template
    prompt = template
    prompt = prompt.replace("{architecture}", full_architecture)
    prompt = prompt.replace("{planner_prompt}", planner 
                            if PIPELINE != "tree_search" else read_prompt("planner_tree_search"))
    prompt = prompt.replace("{builder_prompt}", builder)
    prompt = prompt.replace("{evaluator_prompt}", evaluator)
    prompt = prompt.replace("{skills}", skills)

    # Insert pipeline-specific prompts
    if PIPELINE == "parallel":
        prompt = prompt.replace("{meta_planner_prompt}", meta_planner)
    elif PIPELINE == "iterative":
        prompt = prompt.replace("{explorer_prompt}", explorer)
    elif PIPELINE == "debate":
        prompt = prompt.replace("{secretary_prompt}", secretary)
    elif PIPELINE == "tree_search":
        # prompt = prompt.replace("{planner_prompt}", read_prompt("planner_tree_search"))
        prompt = prompt.replace("{builder_ephemeral_prompt}", read_prompt("builder_ephemeral"))
        prompt = prompt.replace("{evaluator_ephemeral_prompt}", read_prompt("evaluator_ephemeral"))

    # Step 2: Replace config variables globally (including inside skills)
    # Runtime placeholders like {workspace} and {role} are preserved as-is
    prompt = prompt.replace("{project_root}", str(ROOT))
    prompt = prompt.replace("{max_concurrent_problems}", str(MAX_CONCURRENT))
    return prompt


def main():
    global PIPELINE

    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Physics problem solver with multiple pipelines")
    parser.add_argument("workspace", nargs="?", default="problems/001", help="Problem workspace directory")
    parser.add_argument("--pipeline", choices=["standard", "parallel", "iterative", "debate", "tree_search"],
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

    orchestrator_prompt = assemble_orchestrator_prompt()
    agents_json = json.dumps({
        "Orchestrator": {
            "description": f"Orchestrator — {PIPELINE} pipeline",
            "prompt": orchestrator_prompt,
        }
    })

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
        "--add-dir", workspace,
        "--model", MODEL,
        f"请解决 {workspace} 中的物理题目。\n"
        f"按照你的 system prompt 中的工作方式和 Architecture 执行。\n"
        f"创建子 Agent 的方法：Bash 调用 spawn.py <role> <workspace> <prompt_file> <task_file>\n"
        f"全部阶段完成后，将最终结果写入 {workspace}/final_summary.md。\n"
        f"工作目录: {workspace}",
    ]

    # Stream output to terminal and log file
    log_path = os.path.join(workspace, ".orchestrator.log")
    start_time = time.time()

    with open(log_path, "w", encoding="utf-8") as log_file:
        print(f"[Orchestrator] pipeline={PIPELINE}, started at {time.strftime('%H:%M:%S')}", flush=True)
        log_file.write(f"[start] Orchestrator | pipeline={PIPELINE} | {time.strftime('%H:%M:%S')}\n")
        log_file.flush()

        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )

        result_event = None

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

        # Wait for process to complete with timeout
        try:
            proc.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            print(f"[Orchestrator] timeout after {TIMEOUT}s, killing process...")
            proc.kill()
            proc.wait()
            sys.exit(1)

        elapsed = time.time() - start_time

        # Close stdout/stderr to prevent hanging
        if proc.stdout:
            proc.stdout.close()
        if proc.stderr:
            proc.stderr.close()

        if proc.returncode != 0:
            stderr_output = proc.stderr.read() if proc.stderr else ""
            print(f"[Orchestrator] error: exit code {proc.returncode}")
            print(stderr_output[:500])
            sys.exit(1)

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
