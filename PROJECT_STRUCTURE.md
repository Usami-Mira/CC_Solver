# 项目结构与开发指南

本文档帮助 coding agent 快速理解项目结构、核心组件和常见操作。

## 核心文件速查

| 文件 | 用途 | 修改频率 |
|------|------|----------|
| `scripts/run.py` | 入口脚本，启动 Orchestrator（含记忆防火墙前后置、--resume 续跑、工作区 `.claude` hook 注入） | 低 |
| `scripts/spawn.py` | 子进程辅助，创建 sub-agent（含逐阶段 Git 快照、--resume 断点续传、进度文件清理） | 低 |
| `scripts/path_guard.py` | PreToolUse hook：`WORKSPACE` 激活，硬拦截工作区外文件访问（审计入 `debug/.path_guard.log`） | 低 |
| `scripts/memory_guard.py` | 记忆防火墙：运行期清空/运行后恢复工作区专属记忆目录（quarantine/audit/off） | 低 |
| `scripts/stream_parser.py` | 流式输出解析器 | 低 |
| `setup.sh` | 一键配置：git 身份 + claude CLI + API key（.env）+ 依赖 + path_guard 自检 + 回归测试（`--quick` 跳过 pip/RAG） | 低 |
| `config.json` | 项目配置（模型、超时、并行数） | 低 |
| `prompts/orchestrator.md` | 通用 Orchestrator 系统提示词 | 中 |
| `prompts/agents/*.md` | 各 Agent 系统提示词 | 中 |
| `prompts/pipelines/*.md` | 各 Pipeline 配置 | 中 |
| `prompts/skills/*.md` | Skill 定义（可调用能力） | 中 |

## 目录结构详解

