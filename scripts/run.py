#!/usr/bin/env python3
"""Bootstrap — assembles Orchestrator prompt from prompts/ directory and launches via Claude Code CLI.
Streams Orchestrator output to terminal and log file in real-time.
"""

import sys, os, json, re, signal, subprocess, threading, time
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
MAX_CONCURRENT_AGENTS = CONFIG.get("max_concurrent_agents", 4)   # 同时派活的 sub-Agent 上限（软约束，供用户调）
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
MAX_VERIFY_ROUNDS = 3
MAX_SUBTASKS = 3
MAX_PHASES = 6            # auto：蓝图阶段数上限
MAX_SPAWNS = 40           # auto：全程派活总数上限
MAX_ESCALATIONS = 2       # auto：结构升级次数上限
MAX_SEARCH_ROUNDS = 4     # auto：搜索块轮数上限
MAX_DEBATE_ROUNDS = 2     # auto：辩论块轮数上限
MAX_AUTO_RESUMES = 30   # 监督者自动续跑上限（会话早退但流水线未完成时 --resume 续接）


def apply_pipeline_config(name):
    """按 pipeline 名设置模块级配置变量。"""
    global PIPELINE, PIPELINE_CONFIG, MODEL, TIMEOUT, MAX_REVISIONS, AGENT_MODELS
    global MAX_ITERATIONS, MAX_ROUNDS, NUM_PLANNERS, EPHEMERAL_TIMEOUT, DEEP_TIMEOUT, MAX_MOTIONS
    global MAX_VERIFY_ROUNDS, MAX_SUBTASKS, MAX_CONCURRENT_AGENTS
    global MAX_PHASES, MAX_SPAWNS, MAX_ESCALATIONS, MAX_SEARCH_ROUNDS, MAX_DEBATE_ROUNDS
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
    MAX_VERIFY_ROUNDS = PIPELINE_CONFIG.get("max_verify_rounds", 3)
    MAX_SUBTASKS = PIPELINE_CONFIG.get("max_subtasks", 3)
    MAX_CONCURRENT_AGENTS = PIPELINE_CONFIG.get("max_concurrent_agents", MAX_CONCURRENT_AGENTS)
    MAX_PHASES = PIPELINE_CONFIG.get("max_phases", MAX_PHASES)
    MAX_SPAWNS = PIPELINE_CONFIG.get("max_spawns", MAX_SPAWNS)
    MAX_ESCALATIONS = PIPELINE_CONFIG.get("max_escalations", MAX_ESCALATIONS)
    MAX_SEARCH_ROUNDS = PIPELINE_CONFIG.get("max_search_rounds", MAX_SEARCH_ROUNDS)
    MAX_DEBATE_ROUNDS = PIPELINE_CONFIG.get("max_debate_rounds", MAX_DEBATE_ROUNDS)


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
    """把 .state 渲染成一行状态文本。

    不画进度条：max_iterations/max_revisions 是预算上限而非预期终点，
    拿它当进度条分母是误导。轮次只作事实信息附在阶段后。
    """
    stage = state.get("stage", "?")
    iteration = state.get("iteration")
    verdict = state.get("last_verdict")
    nxt = state.get("next")
    elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    head = f"[{elapsed}] Orchestrator · {PIPELINE} {stage}"
    if iteration:
        head += f" 第 {iteration} 轮"
    segs = []
    if verdict and verdict != "-":
        segs.append(f"{VERDICT_ICON.get(verdict, '')} {verdict}".strip())
    if nxt:
        segs.append(f"→ {nxt}")
    segs.extend(progress)
    return " ".join([head] + segs)


# ---------------------------------------------------------------------------
# 控制台渲染：主体是一条条进度事件，每行带主语（谁干了什么）。
# 每个 Bash/tool call（含 spawn 脚本）都计入进度、各占一行；模型的 [text]
# 独白不上屏（只进日志文件）。行格式统一为 `[HH:MM:SS] <主语> · <动作>`。
# 任务文件（调度脚本）要求作者在标题后写 `说明：<一句话>`，
# spawn 时由 read_task_note 提取并附在该行末尾。
# ---------------------------------------------------------------------------

