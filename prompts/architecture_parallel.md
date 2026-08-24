# Parallel Paths Architecture

## 流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator                              │
│  (读取 problem.md, 编排子 Agent, 管理状态)                    │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Planner 1   │ │  Planner 2   │ │  Planner 3   │
    │  (并行执行)   │ │  (并行执行)   │ │  (并行执行)   │
    │  → plan_1.md │ │  → plan_2.md │ │  → plan_3.md │
    └──────────────┘ └──────────────┘ └──────────────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Meta-Planner    │
                  │  (评估 + 选择)    │
                  │  → plan.md       │
                  └──────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Builder         │
                  │  (执行推导)       │
                  │  → solution.md   │
                  └──────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Evaluator       │
                  │  (审查)          │
                  │  → review.md     │
                  └──────────────────┘
                            │
                    ┌───────┴───────┐
                    │               │
                    ▼               ▼
                  PASS           REVISE
                    │               │
                    │               └──→ Builder (修正)
                    │                      (最多 2 次)
                    ▼
              ┌──────────────┐
              │ Final Summary│
              │ (final_summary.md)│
              └──────────────┘
```

## 状态转换

```
parallel_planner_1
parallel_planner_2
parallel_planner_3
meta_planner
builder
evaluator
builder_revise_1
evaluator_revise_1
builder_revise_2
evaluator_revise_2
done
```

## 文件流

**输入：**
- `problem.md` — 物理题目

**中间文件：**
- `plan_1.md`, `plan_2.md`, `plan_3.md` — 3 个 Planner 的独立方案
- `plan.md` — Meta-Planner 选择/合并后的最终方案
- `solution.md` — Builder 的完整求解
- `review.md` — Evaluator 的审查结果

**输出：**
- `final_summary.md` — 最终总结报告

## 关键特性

1. **并行探索**：3 个 Planner 独立分析，增加找到创新方案的概率
2. **元评估**：Meta-Planner 综合比较，避免单一视角的局限
3. **方案融合**：可以合并多个方案的优点
4. **质量保障**：保留 Evaluator 审查 + REVISE 循环

## 适用场景

- 问题有多种可能的解法
- 不确定哪种方法最有效
- 需要探索创新思路（如"绕过椭圆积分的方法"）
- 有充足的计算资源（token 预算较高）
