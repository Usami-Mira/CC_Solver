# Parallel Pipeline

## 概述

多个 Planner 并行生成方案 → Meta-Planner 选择最优 → Builder 执行 → Evaluator 审查

## 流程

```
{num_planners} × Planner（并行）→ plan_1.md, plan_2.md, ...
    ↓
Meta-Planner → plan.md（选择最优方案）
    ↓
Builder → solution.md
    ↓
Evaluator → review.md
    ↓
PASS → final_summary.md
REVISE → 回到 Builder（最多 {max_revisions} 次）
```

## Agent 配置

### Planner（并行）
- 使用基础版本：`agents/planner.md`
- 并行数量：`{num_planners}`
- 输出：`plan_{i}.md`（i = 1, 2, ..., num_planners）
- 权限：读 problem.md，写 plan_{i}.md

### Meta-Planner
- 使用专用版本：`agents/meta_planner.md`
- 输入：problem.md + 所有 plan_{i}.md
- 输出：`plan.md`（综合最优方案）
- 权限：读 problem.md + plan_*.md，写 plan.md

### Builder
- 使用基础版本：`agents/builder.md`
- 输入：problem.md + plan.md
- 输出：`solution.md`

### Evaluator
- 使用基础版本：`agents/evaluator.md`
- 输入：problem.md + solution.md
- 输出：`review.md`

## 状态管理

```
planner_parallel
meta_planner
builder
evaluator
builder_revise_1
evaluator_revise_1
done
```

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `num_planners`: {num_planners}
