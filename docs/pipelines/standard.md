# Standard Pipeline

**状态：** ✅ 已实现  
**适用场景：** 标准物理竞赛题，有明确解法

## 架构

```
Orchestrator
  ├── Planner → plan.md
  ├── Builder → solution.md
  ├── Evaluator → review.md
  │   └── REVISE? → 重新 Builder（最多 2 次）
  └── final_summary.md
```

## Agent 角色

| Agent | 职责 | 输入 | 输出 |
|-------|------|------|------|
| **Planner** | 分析问题，制定解题计划 | problem.md | plan.md |
| **Builder** | 执行推导，求解问题 | problem.md, plan.md | solution.md |
| **Evaluator** | 审查解答，判断 PASS/REVISE | problem.md, solution.md, plan.md | review.md |
| **Orchestrator** | 协调流程，管理状态 | - | final_summary.md |

## 工作流

1. **Planner 阶段**
   - 分析物理情景
   - 确定适用定律
   - 制定解题路线
   - 输出：`plan.md`

2. **Builder 阶段**
   - 基于 plan 执行推导
   - 逐步计算，带单位
   - 可用 Python 验证数值
   - 输出：`solution.md`

3. **Evaluator 阶段**
   - 检查物理正确性
   - 检查量纲一致性
   - 检查数学推导
   - 输出：`review.md`（首行 `PASS` 或 `REVISE`）

4. **REVISE 循环**（如需要）
   - 如果 `review.md` 首行为 `REVISE`
   - 将 review 反馈给 Builder
   - Builder 修正并重新输出
   - 最多迭代 2 次

5. **汇总阶段**
   - 写入 `final_summary.md`
   - 包含执行统计和最终答案

## 状态管理

`.state` 文件内容：
```
planner     # 下一步：运行 Planner
builder     # 下一步：运行 Builder
evaluator   # 下一步：运行 Evaluator
done        # 已完成
```

## Git 提交策略

| 时机 | 提交消息 |
|------|----------|
| 初始化后 | `init: workspace setup with problem files` |
| 预创建文件后 | `init: create output files` |
| Planner 完成后 | `plan: v1 complete` |
| Builder 完成后 | `solution: v1 complete` 或 `solution: v2 revised` |
| Evaluator 完成后 | `review: v1 complete` 或 `review: v2 revised` |
| 汇总后 | `final: summary` |

## 输出文件

```
problem.md          # 输入
plan.md             # Planner 输出
solution.md         # Builder 输出
review.md           # Evaluator 输出
final_summary.md    # 最终汇总
```

## 优点

- 简单直接，易于理解
- Token 消耗低
- 适合大多数标准问题

## 局限

- 只有一条路径，无法探索多种解法
- REVISE 循环只处理错误，不处理探索
- 不适合高度不确定的前沿问题