SPAWN_CMD_RE = re.compile(r"spawn\.py\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)")
TASK_NOTE_RE = re.compile(r"^\s*说明[:：]\s*(.+)\s*$", re.MULTILINE)


def read_task_note(workspace_abs, task_ref):
    """从任务文件中提取 `说明：` 一行（任务书写者的目的声明）。找不到返回 ""。"""
    if not task_ref:
        return ""
    base = os.path.basename(task_ref)
    candidates = [
        os.path.join(workspace_abs, task_ref),
        os.path.join(workspace_abs, task_ref + ".md"),
        os.path.join(workspace_abs, TASKS_DIR, base),
        os.path.join(workspace_abs, TASKS_DIR, base + ".md"),
    ]
    for path in candidates:
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                head = f.read(4096)
        except OSError:
            continue
        m = TASK_NOTE_RE.search(head)
        if m:
            note = m.group(1).strip()
            return note[:80] + ("…" if len(note) > 80 else "")
    return ""


def _short_path(path, workspace_abs):
    """路径相对工作区显示（控制台上不出现冗长绝对路径）。"""
    if not path:
        return ""
    if workspace_abs and path.startswith(workspace_abs):
        path = path[len(workspace_abs):].lstrip("/")
    return path


def role_model(role):
    """角色 → 所用模型名（剥掉 Planner_1 之类并行编号，查 agent_models）。"""
    base = re.sub(r"_\d+$", "", role)
    return AGENT_MODELS.get(base) or AGENT_MODELS.get(role) or MODEL


def _tool_use_name_input(event):
    """从 assistant 事件里提取第一个 tool_use 块的名称与输入。"""
    try:
        for block in event.get("message", {}).get("content", []):
            if block.get("type") == "tool_use":
                return block.get("name", ""), (block.get("input") or {})
    except (AttributeError, TypeError):
        pass
    return "", {}


def console_log(workspace_abs, text):
    """控制台行同步到 {workspace}/console.log——工作区根目录，用户随时可看运行活动。"""
    if not workspace_abs or not text:
        return
    try:
        with open(os.path.join(workspace_abs, "console.log"), "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%m-%d %H:%M:%S')}] {text}\n")
    except OSError:
        pass


