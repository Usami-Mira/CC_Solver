# Adaptive Pipeline

## 概述

Planner 自适应决策 → 调用临时 Builder-Evaluator 验证小结论 → 动态调整策略 → 形成完整方案 → Final Builder 执行 → Final Evaluator 审查

## 流程

```
阶段 1：Planner 自适应分析 + 验证循环（最多 {max_iterations} 次）
    Planner → strategy.md + task_{id}.md（+ 更新 calculations_history.md）
        ↓
    Ephemeral Builder → calculation_{id}.md
        ↓
    Ephemeral Evaluator → verification_{id}.md
        ↓
    PASS → 回到 Planner（进入下一轮迭代）
    FAIL → 回到 Planner（调整策略）
        ↓
    Planner 认为理解充分 → final_plan.md + HANDOFF 标记 DONE

阶段 2：Final Builder 执行
    Builder → solution.md

阶段 3：Final Evaluator 审查
    Evaluator → review.md
    PASS → final_summary.md
    REVISE → 回到 Final Builder（最多 {max_revisions} 次）
```

## 职责划分（重要）

**所有物理内容都由 Planner / Builder / Evaluator 产出。Orchestrator 只做调度。**

| 文件 | 谁写 |
|------|------|
| `task_planner_{n}.md`（样板） | Orchestrator（只含调度指令，不含物理内容） |
| `task_{id}.md`（验证任务，含物理细节） | **Planner** |
| `task_eval_{id}.md`（样板） | Orchestrator（固定模板，`{id}` 取自 Planner HANDOFF 的 `NEXT_TASK`） |
| `strategy.md`、`final_plan.md`、`calculations_history.md` | Planner |
| `calculation_{id}.md`、`solution.md` | Builder |
| `verification_{id}.md`、`review.md` | Evaluator |

## Orchestrator 执行协议

### 迭代开始（第 $n$ 轮）

写入样板任务文件 `task_planner_{n}.md`（不含物理内容）：

```markdown
# Task planner_{n}

请阅读以下文件，决定下一步：
- `{workspace}/problem.md`
- `{workspace}/strategy.md`（如存在）
- `{workspace}/calculations_history.md`（如存在）
- 最新的 `calculation_*.md` 和 `verification_*.md`（如存在）

然后：
1. 更新 `{workspace}/strategy.md`（当前理解 + 下一步计划）
2. 若最新一轮验证的结论应保留，将其要点追加到 `{workspace}/calculations_history.md`
3. 二选一：
   a. 还需要验证 → 写 `{workspace}/task_{id}.md`（完整验证任务，含所有物理细节）
   b. 理解已充分 → 写 `{workspace}/final_plan.md`（完整求解方案）
```

然后 `spawn.py Planner {workspace} agents/planner task_planner_{n}`，读 `.Planner.result`。

### 根据 Planner 的 HANDOFF 路由

- `STATUS: DONE` → 进入阶段 2（spawn Builder，任务文件用样板，见下）
- `STATUS: VERIFY` + `NEXT_TASK: task_{id}.md` → spawn Builder（`agents/builder task_{id}`），读 `.Builder.result`
  - `STATUS: OK` → 写样板 `task_eval_{id}.md` → spawn Evaluator（`agents/evaluator task_eval_{id}`）
  - `STATUS: BLOCKED` → 直接进入下一轮迭代（Planner 自己会读文件了解情况）
- `STATUS: FAIL` → 直接进入下一轮迭代

**样板 `task_eval_{id}.md`：**

```markdown
# Task eval_{id}

请审查 `{workspace}/calculation_{id}.md`（参考 `{workspace}/problem.md` 和 `{workspace}/scripts/` 下的代码）。
将结果写入 `{workspace}/verification_{id}.md`。输出第一行必须是 PASS 或 FAIL。
```

### 根据 Evaluator 的 HANDOFF 路由

读 `.Evaluator.result` 的 `VERDICT` 字段（可用 `head -1 verification_{id}.md` 交叉验证）：

- `PASS` → 更新 `.state`，git commit，进入下一轮迭代
- `FAIL` → 更新 `.state`，git commit，进入下一轮迭代（Planner 会看到失败并调整）

**两种裁决都回到 Planner** — 由 Planner 决定如何利用结果，Orchestrator 不做内容判断。

### 阶段 2 / 3 样板任务文件

```markdown
# Task final_builder

请阅读 `{workspace}/problem.md` 和 `{workspace}/final_plan.md`，执行完整求解。
将完整推导写入 `{workspace}/solution.md`，最终答案用 $\boxed{}$ 标注。
```

```markdown
# Task final_evaluator

请审查 `{workspace}/solution.md`（对照 `{workspace}/problem.md`、`{workspace}/final_plan.md` 和 `{workspace}/scripts/`）。
将结果写入 `{workspace}/review.md`。输出第一行必须是 PASS 或 REVISE。
```

REVISE 时：更新 `.state` 中的修订计数，重写样板任务（追加一句"请阅读 review.md 中的问题清单并修正"），重新 spawn Builder。

## Agent 配置

### Planner
- 基础版本：`agents/planner.md`
- **差分：** 自适应模式下额外输出 `strategy.md`、`task_{id}.md`、`calculations_history.md`、`final_plan.md`；最终消息为 HANDOFF 格式（`STATUS: VERIFY/DONE/FAIL` + `NEXT_TASK`）
- 职责：分析理解程度，决定验证什么，根据结果调整

### Builder（临时模式）
- 基础版本：`agents/builder.md`
- **差分：** 只验证小结论；输出 `calculation_{id}.md`；超时 `{ephemeral_timeout}` 秒；最终消息为 HANDOFF 格式

### Evaluator（临时模式）
- 基础版本：`agents/evaluator.md`
- **差分：** 快速验证；输出 `verification_{id}.md`，第一行必须 `PASS` 或 `FAIL`；超时 `{ephemeral_timeout}` 秒；最终消息为 HANDOFF 格式（`VERDICT`）

### Builder / Evaluator（最终模式）
- 使用基础版本（无差分），最终消息为 HANDOFF 格式

## 状态管理

`.state` 示例（每完成一个阶段更新）：

```
pipeline: adaptive
stage: iteration
iteration: 3
last_verdict: PASS
next: Planner task_planner_4.md
```

## 与 Tree Search 的区别

| 特性 | Tree Search | Adaptive |
|------|-------------|----------|
| 决策方式 | 树状探索 + 回溯 | 线性迭代 + 自适应调整 |
| 状态管理 | 复杂树结构 | 简单历史记录 |
| 适用场景 | 多路径探索 | 单路径深入验证 |
| Planner 职责 | 生成探索树 | 自适应决策 + 动态调整 |

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `max_iterations`: {max_iterations}
- `ephemeral_timeout`: {ephemeral_timeout}
