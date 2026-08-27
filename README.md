# CC_Solver — 多 Agent 协作物理解题系统

## 简介

本项目通过 Claude Code CLI 编排多个 Agent 自动解决物理题目。系统提供 **6 种解题策略（Pipeline）**，适应不同类型的问题：

| Pipeline | 策略 | 适用场景 |
|----------|------|----------|
| **Standard** | Planner → Builder → Evaluator | 常规题目，思路明确 |
| **Parallel** | 3×Planner 并行 → Meta-Planner 选优 → Builder → Evaluator | 多解法探索，需要最优方案 |
| **Iterative** | Explorer 提出假设 → Builder 验证 → Evaluator 评估 → 循环迭代 | 开放性问题，需要逐步逼近 |
| **Debate** | 3×专家（理论/计算/实验）辩论 → Secretary 综合 → Builder → Evaluator | 复杂问题，需要多角度分析 |
| **Tree Search** | Planner 决策 → Ephemeral Builder-Evaluator 验证 → Verifier 审查方案 → Final Builder → Evaluator | 探索性问题，需要试错和回溯 |
| **Adaptive** | Planner 自适应决策 → Ephemeral Builder-Evaluator 验证 → 动态调整 → Verifier 审查方案 → Final Builder → Evaluator | 需要逐步验证和策略调整的问题 |

每道题支持断点续传：状态文件 + `claude --resume` 会话续接双重保障，中断后可自动从上次进度继续。系统使用 Git 自动追踪解题过程的完整演变（逐阶段快照在代码层自动完成），支持查看每个阶段的变更历史和版本对比。

## 环境安装

### 安装 Claude Code

本项目依赖 [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) CLI 工具：

```bash
npm install -g @anthropic-ai/claude-code
```

### 安装 Git

系统使用 Git 进行版本控制和解题过程追踪：

```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git

# Windows
# 下载 Git for Windows: https://git-scm.com/download/win
```

验证安装：
```bash
git --version
```

**注意**：Git 用于追踪每道题的解题过程演变（plan → solution → review），支持自动提交和迭代历史查看。

### 安装项目依赖

首次使用或依赖变更时，运行项目根目录的安装脚本：

```bash
bash setup.sh
```

这会自动创建 `textbook/rag_env` 虚拟环境并安装 RAG 知识库所需的全部依赖（PyTorch、FlagEmbedding、Weaviate 客户端等）。

### 配置 API Key（按量计费模式）

如果使用第三方兼容 API（如硅基流动等），设置环境变量：

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
export ANTHROPIC_BASE_URL="https://your-api-endpoint.example.com/v1"
```

将上述两行加入 `~/.bashrc` 或 `~/.zshrc` 以持久化。

### 放置题目

在 `problems/` 目录下为每道题创建一个子文件夹，放入 `problem.md`（如果不改名称，直接拖入任意md文件亦可，但是不建议）：

```
problems/
  example_single/
    problem.md
  example_multiple/
    1/
      problem.md
    2/
      problem.md
    3/
      problem.md
```

多题只需指定父目录，系统会自动识别并依次处理。

## 配置

编辑项目根目录的 `config.json`：

```json
{
  "pipeline": "standard",
  "max_concurrent_problems": 3,
  "max_disputes": 2,
  "memory_guard": "quarantine",

  "configs": {
    "standard": {
      "model": "qwen3.6-plus",
      "timeout_seconds": 600,
      "max_revisions": 2,
      "agent_models": {
        "Planner": "qwen3.6-plus",
        "Builder": "qwen3.6-plus",
        "Evaluator": "qwen3.6-plus"
      }
    },

    "adaptive": {
      "model": "qwen3.6-plus",
      "timeout_seconds": 600,
      "max_iterations": 15,
      "max_revisions": 2,
      "ephemeral_timeout": 300,
      "agent_models": {
        "Planner": "qwen3.6-plus",
        "Builder": "qwen3.6-plus",
        "Evaluator": "qwen3.6-plus"
      }
    }
  }
}
```

**顶层字段：**

| 字段 | 说明 |
|------|------|
| `pipeline` | 当前使用的解题策略：`standard` / `parallel` / `iterative` / `debate` / `tree_search` / `adaptive` |
| `max_concurrent_problems` | 多题场景下同时并行处理的最大题目数，默认 3 |
| `max_disputes` | 修订争议协议最大轮数：REVISE 时 Builder 回击 → Evaluator 复审，达上限后强制修订（争议点单独标注），默认 2 |
| `memory_guard` | 记忆防火墙模式：`quarantine`（运行后 git 快照隔离，重置本次运行对记忆目录的改动）/ `audit`（只记录不重置）/ `off` |

**各 Pipeline 配置字段（在 `configs` 下）：**

| 字段 | 适用 Pipeline | 说明 |
|------|--------------|------|
| `model` | 所有 | 默认使用的模型名 |
| `timeout_seconds` | 所有 | 单次调用的最大超时时间（秒） |
| `max_revisions` | 所有 | Builder-Evaluator 循环的最大修正次数 |
| `max_iterations` | iterative, tree_search, adaptive | 迭代循环的最大次数 |
| `max_rounds` | debate | 辩论轮数 |
| `num_planners` | parallel | 并行 Planner 数量 |
| `ephemeral_timeout` | tree_search, adaptive | Ephemeral Builder/Evaluator 超时（秒） |
| `agent_models` | 所有 | 为不同 Agent 配置不同模型 |

## 运行

```bash
# 处理单道题（使用 config.json 中的 pipeline）
python3 scripts/run.py problems/example_single

