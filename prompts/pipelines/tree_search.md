# Tree Search Pipeline

## 概述

Planner 驱动决策 → 调用临时 Builder-Evaluator 验证小结论 → 形成完整方案 → Final Builder 执行 → Final Evaluator 审查

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

阶段 2：Final Builder 执行
    Builder → solution.md

阶段 3：Final Evaluator 审查
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
