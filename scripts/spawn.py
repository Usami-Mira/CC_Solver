#!/usr/bin/env python3
"""Helper script — spawn a sub-Agent via Claude Code CLI with streaming log.

Usage: spawn.py <role> <workspace> <prompt_file> <task_file> [--tools Read,Write,Edit,Bash]
"""

import sys, os, json, signal, subprocess, threading, time
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT))
from stream_parser import parse_stream_event

CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
# model / agent_models / timeout 都在 configs.<pipeline> 下，不在顶层
PIPELINE = CONFIG.get("pipeline", "standard")
PIPELINE_CONFIG = CONFIG.get("configs", {}).get(PIPELINE, {})
DEFAULT_MODEL = PIPELINE_CONFIG.get("model", CONFIG.get("model", "qwen3.6-plus"))
AGENT_MODELS = PIPELINE_CONFIG.get("agent_models", {})
TIMEOUT = PIPELINE_CONFIG.get("timeout_seconds", CONFIG.get("timeout_seconds", 600))

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


def main():
    if len(sys.argv) < 5:
        print("Usage: spawn.py <role> <workspace> <prompt_file> <task_file> [--tools Read,Write,Edit,Bash]")
        sys.exit(1)

    role = sys.argv[1]
    workspace = sys.argv[2]
    prompt_file = sys.argv[3]
    task_file = sys.argv[4]

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
    for i, arg in enumerate(sys.argv):
        if arg == "--tools" and i + 1 < len(sys.argv):
            allowed_tools = sys.argv[i + 1]

    # 转换为绝对路径，因为 cwd 会改成 workspace
    prompt_file_abs = str(ROOT / "prompts" / f"{prompt_file}.md")

    # 查找 task 文件：先在 workspace 中找，找不到再去当前目录找
    if os.path.isabs(task_file):
        task_file_abs = task_file
    elif os.path.exists(os.path.join(workspace, f"{task_file}.md")):
        task_file_abs = os.path.join(workspace, f"{task_file}.md")
    elif os.path.exists(os.path.join(workspace, task_file)):
        task_file_abs = os.path.join(workspace, task_file)
    elif os.path.exists(f"{task_file}.md"):
        task_file_abs = f"{task_file}.md"
    else:
        task_file_abs = task_file

    system_prompt = open(prompt_file_abs, encoding="utf-8").read()
    workspace_abs = os.path.abspath(workspace) if workspace else ""
    if workspace:
        # 用绝对路径替换 {workspace}，因为下面会把 cwd 改成 workspace
        system_prompt = system_prompt.replace("{workspace}", workspace_abs)
    task = open(task_file_abs, encoding="utf-8").read()
    if workspace:
        task += f"\n\n**重要：** 所有文件操作必须在 `{workspace_abs}` 目录内进行，不要在项目根目录创建文件。"

    agents_json = json.dumps({role: {"description": f"{role} Agent", "prompt": system_prompt}})

    cmd = [
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
        task,
    ]

    log_path = os.path.join(workspace, f".{role}.log")
    start_time = time.time()

    # 设置环境变量，让 hook 知道 workspace 路径
    env = os.environ.copy()
    env["WORKSPACE"] = os.path.abspath(workspace)

    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"\n===== [start] {role} | task={task_file} | {time.strftime('%H:%M:%S')} =====\n")
        log_file.flush()

        # 设置工作目录为 workspace，确保 Agent 在正确的位置创建文件。
        # start_new_session=True：子进程自成进程组，必要时可整组杀掉
        # （claude 常派生后台子进程；若有孤儿进程卡住，claude 本体不退出）。
        # stderr 直接写入日志文件而不用 PIPE，避免管道写满导致子进程阻塞。
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=log_file, text=True,
            cwd=workspace if os.path.isdir(workspace) else None,
            env=env,
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
                    log_file.write(f"[{etype}] {summary}\n")
                    log_file.flush()
                if etype == "result" and event:
                    result_event = event
                    return  # 拿到结果即返回，不等 EOF（进程可能被孤儿子进程卡住而不退出）

        pump_thread = threading.Thread(target=pump_stdout, daemon=True)
        pump_thread.start()
        pump_thread.join(timeout=TIMEOUT)

        if pump_thread.is_alive():
            log_file.write(f"[error] timeout after {TIMEOUT}s, killing process group\n")
            log_file.flush()
            kill_process_group(proc)
            print(f"[spawn:{role}] error: timeout after {TIMEOUT}s")
            sys.exit(1)

        # 已拿到结果：给进程一小段宽限期自行退出；
        # 若它因等待孤儿后台进程而不退出，直接杀掉整个进程组。
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            log_file.write(f"[warn] {role} 在产出结果后 15s 未退出，杀掉进程组以继续\n")
            log_file.flush()
            kill_process_group(proc)

        elapsed = time.time() - start_time

        if not result_event:
            log_file.write(f"[error] no result event received\n")
            log_file.flush()
            print(f"[spawn:{role}] error: no result event")
            sys.exit(1)

        if result_event.get("is_error"):
            err_msg = result_event.get("result", "Unknown")[:300]
            log_file.write(f"[error] {err_msg}\n")
            log_file.flush()
            print(f"[spawn:{role}] error: {err_msg}")
            sys.exit(1)

        log_file.write(f"[done] {role} | {time.strftime('%H:%M:%S')} | elapsed={elapsed:.1f}s\n")

    # Write result text for Orchestrator
    result_path = os.path.join(workspace, f".{role}.result")
    with open(result_path, "w", encoding="utf-8") as f:
        f.write(result_event.get("result", ""))

    # Write metrics for Orchestrator to collect
    metrics = {
        "role": role,
        "duration_ms": result_event.get("duration_ms", 0),
        "duration_api_ms": result_event.get("duration_api_ms", 0),
        "usage": result_event.get("usage", {}),
    }
    metrics_path = os.path.join(workspace, f".{role}.metrics")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False)

    print(f"[spawn:{role}] done ({elapsed:.0f}s, log: .{role}.log)")


if __name__ == "__main__":
    main()
