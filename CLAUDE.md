# Project Configuration

## Setup

首次使用或依赖变更时，运行：
```bash
bash setup.sh            # 完整配置（pip 安装，首次较慢）
bash setup.sh --quick    # 跳过 pip/RAG，只验证配置与防偷看机制
```

一键完成：先决条件检查（python3/git，claude CLI 缺失时自动尝试 `npm install -g`）、
git 身份（`user.name`/`user.email` 缺失时提示配置，消除每次提交的身份告警）、
API 配置（环境变量中已有则持久化到 `.env`，否则交互提示；`.env` 权限 600、已入
`.gitignore`，`scripts/load_env.py` 在 run.py/spawn.py 启动时自动载入，已有环境变量优先）、
`textbook/rag_env` 虚拟环境与依赖、path_guard 防偷看自检（工作区外访问必须被
exit(2) 硬拦截）、记忆目录状态、回归测试。任何一项失败会以非零码退出并标 ✗。

## CRITICAL: Directory Structure and Working Directory

**Project Root**: 本仓库根目录（即包含此 CLAUDE.md 的目录）。下文相对路径均相对于项目根；代码内部一律用运行时推导的路径（`Path(__file__).parent` 等），不写死绝对路径。

**Bash tool default working directory**: 项目根目录

**IMPORTANT**: RAG 查询使用 `textbook/rag_env/bin/python` 直接调用，**不要** source activate：
```bash
cd textbook && rag_env/bin/python rag_build/query_rag.py "your query"
```

### Directory Layout
```
<project-root>/                              ← Project root (Bash default cwd)
├── config.json                            ← Agent configuration
├── setup.sh                               ← 一键配置（git 身份 + claude CLI + API key + 依赖 + 防偷看自检 + 回归测试）
├── CLAUDE.md                              ← Project instructions
├── README.md, PROJECT_STRUCTURE.md        ← Documentation
├── scripts/                               ← 脚本目录
│   ├── run.py                             ← 入口脚本：组装 Orchestrator prompt
│   ├── spawn.py                           ← 子进程辅助：创建 sub-agent（含逐阶段 Git 快照、--resume 断点续传）
│   ├── path_guard.py                      ← PreToolUse hook：硬拦截 workspace 外的文件访问
│   ├── memory_guard.py                    ← 记忆防火墙：用 git 隔离/审计记忆目录
│   ├── load_env.py                        ← 自动载入项目根 .env（setup.sh 写入的 API 配置）
│   ├── stream_parser.py                   ← 流式输出解析器
│   ├── statusline.py                      ← Claude Code 状态栏：实时显示 pipeline 进度
│   ├── test_git_integration.py            ← Git 集成单元测试
│   ├── test_path_guard.py                 ← path_guard 单元测试
│   └── test_hang_kill.py                  ← 进程挂起防护回归测试
├── prompts/                               ← Agent system prompts
│   ├── orchestrator.md                    ← 通用 Orchestrator prompt
│   ├── agents/                            ← 各 Agent 定义
│   │   ├── planner.md, planner_deep.md, builder.md, evaluator.md, verifier.md
│   │   ├── meta_planner.md, explorer.md, secretary.md
│   │   └── theorist.md, computationalist.md, experimentalist.md, critic.md
│   ├── pipelines/                         ← 各 Pipeline 配置
│   │   └── standard.md, parallel.md, iterative.md, debate.md, tree_search.md, adaptive.md, deep_search.md
│   └── skills/                            ← Skill definitions
├── problems/                              ← Problem workspaces (e.g., CPhO42j/)
└── textbook/                              ← RAG knowledge base (SEPARATE WORKING DIR)
    ├── rag_env/                           ← Python virtual environment
    │   └── bin/activate                   ← Activate script
    ├── rag_build/                         ← RAG scripts (run from textbook/)
    │   ├── embed_bge.py                   ← Embedding generation
    │   └── query_rag.py                   ← RAG query tool
    ├── models/bge-m3/                     ← BGE-M3 model files
    ├── weaviate_data/                     ← Weaviate vector database
    ├── merged/                            ← Processed textbook chunks
    └── *_output/                          ← OCR output directories
```

