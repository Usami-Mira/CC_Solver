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
├── CLAUDE.md                              ← Project instructions
├── README.md, PROJECT_STRUCTURE.md        ← Documentation
├── scripts/                               ← 脚本目录
│   ├── run.py                             ← 入口脚本：组装 Orchestrator prompt
│   ├── spawn.py                           ← 子进程辅助：创建 sub-agent
│   ├── stream_parser.py                   ← 流式输出解析器
│   └── test_git_integration.py            ← Git 集成单元测试
├── prompts/                               ← Agent system prompts
│   ├── orchestrator.md                    ← 通用 Orchestrator prompt
│   ├── agents/                            ← 各 Agent 定义
│   │   ├── planner.md, builder.md, evaluator.md
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
- **Tree Search**: Planner 决策 → Ephemeral Builder-Evaluator → Final Builder → Evaluator
- **Adaptive**: Planner 自适应决策 → Ephemeral Builder-Evaluator → 动态调整 → Final Builder → Evaluator

Orchestrator 负责编排，通过 `scripts/spawn.py` 创建 sub-agent。

## Orchestrator 信息管制（重要设计原则）

Orchestrator **只调度、不解题、不读题**。为防止上下文膨胀导致中断：

- **禁止读**：`problem.md`、`strategy.md`、`calculation_*.md`、`solution.md`、`verification_*.md`/`review.md`（除第一行）、`.*.log`
- **禁止做**：运行 `python3`、写脚本、做拟合、自己写含物理内容的任务文件
- **只读**：`.{Role}.result`（sub-agent 简短汇报）、`.state`、裁决文件的**第一行**（`head -1`）
- **通信通路**：每个 sub-agent 的最终消息被写入 `.{Role}.result`，格式固定为 `HANDOFF` + `STATUS/VERDICT` + `OUTPUT` + `SUMMARY`（≤5 行）
- **断点续传**：所有决策信息写进 `.state`（auto-compact 后可恢复）
- 验证任务文件 `task_{id}.md`（含物理细节）由 **Planner** 撰写；Orchestrator 只写不含物理内容的样板调度指令

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
7. **Evaluator 必须检查代码**：Evaluator 必须先读取 Builder 的 scripts/ 目录，审查代码逻辑，然后才做独立验证