# 处理一批题（自动识别多题模式）
python3 scripts/run.py problems/example_multiple

# 指定 pipeline（覆盖 config.json）
python3 scripts/run.py problems/example_single --pipeline parallel
python3 scripts/run.py problems/example_single --pipeline debate
python3 scripts/run.py problems/example_single --pipeline tree_search
python3 scripts/run.py problems/example_single --pipeline adaptive
```

**Pipeline 选择建议：**

| 题目类型 | 推荐 Pipeline | 理由 |
|----------|--------------|------|
| 常规计算题 | `standard` | 简单直接，资源消耗最少 |
| 多解法题目 | `parallel` | 并行探索多种思路，选最优 |
| 开放性探究 | `iterative` | 假设-验证循环，逐步逼近 |
| 复杂综合题 | `debate` | 多角度分析，专家辩论收敛 |
| 探索性问题 | `tree_search` | 试错+回溯，灵活决策 |
| 需要验证的问题 | `adaptive` | 逐步验证，动态调整策略 |

## 运行测试

```bash
# 运行 Git 集成测试（权限配置、Git 初始化等）
python3 scripts/test_git_integration.py -v

# 运行进程挂起防护测试（result 事件截断、进程组清理）
python3 scripts/test_hang_kill.py

# 运行文本处理管道测试（分块、token 估算等）
python3 textbook/run_tests.py

# 或运行单个测试文件
python3 textbook/test_smart_chunk.py -v
```

测试覆盖：
- Git 版本控制初始化和权限配置
- 文本处理管道的核心逻辑：智能分块、段落边界检测、token 估算
- MCP 服务器和知识库查询

## 查看结果

每道题的子文件夹中，用户需要关注的文件：

| 文件 | 说明 |
|------|------|
| `plan.md` | 解题计划（物理情景、适用定律、解题路线） |
| `solution.md` | 完整求解过程与最终答案 |
| `review.md` | 审查结果，首行为 `PASS` 或 `REVISE` |
| `final_summary.md` | 最终汇总：执行统计 + 完整答案（**主要阅读文件**） |

多题场景下，父目录还会生成 `batch_summary.md`，汇总所有子题的状态和答案摘要。

### 查看解题过程历史

每道题的工作目录都是一个 Git 仓库，可以查看解题过程的完整演变：

```bash
cd problems/example_single

# 查看提交历史
git log --oneline

# 典型输出：
# a1b2c3d final: summary
# e4f5g6h review: v2 revised
# i7j8k9l solution: v2 revised
# m0n1o2p review: v1 complete
# q3r4s5t solution: v1 complete
# t9u0v1w plan: v1 complete
# x2y3z4a init: create output files

# 查看 solution.md 的变更历史
git log -p solution.md

