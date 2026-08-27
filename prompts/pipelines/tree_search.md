# Tree Search Pipeline

## 概述

Planner 驱动决策 → 调用临时 Builder-Evaluator 验证小结论 → 形成完整方案 → Verifier 审查方案 → Final Builder 执行 → Final Evaluator 审查

## 流程

```
阶段 1：Planner 分析 + 验证循环（最多 {max_iterations} 次）
    Planner → strategy.md + task_{id}.md
        ↓
    Ephemeral Builder → calculation_{id}.md
        ↓
    Ephemeral Evaluator → verification_{id}.md
        ↓
    PASS → 追加到 calculations_history.md → 回到 Planner
    FAIL → Planner 调整策略
        ↓
    理解充分 → final_plan.md + 标记 DONE

阶段 2：Verifier 审查方案
    Verifier → verification_plan.md（首行 SOUND / REVISE）
    SOUND → 阶段 3
    REVISE → Planner 修订一次 → Verifier 复审
        （修订上限 1 轮：第二次无论什么裁决都放行）

阶段 3：Final Builder 执行
    Builder → solution.md

阶段 4：Final Evaluator 审查
    Evaluator → review.md
    PASS → final_summary.md
    REVISE → 回到 Final Builder（最多 {max_revisions} 次）
```

## Agent 配置

### Planner
- 使用基础版本：`agents/planner.md`
- 输入：problem.md + calculations_history.md
- 输出：`strategy.md` + `task_{id}.md` + `final_plan.md`
- 职责：自适应决策，决定需要验证什么

### Builder（临时模式）
- 基础版本：`agents/builder.md`
- **差分：**
  - 只验证小结论（积分、极限、数值验证等），不需要完整推导
  - 输出格式简化为 `calculation_{id}.md`
  - 超时缩短为 `{ephemeral_timeout}` 秒
  - 任务来源：`task_{id}.md`（Planner 写的验证任务）
  - 输出内容：计算过程 + 结果（不需要完整解题）

### Evaluator（临时模式）
- 基础版本：`agents/evaluator.md`
- **差分：**
  - 快速验证，只检查关键步骤
  - 输出简化为 `verification_{id}.md`
  - 第一行必须是 PASS 或 FAIL
  - 超时缩短为 `{ephemeral_timeout}` 秒
  - 不需要详细审查，只判断计算是否正确

### Verifier
- 基础版本：`agents/verifier.md`
- 输入：problem.md + final_plan.md（+ strategy.md 等上下文）
- 输出：`verification_plan.md`，第一行必须 `SOUND` 或 `REVISE`
- 职责：在 Final Builder 启动前审查方案的题意一致性、内部自洽性与结构健全性（允许短小数值抽查，禁止完整推导）

### Builder（最终模式）
- 使用基础版本：`agents/builder.md`（无差分）
- 输入：problem.md + final_plan.md
- 输出：`solution.md`
- 完整推导

### Evaluator（最终模式）
- 使用基础版本：`agents/evaluator.md`（无差分）
- 输入：problem.md + solution.md
- 输出：`review.md`
- 完整审查

## 职责划分（重要）

**所有物理内容都由 Planner / Builder / Evaluator 产出。Orchestrator 只做调度。样板任务文件一律写入 `{workspace}/tasks/`。**

| 文件 | 谁写 |
|------|------|
| `tasks/task_planner_{n}.md`（样板） | Orchestrator（只含调度指令，不含物理内容） |
| `tasks/task_{id}.md`（验证任务，含物理细节） | **Planner** |
| `tasks/task_eval_{id}.md`（样板） | Orchestrator（固定模板，`{id}` 取自 Planner HANDOFF 的 `NEXT_TASK`） |
| `tasks/task_verifier.md`（样板） | Orchestrator（固定模板） |
| `strategy.md`、`final_plan.md` | Planner |
| `verification_plan.md` | **Verifier** |
| `calculation_{id}.md`、`solution.md` | Builder |
| `verification_{id}.md`、`review.md` | Evaluator |

## Orchestrator 执行协议

### 迭代开始（第 $n$ 轮）

写入样板任务文件 `tasks/task_planner_{n}.md`（不含物理内容）：

```markdown
# Task planner_{n}

请阅读以下文件，决定下一步：
- `{workspace}/problem.md`
- `{workspace}/strategy.md`（如存在）
- 最新的 `calculation_*.md` 和 `verification_*.md`（如存在）

然后：
1. 更新 `{workspace}/strategy.md`（当前理解 + 下一步计划）
2. 二选一：
   a. 还需要验证 → 写 `{workspace}/tasks/task_{id}.md`（完整验证任务，含所有物理细节）
   b. 理解已充分 → 写 `{workspace}/final_plan.md`（完整求解方案）
```

然后 `spawn.py Planner {workspace} agents/planner task_planner_{n}`，读 `debug/.Planner.result`。

### 根据 Planner 的 HANDOFF 路由

