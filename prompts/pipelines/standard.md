# Standard Pipeline

## 概述

最简单的解题流程：Planner → Builder → Evaluator

## 流程

```
Planner → plan.md
    ↓
Builder → solution.md
    ↓
Evaluator → review.md
    ↓
PASS → final_summary.md
REVISE → 回到 Builder（最多 {max_revisions} 次）
```

## Agent 配置

### Planner
- 使用基础版本：`agents/planner.md`
- 输出：`plan.md`
- 权限：读 problem.md，写 plan.md

### Builder
- 使用基础版本：`agents/builder.md`
- 输入：problem.md + plan.md
- 输出：`solution.md`
- 权限：读 problem.md + plan.md，写 solution.md

### Evaluator
- 使用基础版本：`agents/evaluator.md`
- 输入：problem.md + solution.md
- 输出：`review.md`
- 权限：读 problem.md + solution.md，写 review.md

## Orchestrator 执行协议

**样板任务文件**（由 Orchestrator 撰写，只含调度指令、不含物理内容）：

`task_planner.md`：

```markdown
# Task planner

请阅读 `{workspace}/problem.md`，制定解题计划。
将计划写入 `{workspace}/plan.md`。
```

`task_builder.md`：

```markdown
# Task builder

请阅读 `{workspace}/problem.md` 和 `{workspace}/plan.md`，执行完整求解。
将完整推导写入 `{workspace}/solution.md`，最终答案用 $\boxed{}$ 标注。
```

`task_evaluator.md`：

```markdown
# Task evaluator

请审查 `{workspace}/solution.md`（对照 `{workspace}/problem.md`、`{workspace}/plan.md` 和 `{workspace}/scripts/` 下的代码）。
将结果写入 `{workspace}/review.md`。输出第一行必须是 PASS 或 REVISE。
```

**路由（只依据 `.result` 的 HANDOFF）：**

- Planner `STATUS: OK` → spawn Builder；`BLOCKED`/`FAIL` → 重试一次，仍失败记入 `.errors.log` 并终止
- Builder `STATUS: OK` → spawn Evaluator；`BLOCKED` → 重试一次
- Evaluator `VERDICT: PASS` → 写 final_summary.md，结束；`REVISE` → 更新 `.state` 中的修订计数，重写 `task_builder.md`（追加一句"请先阅读 review.md 中的问题清单并针对性修正"），重新 spawn Builder（最多 {max_revisions} 次，超限则带着最后的 review 结果写 final_summary.md 结束）

## 状态管理

```
planner
builder
evaluator
builder_revise_1
evaluator_revise_1
builder_revise_2
evaluator_revise_2
done
```

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