# 对比 v1 和 v2 的差异（如果有 REVISE）
git diff HEAD~2 solution.md
```

`debug/` 目录存放系统内部使用的状态和缓存文件，一般不需要手动查看（也纳入 Git 版本管理，可事后审计）：

| 文件 | 说明 |
|------|------|
| `debug/.state` | 断点续传状态文件（key: value），记录当前阶段、轮次、裁决与下一个 Agent |
| `debug/.{role}.result` | 对应 Agent 的 HANDOFF 汇报（≤6 行） |
| `debug/.{role}.metrics` | 对应 Agent 的调用指标（用时、Token 消耗等） |
| `debug/.{role}.session` | 对应 Agent 的 Claude 会话 ID（用于 `--resume` 断点续传） |
| `debug/.{role}.progress` | 对应 Agent 的进度条（`k/N: 摘要`，单行） |
| `debug/.orchestrator.log` | Orchestrator 流式日志 |
| `debug/.errors.log` | 运行期错误记录 |
| `debug/.memory_audit` | 记忆防火墙审计日志（运行前后记忆目录的 git 快照对比） |

## 注意事项

- **不要手动删除 `debug/` 下的文件**：如果需要重做某道题，删除该题子文件夹下除 `problem.md` 之外的所有生成文件和目录（含 `debug/`、`tasks/`、`scripts/`）即可重置。
- **超时设置**：复杂题目可能耗时较长，`timeout_seconds` 建议设大一些。如果中途中断，下次运行会自动从断点续传。
- **模型选择**：推荐使用推理能力较强的模型，弱模型在物理推导上可能出错。
- **题目格式**：`problem.md` 建议使用纯文本或 Markdown，包含题目描述、已知条件和待求量。如果题目含图片，可在 Markdown 中用文字描述图片内容。

## 项目结构

```
.
├── config.json              # 项目配置（模型名、超时时间、并行数）
├── setup.sh                 # 一键安装脚本（RAG 虚拟环境 + 依赖）
├── CLAUDE.md                # Claude Code 项目配置
├── PROJECT_STRUCTURE.md     # 详细项目结构和开发指南
├── scripts/                 # 脚本目录
│   ├── run.py               # 入口脚本：组装 Orchestrator prompt 并启动
│   ├── spawn.py             # 子进程辅助脚本：创建 sub-agent，含权限配置、逐阶段 Git 快照、--resume 续传
│   ├── memory_guard.py      # 记忆防火墙：用 git 快照隔离/审计 ~/.claude 记忆目录
│   ├── stream_parser.py     # 流式输出解析器
│   ├── statusline.py        # Claude Code 状态栏：实时显示 pipeline 进度
│   ├── test_git_integration.py  # Git 集成单元测试
│   └── test_hang_kill.py    # 进程挂起防护回归测试
├── prompts/                 # Agent 定义和 Skill 定义
│   ├── orchestrator.md      # 通用 Orchestrator system prompt
│   ├── agents/              # 各 Agent 定义
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
│   ├── pipelines/           # 各 Pipeline 配置
│   │   ├── standard.md
│   │   ├── parallel.md
│   │   ├── iterative.md
│   │   ├── debate.md
│   │   ├── tree_search.md
│   │   └── adaptive.md
│   └── skills/              # Skill 定义
│       ├── calculation.md
│       ├── dimension_check.md
│       └── knowledge_base.md
├── problems/                # 题目目录
│   └── <exam>/
│       ├── <n>/
│       │   ├── problem.md         # 输入：题目
│       │   ├── plan.md            # Planner 输出
│       │   ├── solution.md        # Builder 输出
│       │   ├── review.md          # Evaluator 输出
│       │   ├── final_summary.md   # 最终汇总（含记忆审计段落）
│       │   ├── tasks/             # 任务文件（task_*.md、rebuttal/rejoin 任务）
│       │   ├── scripts/           # 按角色隔离的脚本：builder/、evaluator/、verifier/（每个任务再分子目录）
│       │   ├── debug/             # 内部状态目录（.state、.*.result、.*.session、日志、进度）
│       │   └── .git/              # Git 仓库（自动创建，追踪解题过程）
│       └── ...
├── textbook/                # 教科书 RAG 知识库（详见下方）
│   ├── batch_parse.py               # 分卷合并
│   ├── fix_formulas.py              # OCR 公式修正
│   ├── extract_image_context.py     # 图片上下文提取
│   ├── mcp_server.py                # MCP 服务器（Cherry Studio 集成）
│   ├── split_by_chapter.py          # 按章节切分内容
│   ├── rag_build/                   # RAG 构建脚本
│   │   ├── chunk_markdown.py        # 文本分块
│   │   ├── translate_chunks.py      # 中文→英文翻译
│   │   └── embed_bge.py             # 向量嵌入 + Weaviate 存储
│   ├── by_chapter/                  # 按章节组织的知识库
│   └── weaviate_data/               # Weaviate 向量数据库
└── README.md
```

## 技术细节

### 架构

系统通过 Claude Code CLI 的 `--agents` 功能创建独立的 Agent 进程：

```
Orchestrator
  │
  ├── 滑动窗口并行（最多 max_concurrent_problems 题同时运行）
  │   初始启动 3 题，任一题完成后立即从队列补入下一题
  │   例：1,2,3 同时跑 → 1 完成 → 4 补入 → 2,3,4 同时跑 → 3 完成 → 5 补入 → 2,4,5 同时跑 → ...
  │
  └── 全部完成后生成 batch_summary.md