**Key Rule**: RAG 脚本使用 `textbook/rag_env/bin/python` 直接调用：
```bash
cd textbook && rag_env/bin/python rag_build/query_rag.py "查询内容"
```

## Key Paths

所有路径均相对于项目根目录。

- **Models**: `textbook/models/bge-m3` (BGE-M3, 1024-dim, multilingual)
- **Weaviate data**: `textbook/weaviate_data`
- **RAG scripts**: `textbook/rag_build/`
  - `embed_bge.py` — Generate embeddings and store in Weaviate
  - `query_rag.py` — Query the physics textbook knowledge base
- **Merged chunks**: `textbook/merged/chunks_translated.json` (1139 chunks)

## Environment Variables

When running RAG scripts, set these (or `scripts/run.py` sets them automatically). 在项目根目录下：
```bash
export RAG_MODEL_DIR="$(pwd)/textbook/models/bge-m3"
export RAG_DATA_DIR="$(pwd)/textbook/weaviate_data"
```

For HuggingFace downloads (user in China):
```bash
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DISABLE_XET=1
```

## BGE-M3 Model Notes

- **Dimensions**: 1024 (not 768 like BGE-base)
- **Multilingual**: Handles Chinese natively, no translation needed
- **Max tokens**: 8192
- **FlagEmbedding parameter**: Use `devices=` (plural), NOT `device=`
- **Load on GPU**: `BGEM3FlagModel(path, use_fp16=True, devices="cuda")`

## Agent Workflow

系统支持 7 种 Pipeline（在 `config.json` 中配置）：

- **Standard**: Planner → Builder → Evaluator → (REVISE 循环)
- **Parallel**: N×Planner 并行 → Meta-Planner → Builder → Evaluator
- **Iterative**: Explorer → Builder → Evaluator → 循环迭代
- **Debate**: 专家分析 → 辩论循环 → Secretary 写 Plan → Builder → Evaluator
- **Tree Search**: Planner 展开搜索树（≥2 个结构不同分支，各含机器可检验收判据）→ Ephemeral Builder-Evaluator 逐支验证 → best-first 选择 + 死端回溯 → Verifier 审查方案 → Final Builder → Evaluator
- **Adaptive**: Planner 自适应决策 → Ephemeral Builder-Evaluator → 动态调整 → Verifier 审查方案 → Final Builder → Evaluator
- **Deep Search**: 审题找 crux → 发散生成 ≥3 个结构不同方向（各含验收判据 + 预测撞墙点）→ best-first 深挖 + 死端回溯 → 多专家辩论共识（思想碰撞提出创新点，可动议临时 Builder/Evaluator 解决分歧，Secretary 记录共识）→ Verifier 审查方案 → Final Builder → Evaluator。Planner 用专用版 `agents/planner_deep.md`（解除"一种方法"限制）；集其余结构之大成，难题默认

Orchestrator 负责编排，通过 `scripts/spawn.py` 创建 sub-agent（每次 spawn 前后自动 git 快照）。

Evaluator 给出 REVISE 时先走**修订争议协议**：Builder 逐条 ACCEPT/REBUT（`rebuttal_{n}.md`）→ 有 REBUT 则 Evaluator 复审（`rejoin_{n}.md`，维持意见必须附新的独立证据）→ 达成共识或达 `max_disputes` 上限后才真正修订（达上限后强制修订，争议点单独标注）。

## Orchestrator 信息管制（重要设计原则）

Orchestrator **只调度、不解题、不读题**。为防止上下文膨胀导致中断：

