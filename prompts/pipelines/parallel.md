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

## Orchestrator 执行协议

### 阶段 1：{num_planners} 个 Planner 并行

写样板任务 `tasks/task_planner_{i}.md`（i = 1..{num_planners}，仅输出文件名不同）：

```markdown
# Task planner_{i}
说明：独立制定第 {i} 份解题计划（多方案并行之一）

请阅读 `{workspace}/problem.md`，独立制定一份解题计划。
将计划写入 `{workspace}/plan_{i}.md`。
```

并行 spawn——**「`&` 派发 + 轮询等待」规范模式**（总则见通用编排器「并行 spawn 与轮询等待」节；等待期间你的每一次回应都必须是 Bash 工具调用，输出纯文本会立即终止会话并害死后台 Planner）。角色名带编号以区分 `debug/.<Role>.result`（编号角色互不覆盖，故同角色也可并行）：

```bash
python3 {project_root}/scripts/spawn.py Planner_1 {workspace} agents/planner task_planner_1.md &
python3 {project_root}/scripts/spawn.py Planner_2 {workspace} agents/planner task_planner_2.md &
python3 {project_root}/scripts/spawn.py Planner_3 {workspace} agents/planner task_planner_3.md &
echo SPAWNED
```

然后按规范模式轮询等待（角色名 `Planner_1 Planner_2 Planner_3`，共 {num_planners} 个；重复执行轮询调用直到 `ALL_READY`），再依次读 `debug/.Planner_1.result` … `debug/.Planner_{num_planners}.result`。

### 阶段 2：Meta-Planner 选择/合并

`task_meta_planner.md`：

```markdown
# Task meta_planner
说明：评估并合并 {num_planners} 份计划，产出最终 plan.md

请阅读 `{workspace}/problem.md` 和 `{workspace}/plan_1.md` … `plan_{num_planners}.md`，
评估各方案，选择或合并出最优方案，并补充完整的计划结构（量纲预测、极端情况等）。
将最终计划写入 `{workspace}/plan.md`。
```

### 阶段 3 / 4：Builder / Evaluator

样板任务与路由同 Standard Pipeline（task_builder.md / task_evaluator.md，PASS/REVISE 循环；**REVISE 先走修订争议协议**，见通用编排器）。

**路由：**

- 至少 2 个 Planner `STATUS: OK` → 进入 Meta-Planner；不足 2 个 → 记入 `debug/.errors.log`，用已有 plan 降级继续（只有 1 个则直接将其作为 plan.md 的输入）
- Meta-Planner `OK` → Builder → Evaluator → PASS/REVISE 循环（同 Standard）
- 任一角色 `BLOCKED` → 重试一次，仍失败按上述降级策略处理

## 状态管理

```
planner_parallel
meta_planner
builder
evaluator
dispute_rebuttal_1（仅 REVISE 时）
builder_revise_1
evaluator_revise_1
done
```

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `num_planners`: {num_planners}
