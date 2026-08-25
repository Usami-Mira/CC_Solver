# Adaptive Pipeline

## 概述

Planner 自适应决策 → 调用临时 Builder-Evaluator 验证小结论 → 动态调整策略 → 形成完整方案 → Final Builder 执行 → Final Evaluator 审查

## 流程

```
阶段 1：Planner 自适应分析 + 验证循环（最多 {max_iterations} 次）
    Planner → strategy.md + task_{id}.md
        ↓
    Ephemeral Builder → calculation_{id}.md
        ↓
    Ephemeral Evaluator → verification_{id}.md
        ↓
    PASS → 追加到 calculations_history.md → 回到 Planner
    FAIL → Planner 调整策略（可能换方法或深入验证）
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
- **差分：**
  - 强调自适应决策（根据验证结果动态调整策略）
  - 输入增加 `calculations_history.md`（之前的验证结果）
  - 输出增加 `strategy.md`（当前理解和下一步计划）
  - 可以随时标记 DONE（不必达到 max_iterations）
  - 职责：分析理解程度，决定验证什么，根据结果调整

### Builder（临时模式）
- 基础版本：`agents/builder.md`
- **差分：**
  - 只验证小结论（积分、极限、数值验证、量纲检查等）
  - 输出格式简化为 `calculation_{id}.md`
  - 超时缩短为 `{ephemeral_timeout}` 秒
  - 任务来源：`task_{id}.md`（Planner 写的验证任务）
  - 输出内容：验证过程 + 结果（不需要完整解题）

### Evaluator（临时模式）
- 基础版本：`agents/evaluator.md`
- **差分：**
  - 快速验证，只检查关键步骤
  - 输出简化为 `verification_{id}.md`
  - 第一行必须是 PASS 或 FAIL
  - 超时缩短为 `{ephemeral_timeout}` 秒
  - 不需要详细审查，只判断验证是否正确

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

## 与 Tree Search 的区别

| 特性 | Tree Search | Adaptive |
|------|-------------|----------|
| 决策方式 | 树状探索 + 回溯 | 线性迭代 + 自适应调整 |
| 状态管理 | 复杂树结构 | 简单历史记录 |
| 适用场景 | 多路径探索 | 单路径深入验证 |
| Planner 职责 | 生成探索树 | 自适应决策 + 动态调整 |

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
