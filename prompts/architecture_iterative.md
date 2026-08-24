# Iterative Architecture

## 流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator                              │
│  (读取 problem.md, 管理迭代循环, 维护 exploration_history)   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  初始化          │
                  │  - 创建 exploration_history.md
                  │  - 设置 iteration = 0
                  └──────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │  迭代循环开始           │
              │  iteration < max?       │
              └─────────────────────────┘
                       │
            ┌──────────┴──────────┐
            │                     │
           Yes                    No
            │                     │
            ▼                     ▼
  ┌──────────────────┐    ┌──────────────┐
  │  Explorer        │    │  总结阶段    │
  │  (提出假设)       │    │  → final_summary.md
  │  → hypothesis.md │    └──────────────┘
  └──────────────────┘
            │
            ▼
  ┌──────────────────┐
  │  Builder         │
  │  (验证假设)       │
  │  → experiment.md │
  └──────────────────┘
            │
            ▼
  ┌──────────────────┐
  │  Evaluator       │
  │  (评估进展)       │
  │  → assessment.md │
  └──────────────────┘
            │
            ▼
  ┌──────────────────┐
  │  更新历史        │
  │  → exploration_history.md
  └──────────────────┘
            │
            ▼
    ┌───────┴───────┬──────────────┐
    │               │              │
    ▼               ▼              ▼
  PASS           PARTIAL       DEAD_END
    │               │              │
    │               │              └──→ 记录失败
    │               │                     (可选回溯)
    │               │
    │               └──→ iteration++
    │                    回到 Explorer
    │
    ▼
┌──────────────┐
│ 生成 solution │
│ (基于成功的实验)
└──────────────┘
```

## 状态转换

```
iterative_init
iterative_explorer_1
iterative_builder_1
iterative_evaluator_1
iterative_explorer_2
iterative_builder_2
iterative_evaluator_2
...
iterative_explorer_N
iterative_builder_N
iterative_evaluator_N
iterative_done
```

## 文件流

**输入：**
- `problem.md` — 物理题目

**累积文件：**
- `exploration_history.md` — 探索历史（每次迭代追加）

**每次迭代文件（覆盖）：**
- `hypothesis.md` — 当前假设
- `experiment.md` — 当前实验结果
- `assessment.md` — 当前评估

**输出：**
- `solution.md` — 最终求解（基于成功的假设链）
- `final_summary.md` — 最终总结报告

## 评估状态

Evaluator 在 assessment.md 第一行输出以下状态之一：

### PASS
- 假设验证成功
- 实验结果正确且完整
- 可以生成最终 solution

### PARTIAL
- 假设有部分进展
- 但仍有未解决的问题
- 需要继续迭代

### DEAD_END
- 假设验证失败
- 当前路径无法继续
- 需要回溯或换方向

## 关键特性

1. **渐进式探索**：每次迭代基于之前的经验
2. **历史积累**：exploration_history.md 记录所有尝试，避免重复
3. **灵活调整**：根据 Evaluator 反馈动态调整策略
4. **失败容忍**：DEAD_END 不是终点，可以回溯到新分支

## 适用场景

- 问题需要逐步逼近（如复杂积分、多步骤推导）
- 不确定最佳切入点
- 需要从失败中学习并调整策略
- 问题有多个子问题需要逐个击破

## 迭代策略

### 早期迭代（1-2）
- 尝试大方向（如不同的建模方法）
- 探索多种可能性

### 中期迭代（3-4）
- 基于 PARTIAL 结果细化
- 解决具体的技术难点

### 后期迭代（5+）
- 收敛到最终方案
- 处理细节和边界情况

## 终止条件

1. **成功终止**：Evaluator 输出 PASS
2. **迭代上限**：达到 max_iterations（默认 5）
3. **资源耗尽**：总迭代次数超过 max_iterations * 2（含回溯）
