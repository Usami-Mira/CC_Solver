# Iterative Pipeline

## 概述

Explorer 提出假设 → Builder 验证 → Evaluator 评估 → 循环迭代直到收敛

## 流程

```
循环（最多 {max_iterations} 次）：
    Explorer → hypothesis_{N}.md
        ↓
    Builder → experiment_{N}.md
        ↓
    Evaluator → assessment_{N}.md
        ↓
    PASS → final_solution.md → 结束
    PARTIAL → 继续迭代
    DEAD_END → 回溯或结束
```

## Agent 配置

### Explorer
- 使用专用版本：`agents/explorer.md`
- 输入：problem.md + exploration_history.md
- 输出：`hypothesis_{N}.md`
- 权限：读 problem.md + exploration_history.md，写 hypothesis_{N}.md

### Builder
- 使用基础版本：`agents/builder.md`
- 输入：problem.md + hypothesis_{N}.md
- 输出：`experiment_{N}.md`
- 权限：读 problem.md + hypothesis_{N}.md，写 experiment_{N}.md

### Evaluator
- 使用基础版本：`agents/evaluator.md`
- 输入：problem.md + hypothesis_{N}.md + experiment_{N}.md
- 输出：`assessment_{N}.md`（第一行：PASS / PARTIAL / DEAD_END）
- 权限：读相关文件，写 assessment_{N}.md

## 状态管理

```json
{
  "stage": "iteration",
  "current_iteration": 2,
  "max_iterations": 5,
  "next": "explorer"
}
```

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `max_iterations`: {max_iterations}
