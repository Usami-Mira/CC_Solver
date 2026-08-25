# Project Configuration

## CRITICAL: Directory Structure and Working Directory

**Project Root**: `/home/usamimira/PHY-LLM/CC_Solver`

**Bash tool default working directory**: `/home/usamimira/PHY-LLM/CC_Solver`

**IMPORTANT**: RAG scripts MUST run from `textbook/` subdirectory. Always use subshell with `cd`:
```bash
(source rag_env/bin/activate && python3 rag_build/embed_bge.py)
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

**Key Rule**: When running RAG scripts, the working directory MUST be `textbook/`. Use subshell:
```bash
(source rag_env/bin/activate && python3 rag_build/<script>.py)
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

## LaTeX Requirement

All physics formulas must use LaTeX inline math (`$...$`), not Unicode symbols:
- ✅ Correct: `$F = ma$`, `$E_k = \frac{1}{2}mv^2$`
- ❌ Wrong: `F = ma`, `Ek = ½mv²`

## Common Pitfalls

1. **Virtual environment path**: Always use absolute path `/home/usamimira/PHY-LLM/CC_Solver/textbook/rag_env/bin/activate`
2. **Working directory**: RAG scripts expect to run from `textbook/` directory
3. **BGEM3FlagModel parameter**: `devices=` not `device=`
4. **Template variables**: Use `.replace()` not `.format()` to preserve runtime placeholders like `{workspace}`
5. **HuggingFace downloads**: Must set `HF_ENDPOINT` and `HF_HUB_DISABLE_XET=1` for China mirror
6. **Script paths**: Run scripts from project root, e.g., `python3 scripts/run.py`, not `python3 run.py`