def render_tool_lines(name, inp, workspace_abs):
    """把一个 tool_use 事件渲染成控制台行：**只保留 sub-Agent 的派活事件**。

    监控焦点在 sub-Agent 层：Orchestrator 自己的调度动作（读写/轮询/写任务
    文件）一律不上屏（全量记录仍在 .orchestrator.log）；sub-Agent 内部的
    活动（脚本创建、真正的计算命令）由 spawn.py 直接以带路线颜色的行上屏。
    """
    if name == "Bash":
        cmd = (inp.get("command") or "").strip()
        lines = []
        for role, _ws, _prompt, task in SPAWN_CMD_RE.findall(cmd):
            note = read_task_note(workspace_abs, task)
            action = f"开始 ({_short_path(task, workspace_abs)})"
            if note:
                action += f"：{note}"
            lines.append((f"{role}（{role_model(role)}）", action))
        return lines
    return []


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
        # 专家团主脑流水线：审题/发散/深挖/共识由专家团循环承担，无 Planner 主脑；
        # planner 基础版仅用于阶段 3 Final Evaluator 的子问题增援（Ephemeral Standard 三连）。
        agents_dict = {
            "theorist": read_agent("theorist"),
            "computationalist": read_agent("computationalist"),
            "experimentalist": read_agent("experimentalist"),
            "critic": read_agent("critic"),
            "secretary": read_agent("secretary"),
            "planner": read_agent("planner"),
            "verifier": read_agent("verifier"),
            "builder": read_agent("builder"),
            "evaluator": read_agent("evaluator"),
        }
    elif PIPELINE == "auto":
        # 自适应结构流水线：Assessor 评难度 → Orchestrator 自组蓝图（阶段库拼装）
        # → 按蓝图逐阶段派活。需要全部角色可供编排。
        agents_dict = {
            "assessor": read_agent("assessor"),
            "planner": read_agent("planner"),
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
    prompt = prompt.replace("{max_verify_rounds}", str(MAX_VERIFY_ROUNDS))
    prompt = prompt.replace("{max_subtasks}", str(MAX_SUBTASKS))
    prompt = prompt.replace("{max_concurrent_agents}", str(MAX_CONCURRENT_AGENTS))
    prompt = prompt.replace("{max_phases}", str(MAX_PHASES))
    prompt = prompt.replace("{max_spawns}", str(MAX_SPAWNS))
    prompt = prompt.replace("{max_escalations}", str(MAX_ESCALATIONS))
    prompt = prompt.replace("{max_search_rounds}", str(MAX_SEARCH_ROUNDS))
    prompt = prompt.replace("{max_debate_rounds}", str(MAX_DEBATE_ROUNDS))
    prompt = prompt.replace("{max_disputes}", str(MAX_DISPUTES))

    return prompt


RUNTIME_FILE = ".runtime_seconds"


def read_runtime_base(workspace_abs):
    """题目已累计的运行秒数（断点续传时把之前会话的时长带入）。

    只累计 run.py 实际在跑的挂钟时间，会话之间的间隔不计。
    """
    try:
        with open(os.path.join(workspace_abs, DEBUG_DIR, RUNTIME_FILE), encoding="utf-8") as f:
            return max(0.0, float(f.read().strip() or 0))
    except (OSError, ValueError):
        return 0.0


def newest_artifact_mtime(workspace_abs):
    """工作区顶层 + debug/ + tasks/ 中最新文件的 mtime。

    监督者用它判断一次自动续跑是否产生了实际进展（防打转）。
    排除运行框架自己会写的文件——它们的 mtime 更新不代表
    Orchestrator 有实际产出：
    - .orchestrator*：run.py 每次启动都会写的会话/日志
    - console.log：run.py/spawn.py 追加的活动镜像（每次续跑启动必写）
    - .runtime_seconds：监督者计时心跳（每 30s 一次）
    """
    latest = 0.0
    for base in (workspace_abs,
                 os.path.join(workspace_abs, DEBUG_DIR),
                 os.path.join(workspace_abs, TASKS_DIR)):
        try:
            names = os.listdir(base)
        except OSError:
            continue
        for name in names:
            if name.startswith(".orchestrator"):
                continue
            if name == "console.log" or name == RUNTIME_FILE:
                continue
            p = os.path.join(base, name)
            try:
                if os.path.isfile(p):
                    latest = max(latest, os.path.getmtime(p))
            except OSError:
                pass
    return latest


def main():
    global PIPELINE

    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Physics problem solver with multiple pipelines")
    parser.add_argument("workspace", nargs="?", default="problems/001", help="Problem workspace directory")
    parser.add_argument("--pipeline", choices=["standard", "parallel", "iterative", "debate", "tree_search", "adaptive", "deep_search", "auto"],
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

    # 绝对路径，避免 cwd 歧义
    workspace_abs = os.path.abspath(workspace)
    sess_path = os.path.join(workspace_abs, DEBUG_DIR, ".orchestrator_session")

    # Orchestrator 的 system prompt 走文件（--append-system-prompt-file）而非
    # --agents argv：deep_search 组装后 ~130KB（UTF-8），超过 Linux 单参数
    # 128KB 上限（E2BIG）。文件同时留在 debug/ 作审计记录。
    prompt_file = os.path.join(workspace_abs, DEBUG_DIR, ".orchestrator_prompt.md")
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(orchestrator_prompt)

    def build_cmd(user_prompt, resume_sid=None):
        cmd = [
            "claude",
            "--print",
            "--output-format", "stream-json",
            "--verbose",
            "--permission-mode", "bypassPermissions",
            "--append-system-prompt-file", prompt_file,
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
    # 运行时文件按派活隔离：spawn.py 据此把 .result/.log/.session/.progress/.metrics
    # 命名为 .{Role}_{任务名}.* —— 同角色并行派活互不覆盖（在途旧会话的
    # Orchestrator 进程没有此变量，其派活仍走按角色的旧命名，互不干扰）。
    orch_env["SPAWN_RUNTIME_BY_TASK"] = "1"

    fresh_prompt = (
        f"请解决 {workspace_abs} 中的物理题目。\n"
        f"按照你的 system prompt 中的流程执行。\n"
        f"核心纪律：你不读题目、不做计算 — 只调度 sub-Agent，只读它们的 .result 汇报。\n"
        f"开始前先 cat {workspace_abs}/debug/.state 确认是否有断点（旧布局可能在 {workspace_abs}/.state）；没有则从第一阶段开始。\n"
        f"创建 sub-Agent：Bash 调用 python3 {SCRIPTS_DIR}/spawn.py <Role> {workspace_abs} <prompt_file> <task_file>\n"
        f"spawn.py 必须始终用上面的绝对路径调用——不要 cd 出工作区，也不要用相对路径（相对路径解析进工作区，找不到脚本）。\n"
        f"运行时文件按派活隔离：派 <Role> 执行 <任务名> 时，汇报写入 debug/.<Role>_<任务名>.result"
        f"（.log/.session/.progress/.metrics 同此后缀）；轮询与读取时按你派活用的任务名拼出文件名。"
        f"每次派活的运行时文件互不冲突，同一角色可以多路并行。\n"
        f"会话生命周期：输出不含工具调用的纯文本会立即终止会话——等待 sub-Agent 时必须按"
        f"系统提示「并行 spawn 与轮询等待」节轮询，每次回应都带 Bash 工具调用。\n"
        f"全部阶段完成后，将最终结果写入 {workspace_abs}/final_summary.md。\n"
        f"Workspace（绝对路径）: {workspace_abs}；你的 shell cwd 就是该工作区，文件操作请一律用上面的绝对路径。"
    )
    resume_prompt_text = (
        f"断点续传：上次会话被中断。请先 cat {workspace_abs}/debug/.state 恢复进度，然后从中断处继续编排。\n"
        f"核心纪律不变：你不读题目、不做计算 — 只调度 sub-Agent，只读它们的 .result 汇报。\n"
        f"创建 sub-Agent：Bash 调用 python3 {SCRIPTS_DIR}/spawn.py <Role> {workspace_abs} <prompt_file> <task_file>\n"
        f"spawn.py 必须始终用上面的绝对路径调用——不要 cd 出工作区，也不要用相对路径（相对路径解析进工作区，找不到脚本）。\n"
        f"运行时文件命名（重要，可能与你会话记忆中的旧命名不同）：新派活一律按派活隔离——"
        f"派 <Role> 执行 <任务名> 的汇报在 debug/.<Role>_<任务名>.result"
        f"（.log/.session/.progress/.metrics 同此后缀）；轮询与读取按任务名拼文件名。"
        f"同一角色可以多路并行。此前会话遗留的无任务名后缀旧文件（如 .Builder.result）视为已消费的历史记录，不再据此派活。\n"
        f"会话生命周期：输出不含工具调用的纯文本会立即终止会话——等待 sub-Agent 时必须按"
        f"系统提示「并行 spawn 与轮询等待」节轮询，每次回应都带 Bash 工具调用。\n"
        f"Workspace（绝对路径）: {workspace_abs}"
    )
    auto_continue_prompt = (
        f"自动续跑（{PIPELINE} 流水线未完成）：你上一回合提前结束了。切记纪律：**输出不含工具调用的纯文本会立刻终止会话**，"
        f"等待 sub-Agent 期间的每一步回应都必须是 Bash 工具调用。\n"
        f"1. cat {workspace_abs}/debug/.state 恢复进度；\n"
        f"2. 若中断时有 sub-Agent 在跑：后台 spawn 进程可能已随上轮会话死亡。以 .result 存在与否为准——"
        f"spawn.py 派活时会删除旧 .result，故「文件存在」即「该次派活已完成」；缺失 = 重新派活（同一任务文件，中断的可加 --resume）；\n"
        f"3. 按系统提示协议继续后续流程；需要等待 sub-Agent 时用「并行 spawn 与轮询等待」节的轮询模式。\n"
        f"运行时文件按派活隔离：汇报在 debug/.<Role>_<任务名>.result（.log/.session/.progress/.metrics 同此后缀），"
        f"轮询与读取按你派活用的任务名拼文件名；同一角色可多路并行。\n"
        f"核心纪律不变：你不读题目、不做计算 — 只调度 sub-Agent，只读它们的 .result 汇报。"
    )

    resume_sid = resume_session_id(workspace)

    # Stream output to terminal and log file
    log_path = os.path.join(workspace, DEBUG_DIR, ".orchestrator.log")
    start_time = time.time()

    # 题目累计总运行时长：续传读入以往累计基数，新运行清零。
    # 进度行的 [HH:MM:SS] 即此累计值（断点前的时间也计入）。
    runtime_base = read_runtime_base(workspace_abs) if resume_sid else 0.0
    runtime_file = os.path.join(workspace_abs, DEBUG_DIR, RUNTIME_FILE)
    try:
        with open(runtime_file, "w", encoding="utf-8") as rf:
            rf.write(f"{runtime_base:.0f}")
    except OSError:
        pass
    display_start = start_time - runtime_base

    with open(log_path, "a", encoding="utf-8") as log_file:
        mode_desc = f"resume={resume_sid[:8]}" if resume_sid else "fresh"
        print(f"[Orchestrator] pipeline={PIPELINE}, {mode_desc}, started at {time.strftime('%H:%M:%S')}", flush=True)
        console_log(workspace_abs, f"Orchestrator 启动 · pipeline={PIPELINE} · {mode_desc}")
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
                        # 控制台：每个 tool call（含 spawn 脚本）都是一条进度事件，
                        # 行格式 `[HH:MM:SS] <主语> · <动作>`；[text]/[thinking] 独白
                        # 不上屏；日志文件保留全量记录。
                        ts = time.strftime("%H:%M:%S")
                        if etype == "tool_use":
                            tname, tinp = _tool_use_name_input(event)
                            for subject, action in render_tool_lines(tname, tinp, workspace_abs):
                                print(f"[{ts}] {subject} · {action}", flush=True)
                                console_log(workspace_abs, f"{subject} · {action}")
                        elif etype == "init":
                            print(f"[{ts}] Orchestrator · 会话开始 {summary}", flush=True)
                            console_log(workspace_abs, f"Orchestrator · 会话开始 {summary}")
                        elif etype == "result":
                            print(f"[{ts}] Orchestrator · 会话结束 {summary}", flush=True)
                            console_log(workspace_abs, f"Orchestrator · 会话结束 {summary}")
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
                console_log(workspace_abs, f"Orchestrator 超时（{TIMEOUT}s），监督者将续跑")
                kill_process_group(proc)
                progress_stop.set()
                sys.exit(1)

            # 已拿到结果：给进程一小段宽限期自行退出。
            # 不杀未退出的进程组：若会话早退而后台 sub-Agent 仍在健康运行，
            # 杀掉会浪费已完成的工作——监督者续跑后按 .result 存在与否接管
            # （spawn.py 派活时清陈旧 .result，缺失即重派），无需在此清理。
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                print("[Orchestrator] 产出结果后 15s 未退出——保留进程组，由监督者续跑接管")

            return result_event

        # 进度显示：每 5 秒轮询 .state（优先 debug/.state），变化时打印进度条（另每 5 分钟心跳）
        progress_stop = threading.Event()

        def progress_monitor():
            last_key = None
            last_print = 0.0
            last_save = 0.0
            while not progress_stop.wait(5):
                now = time.time()
                # 定期回写累计时长：进程被杀/断电也不丢超过 30s 的账
                try:
                    if now - last_save >= 30:
                        with open(runtime_file, "w", encoding="utf-8") as rf:
                            rf.write(f"{runtime_base + now - start_time:.0f}")
                        last_save = now
                except OSError:
                    pass
                try:
                    st = parse_state_file(find_state_file(workspace))
                    if not st:
                        continue
                    key = json.dumps(st, sort_keys=True)
                    if key != last_key or now - last_print >= 300:
                        line = render_progress(st, display_start, read_progress_lines(workspace))
                        print(line, flush=True)
                        console_log(workspace_abs, line)
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

        # --- 监督者自动续跑 ---
        # --print 模式下 Orchestrator 一旦输出纯文本（无工具调用）会话立即终止；
        # 若此时 sub-Agent 尚未跑完，流水线就停在半路。完成的事实判据是
        # final_summary.md 已写——未写即未完成，自动 --resume 同一会话续跑。
        # 配合提示词中的轮询等待协议，这是兜底层：正常情况不应触发。
        summary_path = os.path.join(workspace_abs, "final_summary.md")
        resumes = 0
        fast_fails = 0
        while not os.path.exists(summary_path):
            if result_event is None and resumes == 0:
                print("[Orchestrator] error: no result event received")
                sys.exit(1)
            if resumes >= MAX_AUTO_RESUMES:
                print(f"[Orchestrator] 自动续跑已达上限（{MAX_AUTO_RESUMES} 次），流水线仍未完成——中止")
                break
            if result_event and result_event.get("is_error"):
                print(f"[Orchestrator] 会话级错误（稍后续跑）：{str(result_event.get('result', 'Unknown'))[:200]}")
                time.sleep(15)
            resumes += 1
            try:
                with open(sess_path, encoding="utf-8") as sf:
                    sid = sf.read().strip()
            except OSError:
                sid = ""
            if not sid:
                print("[Orchestrator] 无可续接的会话 id——中止")
                break
            print(f"[Orchestrator] 会话结束但流水线未完成——自动续跑 {resumes}/{MAX_AUTO_RESUMES}（session {sid[:8]}）")
            console_log(workspace_abs, f"会话结束但流水线未完成——自动续跑 {resumes}/{MAX_AUTO_RESUMES}")
            log_file.write(f"[auto-resume] #{resumes} | {time.strftime('%H:%M:%S')}\n")
            log_file.flush()
            before = newest_artifact_mtime(workspace_abs)
            t0 = time.time()
            result_event = launch(build_cmd(auto_continue_prompt, sid))
            # 打转保护：<60s 结束且零新产出，连续 3 次则中止
            noop = (time.time() - t0) < 60 and newest_artifact_mtime(workspace_abs) <= before
            fast_fails = fast_fails + 1 if noop else 0
            if fast_fails >= 3:
                print("[Orchestrator] 连续 3 次续跑零产出（<60s 且无新文件）——中止以防打转")
                break

        progress_stop.set()
        progress_thread.join(timeout=5)
        elapsed = time.time() - start_time
        total_elapsed = runtime_base + elapsed
        try:
            with open(runtime_file, "w", encoding="utf-8") as rf:
                rf.write(f"{total_elapsed:.0f}")
        except OSError:
            pass

        log_file.write(f"[done] Orchestrator | pipeline={PIPELINE} | {time.strftime('%H:%M:%S')} | "
                       f"session={elapsed:.1f}s total={total_elapsed:.1f}s resumes={resumes}\n")

    print(f"\n[Orchestrator] done（本次会话 {elapsed:.0f}s，题目累计 {total_elapsed:.0f}s）")
    console_log(workspace_abs, f"运行结束（本次会话 {elapsed:.0f}s，题目累计 {total_elapsed:.0f}s，续跑 {resumes} 次）")

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