- **禁止读**：`problem.md`、`strategy.md`、`calculation_*.md`、`solution.md`、`verification_*.md`/`review.md`（除第一行）、`rebuttal_*`/`rejoin_*`（除第一行）、`debug/*.log`、`~/.claude/` 下的记忆与会话文件
- **禁止做**：运行 `python3`、写脚本、做拟合、自己写含物理内容的任务文件
- **只读**：`debug/.{Role}.result`（sub-agent 简短汇报）、`debug/.state`、`debug/.*.progress`、裁决文件的**第一行**（`head -1`）
- **通信通路**：每个 sub-agent 的最终消息被写入 `debug/.{Role}.result`，格式固定为 `HANDOFF` + `STATUS/VERDICT` + `OUTPUT` + `SUMMARY`（≤6 行）
- **断点续传**：所有决策信息写进 `debug/.state`（key: value，auto-compact 后可恢复）；会话 ID 存 `debug/.orchestrator_session` / `debug/.{Role}.session`，超时/中断后自动 `claude --resume` 续接原会话
- **Workspace 布局**：`debug/`（状态/日志/汇报）、`tasks/`（所有任务文件）、`scripts/{builder,evaluator,verifier}/<任务名>/`（各角色脚本互相隔离，Evaluator 从 problem.md 独立转录、只审计不运行 Builder 的脚本）
- 验证任务文件 `tasks/task_{id}.md`（含物理细节）由 **Planner** 撰写；Orchestrator 只写不含物理内容的样板调度指令
- **Git 快照在代码层自动完成**：`spawn.py` 每次 spawn 前后各提交一次（文件锁互斥，并行安全），Orchestrator 无需手动 commit
- **记忆防火墙 + 路径封锁**：会话**不再用 `--bare`**（它会把 hooks 一并跳过，使封锁失效）。防"前世记忆"与偷看由两层保证：① `scripts/path_guard.py`（PreToolUse hook，由 `run.py` 写入每个工作区的 `.claude/settings.json`，`WORKSPACE` 环境变量激活）用 exit(2) 硬拦截 workspace 外的一切文件访问（Read/Write/Edit/Glob/Grep/Bash 全覆盖，symlink 按 realpath 解析、禁止嵌套启动 `claude`），审计写入 `debug/.path_guard.log`；② `scripts/memory_guard.py`（config: `memory_guard`，默认 `quarantine`）——Orchestrator 与 sub-agent 均以 workspace 为 cwd 运行，其 auto-memory 只落在**工作区专属记忆目录**（`~/.claude/projects/<workspace-slug>/memory/`）；pre_run 清空该目录、post_run 捕获期间写入并恢复基线。**主项目记忆目录（用户交互式会话所用）全程不触碰**，运行期间照常读写。审计写入 `debug/.memory_audit` 并附入 final_summary.md

## LaTeX Requirement

All physics formulas must use LaTeX inline math (`$...$`), not Unicode symbols:
- ✅ Correct: `$F = ma$`, `$E_k = \frac{1}{2}mv^2$`
- ❌ Wrong: `F = ma`, `Ek = ½mv²`

## Common Pitfalls

1. **RAG 调用方式**：使用 `textbook/rag_env/bin/python` 直接调用，不要 source activate
2. **Working directory**: RAG 脚本从 `textbook/` 目录运行
3. **BGEM3FlagModel parameter**: `devices=` not `device=`
4. **Template variables**: Use `.replace()` not `.format()` to preserve runtime placeholders like `{workspace}`
5. **HuggingFace downloads**: Must set `HF_ENDPOINT` and `HF_HUB_DISABLE_XET=1` for China mirror
6. **Script paths**: Run scripts from project root, e.g., `python3 scripts/run.py`, not `python3 run.py`
7. **Evaluator 必须检查代码**：Evaluator 必须先审计 Builder 的 scripts/ 目录（只读，不运行、不采信其输出），然后从 problem.md 独立转录做自己的验证；数值结果与已证明的结构性质矛盾时，优先怀疑自己的脚本
8. **Workspace 布局**：状态/日志/汇报在 `debug/`，任务文件在 `tasks/`，脚本在 `scripts/<角色>/<任务名>/`；旧版布局的工作区在下次运行时自动迁移（`ensure_workspace_layout` 每次运行都会重写 .gitignore）
9. **记忆隔离与路径封锁**：不再用 `--bare`（它会禁用 hooks）。防偷看靠 `path_guard.py`（PreToolUse hook，`WORKSPACE` 环境变量激活，exit(2) 硬拦截 + `debug/.path_guard.log` 审计）；记忆隔离靠 `memory_guard` 运行期清空**工作区专属**记忆目录、运行后恢复基线——主项目记忆目录（交互式会话）不受影响
