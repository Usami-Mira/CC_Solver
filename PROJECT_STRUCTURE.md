# 项目结构与开发指南

本文档帮助 coding agent 快速理解项目结构、核心组件和常见操作。

## 核心文件速查

| 文件 | 用途 | 修改频率 |
|------|------|----------|
| `scripts/run.py` | 入口脚本，启动 Orchestrator | 低 |
| `scripts/spawn.py` | 子进程辅助，创建 Planner/Builder/Evaluator | 低 |
| `scripts/stream_parser.py` | 流式输出解析器 | 低 |
| `config.json` | 项目配置（模型、超时、并行数） | 低 |
| `prompts/orchestrator.md` | 通用 Orchestrator 系统提示词 | 中 |
| `prompts/agents/*.md` | 各 Agent 系统提示词 | 中 |
| `prompts/pipelines/*.md` | 各 Pipeline 配置 | 中 |
| `prompts/skills/*.md` | Skill 定义（可调用能力） | 中 |

## 目录结构详解

```
CC_Solver/
├── config.json               # 运行时配置
├── CLAUDE.md                 # Claude Code 项目配置
├── README.md                 # 用户文档
├── PROJECT_STRUCTURE.md      # 本文档
│
├── scripts/                  # 脚本目录
│   ├── run.py                #   入口：组装 Orchestrator prompt 并启动
│   ├── spawn.py              #   子进程创建：被 Orchestrator 调用
│   ├── stream_parser.py      #   流式输出解析器
│   └── test_git_integration.py # Git 集成单元测试
│
├── prompts/                  # Agent 定义
│   ├── orchestrator.md       #   通用 Orchestrator prompt（含模板变量）
│   ├── agents/               #   各 Agent 定义
│   │   ├── planner.md
│   │   ├── builder.md
│   │   ├── evaluator.md
│   │   ├── meta_planner.md
│   │   ├── explorer.md
│   │   ├── secretary.md
│   │   ├── theorist.md
│   │   ├── computationalist.md
│   │   ├── experimentalist.md
│   │   └── critic.md
│   ├── pipelines/            #   各 Pipeline 配置
│   │   ├── standard.md
│   │   ├── parallel.md
│   │   ├── iterative.md
│   │   ├── debate.md
│   │   ├── tree_search.md
│   │   └── adaptive.md
│   └── skills/               #   可调用的 Skill
│       ├── calculation.md
│       ├── dimension_check.md
│       └── knowledge_base.md
│
├── problems/                 # 题目工作区（每题一个子目录）
│   └── <exam>/
│       └── <n>/
│           ├── problem.md         # 输入：题目描述
│           ├── plan.md            # Planner 输出
│           ├── solution.md        # Builder 输出
│           ├── review.md          # Evaluator 输出
│           ├── final_summary.md   # 最终汇总
│           ├── .state             # 断点状态
│           ├── .git/              # Git 仓库（自动创建）
│           └── .*.result/metrics  # 内部缓存
│
└── textbook/                 # 教科书 RAG 知识库
    ├── rag_build/            #   RAG 构建脚本
    │   ├── chunk_markdown.py #     文本分块
    │   ├── translate_chunks.py #   中英翻译
    │   └── embed_bge.py      #     向量嵌入
    ├── fix_formulas.py       #   OCR 公式修正
    ├── mcp_server.py         #   MCP 服务器（Cherry Studio 集成）
    ├── weaviate_data/        #   Weaviate 向量数据库
    ├── models/               #   嵌入模型（BGE-M3）
    └── rag_env/              #   Python 虚拟环境
```

## 核心组件交互

```
用户运行: python3 scripts/run.py problems/example
                    │
                    ▼
              ┌─────────────┐
              │   run.py    │
              │  (Bootstrap)│
              └──────┬──────┘
                     │ 1. 初始化 Git 仓库
                     │ 2. 组装 Orchestrator prompt
                     │ 3. 启动 Claude Code CLI
                     ▼
              ┌─────────────┐
              │Orchestrator │
              │ (协调者)     │
              └──────┬──────┘
                     │ 调用 spawn.py
                     ▼
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │ Planner  │ │ Builder  │ │Evaluator │
  │ (规划者)  │ │ (求解者)  │ │ (审查者)  │
  └────┬─────┘ └────┬─────┘ └────┬─────┘
       │            │            │
       │ plan.md    │ solution.md│ review.md
       │            │            │
       └────────────┴────────────┘
                    │
                    ▼
            Git 自动提交每个阶段
```

## 常见开发任务

### 1. 修改 Agent 行为

**场景**：调整 Planner/Builder/Evaluator 的输出格式或策略

**步骤**：
1. 编辑 `prompts/agents/<role>.md`
2. 测试：`python3 scripts/run.py problems/test_simple`
3. 检查输出：`cat problems/test_simple/<role>.md`

**注意**：`orchestrator.md` 中的 `{pipeline_config}` 等占位符会被替换为对应 Pipeline 配置内容。

### 2. 添加新 Skill

**场景**：为 Agent 添加新能力（如"误差分析"）

**步骤**：
1. 创建 `prompts/skills/error_analysis.md`
2. 在对应 Agent prompt 中引用：`参见 Skill: error_analysis`
3. Agent 运行时会自动加载该 Skill

### 3. 修改权限配置

**场景**：调整 sub-Agent 可使用的工具

**位置**：`scripts/spawn.py` 中的 `AGENT_PROFILES` 字典

