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