```

单道题内的阶段顺序：

```
题目 X
  ├── spawn Planner   → plan.md
  ├── spawn Builder   → solution.md
  ├── spawn Evaluator → review.md
  └── 检查 review.md
        PASS  → final_summary.md
        REVISE → 先走修订争议协议（Builder 逐条回击 → 必要时 Evaluator 复审，
                 达成共识或达 max_disputes 上限），然后才重新 spawn Builder 修订，
                 最多 max_revisions 次
```

每个 Agent 是一个独立的 Claude Code 进程，通过 `spawn.py` 封装创建。Agent 之间不直接通信，而是通过文件系统中的 Markdown 文件传递结果。

### 断点续传

断点续传有两层：

1. **状态层**：`debug/.state`（key: value 格式）记录当前 pipeline 阶段、迭代轮次、最新裁决、下一个 Agent 等。Orchestrator 每完成一个阶段更新一次，续跑时先读它恢复决策上下文。
2. **会话层**：Orchestrator 和每个 sub-agent 的 Claude 会话 ID 分别存于 `debug/.orchestrator_session` 和 `debug/.{role}.session`。超时/中断后，下次运行自动用 `claude --resume <会话ID>` 续接原会话（模型从中断处继续，而不是从头再来）；若续接失败或再次超时，才退回开新会话并依据 `.state` 继续。

`debug/.state` 中 `stage` 已为完成态、或 `final_summary.md` 已存在时视为已完成，不再续跑。

### Agent 进度条

Builder 执行最终推导时，会按 plan / final_plan 的步骤编号逐步覆写 `debug/.builder.progress`（单行：`k/N: 本步摘要`）。`run.py` 的后台监视器与 `statusline.py`（Claude Code 状态栏）实时读取并渲染，长推导也能看到进行到了哪一步；其他角色的进度文件同理。

### Agent 定义

各 Agent 的 system prompt 分别定义在 `prompts/` 目录下的独立 `.md` 文件中。`run.py` 启动时读取所有文件并组装成完整的 Orchestrator prompt（含嵌入的 sub-Agent prompt 和 Skill 定义）。新增角色只需在 `prompts/` 下添加 `.md` 文件并更新 `run.py` 的组装逻辑。新增 Skill 只需在 `prompts/skills/` 下添加 `.md` 文件，并在对应 Agent prompt 中声明引用。

### Git 版本控制

每道题的工作目录在启动时自动初始化为 Git 仓库，用于追踪解题过程的完整演变。

**提交时机（代码层自动完成，不依赖模型自觉）：**

`spawn.py` 在每次 spawn sub-agent 前后各做一次 git 快照（文件锁互斥，多题并行安全），提交消息前缀 `<pipeline>:` 自动解析自 `debug/.state`：

| 时机 | 提交消息示例 |
|------|----------|
| sub-agent 启动前 | `standard: spawn Builder (task_builder)` |
| sub-agent 完成后 | `standard: Builder done (task_builder)` |
| sub-agent 失败后 | `standard: Builder failed (task_builder)` |
| run.py 收尾 | `standard: run complete (summary + memory audit)` |

快照实现在代码层（而非依赖 Orchestrator 在 prompt 里记得 commit），因此即使模型忘记也不会漏提交。`debug/` 目录同样纳入版本管理，`.state`、`.result`、日志等可事后审计。

**典型 Git 历史：**

```bash
$ git log --oneline
c9d8e7f standard: run complete (summary + memory audit)
a1b2c3d standard: Evaluator done (task_evaluator)
e4f5g6h standard: spawn Evaluator (task_evaluator)
i7j8k9l standard: Builder done (task_builder)
m0n1o2p standard: spawn Builder (task_builder)
q3r4s5t standard: Planner done (task_planner)
u6v7w8x standard: spawn Planner (task_planner)
```

**Agent 的 Git 权限：**

Sub-Agent（Planner/Builder/Evaluator）可以使用只读 Git 命令查看历史，但不能修改仓库：
- ✅ 允许：`git status`、`git diff`、`git log`、`git add`
- ❌ 禁止：`git commit`、`git reset`、`git checkout`、`git push`

这样 Agent 可以查看文件变更历史（如 `git diff HEAD~1 solution.md` 查看 Builder 的修改），但提交由 `spawn.py` 在代码层自动完成，确保提交历史的一致性和可追溯性。

### 权限控制

每个 Agent 的工具权限通过 `spawn.py` 中的 `AGENT_PROFILES` 字典精确控制，使用 Claude Code 的 `--allowed-tools` 参数实现命令级别的权限隔离。

**权限配置示例：**

```python
AGENT_PROFILES = {
    "Planner": (
        "Read,"                          # 读取文件
        "Write,"                         # 写入文件
        "Edit,"                          # 编辑文件
        "Bash(python3 *),"               # 运行 Python 脚本
        "Bash(source * && python3 *),"   # 激活虚拟环境后运行脚本
        "Bash(git status*),"             # Git 状态查询
        "Bash(git diff*),"               # Git 差异比较
        "Bash(git log*),"                # Git 历史查看
        "Bash(git add *)"                # Git 暂存文件
    ),
    # Builder 和 Evaluator 权限相同
}
```

**安全设计：**

1. **命令模式匹配**：`Bash(python3 *)` 只允许以 `python3` 开头的命令，阻止 `rm`、`curl` 等危险操作
2. **最小权限原则**：Agent 只能执行解题必需的命令，无法安装软件包或访问网络
3. **Git 写入隔离**：只有 Orchestrator 可以执行 `git commit`，Sub-Agent 只能读取
4. **工作目录限制**：Agent 被约束在 `{workspace}` 目录内，无法访问其他题目或项目文件

**权限覆盖：**

如果需要临时调整权限，可以通过 `spawn.py` 的 `--tools` 参数覆盖：

```bash
python3 scripts/spawn.py Planner problems/example --tools "Read,Write,Bash"
```

但通常不需要手动调整，默认配置已针对各角色的职责优化。

### 记忆防火墙

解题会话中的 sub-agent 应当"自己把题做出来"，而不是借用平时积累的记忆。系统从三层防御：

1. **注入阻断**：所有 pipeline 会话（Orchestrator 与每个 sub-agent）都以 `--bare` 模式运行，Claude Code 的 auto-memory 注入、CLAUDE.md 自动发现均被关闭。
2. **git 隔离**：`scripts/memory_guard.py` 在运行前后对记忆目录（`~/.claude/projects/<项目>/memory/`）做 git 快照。`quarantine` 模式（默认）下，运行期间对记忆目录的任何改动会在结束后被重置（所有改动都留在 git 历史中，不会被销毁）；`audit` 模式只记录不重置；`off` 关闭。
3. **审计留痕**：审计结果写入 `debug/.memory_audit`，并追加到 `final_summary.md` 的"记忆审计"段落，可与答案的推导过程对照核查。

此外，所有 Agent 的 prompt 都明确禁止读写 `~/.claude/` 下的任何文件（记忆、历史会话），也不得在任务文件中提及。

---

## 教科书 RAG 知识库

`textbook/` 目录包含从 4 本高中物理竞赛教科书（电磁学、力学、光学、热学）PDF 扫描件构建的 RAG 知识库，为解题 Agent 提供物理知识检索能力。

### 构建流程

| 步骤 | 脚本 | 说明 |
|------|------|------|
| 1. OCR | MinerU Web API | PDF → 结构化 Markdown + 图片 |
| 2. 公式修正 | `fix_formulas.py` | LLM 纠正 OCR 公式错误 |
| 3. 图片上下文 | `extract_image_context.py` | 提取图文关联 |
| 4. 合并分卷 | `batch_parse.py` | 多 part → 单文件 Markdown |
| 5. 文本分块 | `rag_build/chunk_markdown.py` | 按章节切分为 1139 个语义块 |
| 6. 翻译 | `rag_build/translate_chunks.py` | Qwen 3.6 Flash 中英双语（20 并发） |
| 7. 向量嵌入 | `rag_build/embed_bge.py` | BGE-base-en-v1.5 → Weaviate |

### 技术选型

| 组件 | 选型 | 理由 |
|------|------|------|
| OCR | MinerU Web API | 结构化输出，支持公式和图片 |
| 翻译 | Qwen 3.6 Flash | 快速、物理术语准确 |
| 嵌入模型 | BGE-base-en-v1.5 | 768维，语义检索效果好 |
| 向量数据库 | Weaviate Embedded | 无需 Docker，本地持久化 |

### 数据说明

原始 PDF、OCR 输出、合并后的 Markdown、图片和嵌入模型文件均通过 `.gitignore` 排除，不纳入版本管理。构建好的 Weaviate 数据库（`weaviate_data/`，61MB）直接包含在仓库中，clone 后即可使用。如需从头重建知识库，按上表步骤依次运行即可。