**示例**：允许 Builder 使用 `git log`：
```python
"Builder": (
    "Read,Write,Edit,"
    "Bash(python3 *),"
    "Bash(git status*),"
    "Bash(git diff*),"
    "Bash(git log*),"  # 添加这行
    "Bash(git add *)"
)
```

### 4. 运行测试

```bash
# 运行所有单元测试
python3 scripts/test_git_integration.py -v
python3 textbook/test_smart_chunk.py -v

# 运行端到端测试（会调用 API）
python3 scripts/run.py problems/test_simple
```

### 5. 调试 Git 提交

**场景**：查看某道题的 Git 历史

```bash
cd problems/example_single
git log --oneline
git show <commit-hash>
git diff HEAD~1 solution.md
```

## 关键配置说明

### config.json

```json
{
  "pipeline": "standard",              // 当前使用的 pipeline
  "max_concurrent_problems": 3,        // 最大并行题目数
  
  "configs": {                         // 各 Pipeline 的独立配置
    "standard": {
      "model": "qwen3.6-plus",         // 使用的模型名
      "timeout_seconds": 600,          // 单次调用超时（秒）
      "max_revisions": 2,              // Builder-Evaluator 循环次数
      "agent_models": {                // 为不同 Agent 配置不同模型
        "Planner": "qwen3.6-plus",
        "Builder": "qwen3.6-plus",
        "Evaluator": "qwen3.6-plus"
      }
    },
    
    "adaptive": {
      "model": "qwen3.6-plus",
      "timeout_seconds": 600,
      "max_iterations": 15,            // 迭代循环最大次数
      "max_revisions": 2,
      "ephemeral_timeout": 300,        // 临时 Builder/Evaluator 超时
      "agent_models": {
        "Planner": "qwen3.6-plus",
        "Builder": "qwen3.6-plus",
        "Evaluator": "qwen3.6-plus"
      }
    }
  }
}
```

### AGENT_PROFILES（scripts/spawn.py）

控制每个 Agent 可使用的工具：
- `Read`, `Write`, `Edit` — 文件操作
- `Bash(python3 *)` — 运行 Python 脚本
- `Bash(git status*)` — Git 只读命令
- `Bash(git add *)` — Git 暂存（但不能 commit）

**禁止的命令**：`git commit`, `git reset`, `git push` 等（由 Orchestrator 统一管理）

## 数据流

```
输入                    处理                     输出
─────                  ────                     ────
problem.md      →     Planner          →     plan.md
                      (分析问题)

problem.md      →     Builder          →     solution.md
plan.md               (执行推导)

problem.md      →     Evaluator        →     review.md
solution.md           (审查验证)
plan.md

review.md       →     Orchestrator     →     判断 PASS/REVISE
                      (决策)

所有文件        →     Git              →     版本历史
                      (自动提交)
```

## 断点续传机制

每道题的 `.state` 文件记录下一个应执行的 Agent：

```
无 .state 文件  → 从 planner 开始
.state = planner → 运行 Planner
.state = builder → 运行 Builder
.state = evaluator → 运行 Evaluator
.state = done   → 跳过（已完成）
```

Agent 成功后才更新 `.state`，失败不更新，确保可随时中断并安全恢复。

## Git 提交约定

Orchestrator 在以下节点自动提交：

| 时机 | 提交消息 |
|------|----------|
| 初始化后 | `init: workspace setup with problem files` |
| 预创建文件后 | `init: create output files` |
| Planner 完成后 | `plan: v1 complete` |
| Builder 完成后 | `solution: v1 complete` 或 `solution: v2 revised` |
| Evaluator 完成后 | `review: v1 complete` 或 `review: v2 revised` |
| 写入汇总后 | `final: summary` |

## 故障排查

### 问题：Agent 卡住或超时

**检查**：
1. `cat problems/<exam>/<n>/.<role>.log` — 查看 Agent 日志
2. `cat problems/<exam>/<n>/.state` — 查看当前阶段
3. `config.json` 中的 `timeout_seconds` — 是否太短

### 问题：Git 提交失败

**检查**：
1. `git --version` — Git 是否安装
2. `git -C problems/<exam>/<n> status` — 工作区状态
3. `.gitignore` — 是否误排除了重要文件

### 问题：权限被拒绝

**检查**：
1. `spawn.py` 中的 `AGENT_PROFILES` — 是否缺少所需工具
2. Claude Code 日志 — 查看具体被拒绝的命令

## 扩展建议

### 添加新 Agent 角色

1. 在 `prompts/agents/` 下创建 `<role>.md`
2. 在 `scripts/spawn.py` 的 `AGENT_PROFILES` 中添加配置
3. 在 `scripts/run.py` 的 `assemble_orchestrator_prompt()` 中添加 agent 读取逻辑
4. 在相关 `prompts/pipelines/*.md` 中引用新 Agent

### 添加新 Pipeline

1. 在 `prompts/pipelines/` 下创建 `<pipeline_name>.md`
2. 在 `config.json` 的 `configs` 中添加对应配置
3. 在 `scripts/run.py` 的 `assemble_orchestrator_prompt()` 中添加 pipeline 处理逻辑
4. 更新 README.md 中的 Pipeline 表格

## 测试覆盖

| 测试文件 | 覆盖范围 | 类型 |
|----------|----------|------|
| `test_git_integration.py` | Git 初始化、权限配置 | 干测试（无 API 调用） |
| `textbook/test_smart_chunk.py` | 文本分块算法 | 干测试 |
| `textbook/test_mcp.py` | MCP 服务器 | 干测试 |

**注意**：目前没有"湿测试"（调用 API 的集成测试）。如需添加，建议放在 `tests/integration/` 目录。
