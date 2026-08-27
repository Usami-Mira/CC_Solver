# Project Configuration

## Setup

首次使用或依赖变更时，运行：
```bash
bash setup.sh
```

这会自动创建 `textbook/rag_env` 虚拟环境并安装所有依赖。

## CRITICAL: Directory Structure and Working Directory

**Project Root**: `/home/usamimira/PHY-LLM/CC_Solver`

**Bash tool default working directory**: `/home/usamimira/PHY-LLM/CC_Solver`

**IMPORTANT**: RAG 查询使用 `textbook/rag_env/bin/python` 直接调用，**不要** source activate：
```bash
cd textbook && rag_env/bin/python rag_build/query_rag.py "your query"
```

### Directory Layout
```
/home/usamimira/PHY-LLM/CC_Solver/         ← Project root (Bash default cwd)
├── config.json                            ← Agent configuration
├── setup.sh                               ← 一键安装（RAG 虚拟环境 + 依赖）
├── CLAUDE.md                              ← Project instructions
├── README.md, PROJECT_STRUCTURE.md        ← Documentation
├── scripts/                               ← 脚本目录
│   ├── run.py                             ← 入口脚本：组装 Orchestrator prompt
│   ├── spawn.py                           ← 子进程辅助：创建 sub-agent（含逐阶段 Git 快照、--resume 断点续传）
│   ├── memory_guard.py                    ← 记忆防火墙：用 git 隔离/审计记忆目录
│   ├── stream_parser.py                   ← 流式输出解析器
│   ├── statusline.py                      ← Claude Code 状态栏：实时显示 pipeline 进度
│   ├── test_git_integration.py            ← Git 集成单元测试
│   └── test_hang_kill.py                  ← 进程挂起防护回归测试
├── prompts/                               ← Agent system prompts
│   ├── orchestrator.md                    ← 通用 Orchestrator prompt
│   ├── agents/                            ← 各 Agent 定义
│   │   ├── planner.md, builder.md, evaluator.md, verifier.md
│   │   ├── meta_planner.md, explorer.md, secretary.md
│   │   └── theorist.md, computationalist.md, experimentalist.md, critic.md
│   ├── pipelines/                         ← 各 Pipeline 配置
│   │   └── standard.md, parallel.md, iterative.md, debate.md, tree_search.md, adaptive.md
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

- **Models**: `/home/usamimira/PHY-LLM/CC_Solver/textbook/models/bge-m3` (BGE-M3, 1024-dim, multilingual)
- **Weaviate data**: `/home/usamimira/PHY-LLM/CC_Solver/textbook/weaviate_data`
- **RAG scripts**: `/home/usamimira/PHY-LLM/CC_Solver/textbook/rag_build/`
  - `embed_bge.py` — Generate embeddings and store in Weaviate
  - `query_rag.py` — Query the physics textbook knowledge base
- **Merged chunks**: `/home/usamimira/PHY-LLM/CC_Solver/textbook/merged/chunks_translated.json` (1139 chunks)

## Environment Variables

When running RAG scripts, set these (or `scripts/run.py` sets them automatically):
```bash
export RAG_MODEL_DIR=/home/usamimira/PHY-LLM/CC_Solver/textbook/models/bge-m3
export RAG_DATA_DIR=/home/usamimira/PHY-LLM/CC_Solver/textbook/weaviate_data
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

系统支持 6 种 Pipeline（在 `config.json` 中配置）：

- **Standard**: Planner → Builder → Evaluator → (REVISE 循环)
- **Parallel**: N×Planner 并行 → Meta-Planner → Builder → Evaluator
- **Iterative**: Explorer → Builder → Evaluator → 循环迭代
- **Debate**: 专家分析 → 辩论循环 → Secretary 写 Plan → Builder → Evaluator
- **Tree Search**: Planner 决策 → Ephemeral Builder-Evaluator → Verifier 审查方案 → Final Builder → Evaluator
- **Adaptive**: Planner 自适应决策 → Ephemeral Builder-Evaluator → 动态调整 → Verifier 审查方案 → Final Builder → Evaluator

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
- **记忆防火墙**：所有会话均 `--bare`（禁用 auto-memory 注入）；`scripts/memory_guard.py`（config: `memory_guard`，默认 `quarantine`）在运行前后用 git 快照隔离 `~/.claude/.../memory/`，审计写入 `debug/.memory_audit` 并附入 final_summary.md

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
9. **记忆隔离**：所有会话用 `--bare`；`memory_guard`（config.json，默认 `quarantine`）用 git 隔离记忆目录，防止"前世记忆"进入解题过程
