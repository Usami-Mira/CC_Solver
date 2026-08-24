# Debate Architecture

## 流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator                              │
│  (读取 problem.md, 编排辩论, 管理状态)                       │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Theorist    │ │  Comp-       │ │  Experi-     │
    │  (理论分析)   │ │  utationalist│ │  mentalist   │
    │  → theorist  │ │  (计算分析)   │ │  (估算分析)   │
    │    .md       │ │  → computa-  │ │  → experi-   │
    │              │ │    tionalist │ │    mentalist │
    │              │ │    .md       │ │    .md       │
    └──────────────┘ └──────────────┘ └──────────────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Critic          │
                  │  (批评第 1 轮)    │
                  │  → critic_       │
                  │    round_1.md    │
                  └──────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Theorist    │ │  Comp-       │ │  Experi-     │
    │  (回应批评)   │ │  utationalist│ │  mentalist   │
    │  → 更新      │ │  (回应批评)   │ │  (回应批评)   │
    │    theorist  │ │  → 更新      │ │  → 更新      │
    │    .md       │ │    computa-  │ │    experi-   │
    │              │ │    tionalist │ │    mentalist │
    └──────────────┘ └──────────────┘ └──────────────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  第 2 轮辩论      │
                  │  (可选)          │
                  │  Critic + 回应    │
                  └──────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Coordinator     │
                  │  (综合共识)       │
                  │  → consensus_    │
                  │    plan.md       │
                  └──────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Builder         │
                  │  (执行共识方案)   │
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
                    ▼
              ┌──────────────┐
              │ Final Summary│
              │ (final_summary.md)│
              └──────────────┘
```

## 状态转换

```
debate_experts_initial
debate_critic_1
debate_experts_respond_1
debate_critic_2
debate_experts_respond_2
debate_critic_3
debate_experts_respond_3
debate_coordinator
debate_builder
debate_evaluator
debate_builder_revise_1
debate_evaluator_revise_1
debate_done
```

## 文件流

**输入：**
- `problem.md` — 物理题目

**专家分析文件：**
- `theorist.md` — 理论物理学家的分析
- `computationalist.md` — 计算物理学家的分析
- `experimentalist.md` — 实验物理学家的分析

**辩论文件：**
- `critic_round_1.md`, `critic_round_2.md`, `critic_round_3.md` — 批评

**综合文件：**
- `consensus_plan.md` — Coordinator 综合的共识计划

**求解文件：**
- `solution.md` — Builder 的完整求解
- `review.md` — Evaluator 的审查结果

**输出：**
- `final_summary.md` — 最终总结报告

## 关键特性

1. **多视角分析**：3 个专家从不同角度分析，覆盖更全面
2. **批评机制**：Critic 指出问题，提高方案质量
3. **迭代改进**：多轮辩论，逐步收敛到最优方案
4. **共识综合**：Coordinator 整合最优部分，避免单一视角的局限

## 适用场景

- 问题复杂，需要多角度分析
- 存在多种可能的解题思路，需要权衡
- 需要高质量的方案（如竞赛题、研究问题）
- 有充足的计算资源（token 预算较高）

## 辩论策略

### 第 1 轮：发散
- 专家独立分析，提出各自的观点
- Critic 指出所有问题

### 第 2 轮：收敛
- 专家回应批评，修正方案
- Critic 评估改进

### 第 3 轮（可选）：精炼
- 如果仍有 Critical 问题，继续辩论
- 否则直接进入 Coordinator

## 专家角色定义

### Theorist（理论物理学家）
- **关注点**：物理本质、对称性、守恒定律
- **优势**：理论基础扎实，能从第一性原理推导
- **局限**：可能忽视计算可行性

### Computationalist（计算物理学家）
- **关注点**：数学结构、计算方法、数值稳定性
- **优势**：擅长处理复杂的积分和方程
- **局限**：可能忽视物理直觉

### Experimentalist（实验物理学家）
- **关注点**：量级估算、极限情况、实验验证
- **优势**：物理直觉强，能快速估算
- **局限**：可能不够精确

### Critic（批评家）
- **关注点**：逻辑漏洞、物理错误、不一致
- **优势**：严谨客观，能发现隐藏问题
- **局限**：只批评不提出方案

## 终止条件

1. **辩论轮数上限**：最多 3 轮
2. **收敛判断**：如果第 2 轮后 Critic 只指出 Minor 问题，可以提前结束
3. **资源耗尽**：总 token 消耗超过预算