- `STATUS: DONE` → 进入阶段 2（方案验证，spawn Verifier，见下）
- `STATUS: VERIFY` + `NEXT_TASK: task_{id}.md` → spawn Builder（`agents/builder task_{id}`，临时任务加 `--timeout {ephemeral_timeout}`），读 `debug/.Builder.result`
  - `STATUS: OK` → 写样板 `tasks/task_eval_{id}.md` → spawn Evaluator（`agents/evaluator task_eval_{id}`，加 `--timeout {ephemeral_timeout}`）
  - `STATUS: BLOCKED` → 直接进入下一轮迭代（Planner 自己会读文件了解情况）
- `STATUS: FAIL` → 直接进入下一轮迭代

**样板 `tasks/task_eval_{id}.md`：**

```markdown
# Task eval_{id}

请审查 `{workspace}/calculation_{id}.md`（参考 `{workspace}/problem.md`，并审计 `{workspace}/scripts/builder/` 下的代码——只读，不运行）。
你的验证脚本放 `{workspace}/scripts/evaluator/task_eval_{id}/`（从 problem.md 独立转录）。
将结果写入 `{workspace}/verification_{id}.md`。输出第一行必须是 PASS 或 FAIL。
```

### 根据 Evaluator 的 HANDOFF 路由

读 `debug/.Evaluator.result` 的 `VERDICT` 字段（可用 `head -1 verification_{id}.md` 交叉验证）：

- `PASS` → 更新 `debug/.state`，进入下一轮迭代
- `FAIL` → 更新 `debug/.state`，进入下一轮迭代（Planner 会看到失败并调整）

**两种裁决都回到 Planner** — 由 Planner 决定如何利用结果，Orchestrator 不做内容判断。

### 阶段 2：方案验证（Verifier）

写入样板任务文件 `tasks/task_verifier.md`：

```markdown
# Task verifier

请审查 `{workspace}/final_plan.md`（对照 `{workspace}/problem.md`；如需上下文可读 `{workspace}/strategy.md` 和已有的计算/验证记录）。
抽查脚本（如有）放 `{workspace}/scripts/verifier/`。
将结果写入 `{workspace}/verification_plan.md`。输出第一行必须是 SOUND 或 REVISE。
```

然后 `spawn.py Verifier {workspace} agents/verifier task_verifier`，读 `debug/.Verifier.result` 的 `VERDICT` 字段（可用 `head -1 verification_plan.md` 交叉验证）：

- `SOUND` → 更新 `debug/.state`，进入阶段 3（Final Builder）
- `REVISE` 且 `debug/.state` 中尚无 `verify_round`（第一次）：
  1. 更新 `debug/.state`：`verify_round: 1`
  2. 写样板 `tasks/task_planner_{n}.md`（`{n}` 为下一个迭代编号），内容在迭代样板基础上把第 3 条换成一句：「请阅读 `{workspace}/verification_plan.md` 中的问题清单，针对性修订 `{workspace}/final_plan.md`，完成后按原格式汇报 `STATUS: DONE`。」
  3. `spawn.py Planner {workspace} agents/planner task_planner_{n}`，读 `debug/.Planner.result`；`STATUS: DONE` 则回到本阶段重新验证（`STATUS: VERIFY/FAIL` 则按迭代路由处理）
- `REVISE` 且 `debug/.state` 已有 `verify_round: 1`（第二次）：**直接放行进入阶段 3**——在 `debug/.state` 记录 `last_verdict: REVISE` 后继续，不再循环

**验证最多 1 轮修订**：第二次 Verifier 裁决无论是什么都放行。

### 最终阶段样板任务文件（Final Builder / Final Evaluator）

```markdown
# Task final_builder

请阅读 `{workspace}/problem.md` 和 `{workspace}/final_plan.md`，执行完整求解。
将完整推导写入 `{workspace}/solution.md`，最终答案用 $\boxed{}$ 标注。
计算脚本放 `{workspace}/scripts/builder/final/`；按 final_plan 的步骤编号更新进度文件（见你的系统提示）。
```

```markdown
# Task final_evaluator

请审查 `{workspace}/solution.md`（对照 `{workspace}/problem.md`、`{workspace}/final_plan.md`，并审计 `{workspace}/scripts/builder/` 下的代码——只读，不运行）。
你的验证脚本放 `{workspace}/scripts/evaluator/final/`（从 problem.md 独立转录）。
将结果写入 `{workspace}/review.md`。输出第一行必须是 PASS 或 REVISE。
```

REVISE 时：**先执行修订争议协议**（见通用编排器的"修订争议协议"一节：Builder 回击 → 必要时 Evaluator 复审，达成共识或达 {max_disputes} 轮上限后才修订），然后更新 `debug/.state` 中的修订计数，重写样板任务（追加"请先阅读 review.md、rebuttal/rejoin 的最终结论并修正；未解决的争议点单独标注"），重新 spawn Builder（修订最多 {max_revisions} 次）。

## 状态管理

```
planner_1
ephemeral_builder_1
ephemeral_evaluator_1
planner_2
ephemeral_builder_2
ephemeral_evaluator_2
...
planner_done
plan_verifier
plan_revision_1（仅 REVISE 时）
plan_verifier_2（仅 REVISE 时）
final_builder
final_evaluator
final_builder_revise_1
final_evaluator_revise_1
done
```

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `max_iterations`: {max_iterations}
- `ephemeral_timeout`: {ephemeral_timeout}
