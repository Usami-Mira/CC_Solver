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

**样板任务文件全部写入 `{workspace}/tasks/`**（spawn 参数只写文件名，`spawn.py` 自动查找 tasks/），由 Orchestrator 撰写，只含调度指令、不含物理内容：

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
计算脚本放 `{workspace}/scripts/builder/final/`；按 plan 的步骤编号更新进度文件（见你的系统提示）。
```

`task_evaluator.md`：

```markdown
# Task evaluator

请审查 `{workspace}/solution.md`（对照 `{workspace}/problem.md`、`{workspace}/plan.md`，并审计 `{workspace}/scripts/builder/` 下的代码——只读，不运行）。
你的验证脚本放 `{workspace}/scripts/evaluator/final/`（从 problem.md 独立转录）。
将结果写入 `{workspace}/review.md`。输出第一行必须是 PASS 或 REVISE。
```

**路由（只依据 `debug/.<Role>.result` 的 HANDOFF）：**

- Planner `STATUS: OK` → spawn Builder；`BLOCKED`/`FAIL` → 重试一次，仍失败记入 `debug/.errors.log` 并终止
- Builder `STATUS: OK` → spawn Evaluator；`BLOCKED` → 重试一次
- Evaluator `VERDICT: PASS` → 写 final_summary.md，结束；`REVISE` → **先执行修订争议协议**（见通用编排器的"修订争议协议"一节：Builder 回击 → 必要时 Evaluator 复审，达成共识或达 {max_disputes} 轮上限后才修订），然后重写 `tasks/task_builder.md`（追加"请先阅读 review.md、rebuttal/rejoin 的最终结论并针对性修正；未解决的争议点单独标注"），重新 spawn Builder（修订与争议合计仍受 {max_revisions} 次修订上限约束，超限则带着最后的 review 结果写 final_summary.md 结束）

## 状态管理

```
planner
builder
evaluator
dispute_rebuttal_1（仅 REVISE 时）
dispute_rejoin_1（仅存在 REBUT 时）
builder_revise_1
evaluator_revise_1
dispute_rebuttal_2（仅再次 REVISE 时）
builder_revise_2
evaluator_revise_2
done
```

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