```
CC_Solver/
├── config.json               # 运行时配置
├── setup.sh                  # 一键配置（git 身份 + claude CLI + API key + 依赖 + 防偷看自检 + 回归测试）
├── CLAUDE.md                 # Claude Code 项目配置
├── README.md                 # 用户文档
├── PROJECT_STRUCTURE.md      # 本文档
│
├── scripts/                  # 脚本目录
│   ├── run.py                #   入口：组装 Orchestrator prompt 并启动（注入 .claude hook 配置）
│   ├── spawn.py              #   子进程创建：被 Orchestrator 调用（自动 git 快照 + --resume）
│   ├── path_guard.py         #   PreToolUse hook：硬拦截工作区外文件访问
│   ├── memory_guard.py       #   记忆防火墙：运行期清空/运行后恢复工作区专属记忆目录
│   ├── load_env.py           #   自动载入项目根 .env（setup.sh 写入的 API 配置）
│   ├── stream_parser.py      #   流式输出解析器
│   ├── statusline.py         #   Claude Code 状态栏（显示 pipeline 实时进度 + Agent 进度条）
│   ├── test_git_integration.py # Git 集成单元测试
│   ├── test_path_guard.py    #   path_guard（防偷看）单元测试
│   └── test_hang_kill.py     #   进程挂起防护回归测试
│
├── prompts/                  # Agent 定义
│   ├── orchestrator.md       #   通用 Orchestrator prompt（含模板变量）
│   ├── agents/               #   各 Agent 定义
│   │   ├── planner.md
│   │   ├── builder.md
│   │   ├── evaluator.md
│   │   ├── verifier.md
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
│           ├── final_summary.md   # 最终汇总（含记忆审计段落）
│           ├── tasks/             # 任务文件（task_*.md、rebuttal/rejoin 任务）
│           ├── scripts/           # 按角色隔离的脚本：
│           │   ├── builder/<任务名>/    #   Builder 的计算脚本
│           │   ├── evaluator/<任务名>/  #   Evaluator 的独立验证脚本（从 problem.md 重新转录）
│           │   └── verifier/            #   Verifier 的抽查脚本
│           ├── debug/             # 内部状态目录：
│           │   ├── .state         #   断点状态（key: value）
│           │   ├── .{role}.result #   HANDOFF 汇报（≤6 行）
│           │   ├── .{role}.metrics#   调用指标
│           │   ├── .{role}.session#   Claude 会话 ID（--resume 用）
│           │   ├── .{role}.progress#  进度条（k/N: 摘要）
│           │   ├── .orchestrator_session / .orchestrator.log / .errors.log
│           │   └── .memory_audit  #   记忆防火墙审计日志
│           └── .git/              # Git 仓库（自动创建）
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
  "max_disputes": 2,                   // 修订争议协议最大轮数（达上限强制修订）
  "memory_guard": "quarantine",        // 记忆防火墙：quarantine / audit / off

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
        "Verifier": "qwen3.6-plus",
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

断点续传有两层：

**状态层** — `debug/.state`（key: value 格式）记录 pipeline、stage、迭代轮次、最新裁决、下一个 Agent 等：

```
pipeline: adaptive
stage: iteration
iteration: 3
last_verdict: PASS
next: Planner task_planner_4.md
```

Orchestrator 每完成一个阶段更新一次，续跑时先读它恢复决策上下文（auto-compact 后同样可恢复）。

**会话层** — `debug/.orchestrator_session` 与 `debug/.{role}.session` 存 Claude 会话 ID。超时/中断后，`run.py` / `spawn.py` 自动尝试 `claude --resume <会话ID>` 续接原会话（附固定的续传提示：先盘点已完成部分，再从中断处继续）；续接失败或再次超时才退回开新会话。`--resume` 只用于超时/中断，不用于 BLOCKED/FAIL 后的重试。

## Git 提交约定

`spawn.py` 在每次 spawn sub-agent 前后各做一次 git 快照（`fcntl.flock` 文件锁互斥，多题并行安全），提交消息前缀自动解析自 `debug/.state` 的 `pipeline:` 行：

| 时机 | 提交消息示例 |
|------|----------|
| sub-agent 启动前 | `standard: spawn Builder (task_builder)` |
| sub-agent 完成后 | `standard: Builder done (task_builder)` |
| sub-agent 失败后 | `standard: Builder failed (task_builder)` |
| run.py 收尾 | `standard: run complete (summary + memory audit)` |

快照实现在代码层，不依赖 Orchestrator 记得提交；`debug/` 同样纳入版本管理。

## 修订争议协议

Evaluator 给出 REVISE 后，不直接让 Builder 改，而是先走争议协议（防止正确的解答被错误审查意见带偏）：

```
REVISE → task_rebuttal_{n}: Builder 逐条 ACCEPT/REBUT（禁止改 solution.md）
       → REBUTTED=0 → 直接修订
       → REBUTTED>0 → task_rejoin_{n}: Evaluator 复审
           （MAINTAIN 必须附新证据：在 scripts/evaluator/rejoin_{n}/ 重新独立验证）
       → CONSENSUS → 修订
       → DISPUTED 且未达 max_disputes → n+=1 再来一轮
       → 达上限 → 强制修订，争议点单独标注，下次评估必须用全新证据
```

## 故障排查

### 问题：Agent 卡住或超时

**检查**：
1. `cat problems/<exam>/<n>/debug/.{role}.log` — 查看 Agent 日志
2. `cat problems/<exam>/<n>/debug/.state` — 查看当前阶段
3. `cat problems/<exam>/<n>/debug/.errors.log` — 查看运行期错误
4. `config.json` 中的 `timeout_seconds` — 是否太短

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
| `test_hang_kill.py` | sub-Agent 挂起防护：result 事件截断、宽限期、进程组清理 | 干测试（模拟子进程） |
| `textbook/test_smart_chunk.py` | 文本分块算法 | 干测试 |
| `textbook/test_mcp.py` | MCP 服务器 | 干测试 |

**注意**：目前没有"湿测试"（调用 API 的集成测试）。如需添加，建议放在 `tests/integration/` 目录。
