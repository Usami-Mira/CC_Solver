# Tree Search Pipeline

**状态：** 📝 设计中  
**适用场景：** 前沿研究问题，高度不确定，需要系统性探索

## 架构

```
Orchestrator
  │
  └── Strategist（决策者）
      │
      ├── 工具 1: expand_tree() — 展开新分支
      ├── 工具 2: call_validator() — 快速理论验证（仅供参考）
      ├── 工具 3: call_builder() — 完整计算
      └── 工具 4: backtrack() — 回溯到上一节点
      │
      └── 探索完成后
          └── Standard 流程：Builder → Evaluator（执行最终方案）
```

## Agent 角色

| Agent | 职责 | 权限 |
|-------|------|------|
| **Strategist** | 探索策略的决策者和协调者 | 可调用 Validator、Builder，可展开树、可回溯 |
| **Validator** | 快速理论验证（量纲、极限、守恒律） | 只提供建议，Strategist 可以覆盖 |
| **Builder** | 完整推导和计算 | 执行 Strategist 指定的策略 |
| **Evaluator** | 审查最终方案 | 标准审查 |

## 工作流

### 核心循环

```
Strategist 决策循环：
  │
  ├── 观察当前状态（探索树 + 历史记录）
  │
  ├── 选择行动：
  │   ├── expand_tree() — 生成新分支
  │   ├── call_validator(strategy) — 快速验证
  │   ├── call_builder(strategy) — 完整计算
  │   └── backtrack() — 回溯
  │
  ├── 执行行动，观察结果
  │
  ├── 判断是否找到可行方案：
  │   ├── 是 → 退出循环，进入 standard 流程
  │   └── 否 → 继续决策循环
  │
  └── 检查终止条件：
      ├── 找到方案 → 成功退出
      ├── 所有分支耗尽 → 失败退出
      └── 达到最大迭代次数 → 返回最佳尝试
```

### 详细流程示例

**迭代 1：初始探索**
```
Strategist: "问题复杂，先生成高层策略"
  → expand_tree()
  → 生成: [A: 解析方法, B: 数值方法, C: 近似估算]

Strategist: "先看看解析方法"
  → call_validator(A)
  → Validator: "PROMISING - 量纲正确，但方程可能复杂"

Strategist: "值得深入，展开子策略"
  → expand_tree(A)
  → 生成: [A1: 分离变量, A2: 微扰论, A3: 变分法]
```

**迭代 2：细化探索**
```
Strategist: "试试分离变量"
  → call_validator(A1)
  → Validator: "DEAD_END - 变量不可分离"

Strategist: "同意，换一个。微扰论如何？"
  → call_validator(A2)
  → Validator: "UNCERTAIN - 需要看微扰参数大小"

Strategist: "不确定就直接算"
  → call_builder(A2)
  → Builder: "一阶微扰结果偏差 15%，不够精确"

Strategist: "需要二阶修正"
  → expand_tree(A2)
  → 生成: [A2a: 二阶微扰, A2b: 改进微扰论]
```

**迭代 3：深入计算**
```
Strategist: "试试二阶微扰"
  → call_builder(A2a)
  → Builder: "二阶修正后偏差 < 2%，与实验一致"

Strategist: "找到可行方案！退出探索"
  → 将 A2a 的策略交给 standard 流程
```

**Standard 流程执行**
```
Builder: 基于 A2a 策略，完整推导
Evaluator: 审查最终方案
输出: final_solution.md
```

## Strategist 的决策逻辑

```markdown
# Strategist Prompt

你是 Strategist，负责系统性探索解题策略。

## 可用工具

1. **expand_tree([parent])** — 展开新分支
   - 无参数：生成高层策略（2-3 个）
   - 有参数：为指定节点生成子策略

2. **call_validator(strategy)** — 快速理论验证
   - 返回：PROMISING / DEAD_END / UNCERTAIN
   - 仅供参考，你可以不同意

3. **call_builder(strategy)** — 完整计算
   - 用于：需要深入验证时
   - 成本较高，谨慎使用

4. **backtrack()** — 回溯到上一个分支点
   - 用于：当前路径明显走不通

## 决策原则

1. **先广后深**：先生成高层策略，再逐步细化
2. **快速筛选**：优先用 Validator 快速排除明显不可行的
3. **灵活覆盖**：Validator 的意见是参考，你可以调用 Builder 覆盖
4. **避免死循环**：同一分支最多尝试 3 次
5. **及时回溯**：如果连续失败，考虑换大方向

## 输出格式

每次决策输出：
```json
{
  "observation": "当前状态描述",
  "action": "expand_tree / call_validator / call_builder / backtrack",
  "parameters": {"strategy": "A2"},
  "reasoning": "为什么做这个选择"
}
```

## 终止条件

- 找到可行方案（Builder 验证通过）
- 所有分支都已探索且失败
- 达到最大迭代次数（配置项）

找到可行方案后，输出最终策略描述，交给 standard 流程执行。
```

## 状态管理

```json
{
  "stage": "tree_search",
  "tree": {
    "root": "problem_X",
    "children": [
      {
        "id": "A",
        "name": "解析方法",
        "status": "exploring",
        "children": [
          {"id": "A1", "status": "pruned", "reason": "不可分离"},
          {
            "id": "A2", 
            "status": "exploring",
            "children": [
              {"id": "A2a", "status": "success", "solution": "..."},
              {"id": "A2b", "status": "pending"}
            ]
          },
          {"id": "A3", "status": "pending"}
        ]
      },
      {"id": "B", "status": "pending"},
      {"id": "C", "status": "pending"}
    ]
  },
  "current_path": ["root", "A", "A2", "A2a"],
  "backtrack_stack": [],
  "iteration_count": 7,
  "max_iterations": 20,
  "next": "standard_execution"
}
```

## 探索历史文件

维护 `exploration_tree.md`，记录完整探索过程：

```markdown
# 探索树

## 根节点
问题：[问题描述]

---

## 分支 A：解析方法

### 快速验证
- Validator: PROMISING
- 理由：量纲正确，但方程复杂

### 子分支 A1：分离变量
- Validator: DEAD_END
- 原因：变量不可分离
- **已剪枝**

### 子分支 A2：微扰论
- Validator: UNCERTAIN
- 原因：需看微扰参数

#### 完整计算（一阶）
- Builder: 偏差 15%，不够精确
- 决策：需要二阶修正

#### 子子分支 A2a：二阶微扰
- Builder: 偏差 < 2%，与实验一致
- **✅ 成功**

---

## 最终选择

策略 A2a（二阶微扰论）

理由：
1. 解析解形式清晰
2. 精度满足要求（< 2%）
3. 物理图像明确

下一步：交给 standard 流程完整执行
```

## Git 提交策略

| 时机 | 提交消息 |
|------|----------|
| 初始树生成 | `tree: 3 strategies generated` |
| 展开分支 A | `tree: expanded branch A (analytical)` |
| 验证 A1 失败 | `tree: pruned A1 (not separable)` |
| 验证 A2 不确定 | `tree: A2 uncertain, need full computation` |
| Builder 验证 A2 | `tree: A2 first-order insufficient` |
| 展开 A2 | `tree: expanded A2 (perturbation refinements)` |
| Builder 验证 A2a 成功 | `tree: A2a success - second-order perturbation` |
| 探索完成 | `exploration: selected A2a after 7 iterations` |
| Standard 流程 - Builder | `solution: based on A2a strategy` |
| Standard 流程 - Evaluator | `review: final assessment` |
| 最终汇总 | `final: summary` |

## 输出文件

```
problem.md                          # 输入

# 探索阶段
├── exploration_tree.md             # 探索树（累积更新）
├── iteration_1_expand.md           # 迭代 1：生成初始树
├── iteration_2_validate_A.md       # 迭代 2：验证分支 A
├── iteration_3_expand_A.md         # 迭代 3：展开 A 的子策略
├── iteration_4_validate_A1.md      # 迭代 4：验证 A1（失败）
├── iteration_5_validate_A2.md      # 迭代 5：验证 A2（不确定）
├── iteration_6_build_A2.md         # 迭代 6：完整计算 A2
├── iteration_7_expand_A2.md        # 迭代 7：展开 A2
├── iteration_8_build_A2a.md        # 迭代 8：完整计算 A2a（成功）
├── final_strategy.md               # 最终选择的策略

# Standard 执行阶段
├── plan.md                         # 基于 final_strategy.md
├── solution.md                     # Builder 完整推导
├── review.md                       # Evaluator 审查
└── final_summary.md                # 汇总
```

## 配置参数

```json
{
  "pipeline": "tree_search",
  "max_iterations": 20,
  "max_tree_depth": 4,
  "max_branches_per_node": 5,
  "auto_backtrack_after_failures": 3
}
```

## 启发式排序（选择下一个分支）

Strategist 在选择下一个要探索的分支时，可以使用启发式：

```python
def prioritize_branches(branches):
    """根据启发式排序分支"""
    scored_branches = []
    for branch in branches:
        score = 0
        
        # 启发式 1：Validator 的意见
        if branch.validator_result == "PROMISING":
            score += 10
        elif branch.validator_result == "UNCERTAIN":
            score += 5
        elif branch.validator_result == "DEAD_END":
            score -= 10
        
        # 启发式 2：物理直觉
        if branch.method in ["analytical", "perturbation"]:
            score += 3  # 解析方法优先
        elif branch.method in ["numerical"]:
            score += 1
        
        # 启发式 3：探索成本
        if branch.estimated_cost == "low":
            score += 2
        elif branch.estimated_cost == "high":
            score -= 2
        
        scored_branches.append((score, branch))
    
    return sorted(scored_branches, reverse=True)
```

## Strategist 调用工具的接口

```python
# Strategist 输出 JSON，Orchestrator 解析并调用对应 Agent

# 示例 1：展开树
{
  "action": "expand_tree",
  "parameters": {"parent": "A2"}
}
# → Orchestrator 调用 Strategist 生成子策略

# 示例 2：调用 Validator
{
  "action": "call_validator",
  "parameters": {"strategy": "A2a"}
}
# → Orchestrator spawn Validator Agent

# 示例 3：调用 Builder
{
  "action": "call_builder",
  "parameters": {"strategy": "A2a"}
}
# → Orchestrator spawn Builder Agent

# 示例 4：回溯
{
  "action": "backtrack"
}
# → Orchestrator 更新当前路径，返回上一节点
```

## 与 Standard 流程的衔接

探索完成后，Strategist 输出最终策略：

```markdown
# final_strategy.md

## 选择的策略

**策略 ID**: A2a  
**方法**: 二阶微扰论

## 策略描述

1. 将问题写为 $H = H_0 + \lambda V$
2. 求解 $H_0$ 的本征态（零阶近似）
3. 计算一阶修正 $\langle n | V | n \rangle$
4. 计算二阶修正 $\sum_{m \neq n} \frac{|\langle m | V | n \rangle|^2}{E_n - E_m}$
5. 验证收敛性（$\lambda \ll 1$）

## 关键参数

- 微扰参数：$\lambda = 0.1$
- 零阶能量：$E_0 = 10.5$ eV
- 一阶修正：$\Delta E_1 = 0.8$ eV
- 二阶修正：$\Delta E_2 = 0.2$ eV

## 预期精度

总能量 $E = E_0 + \Delta E_1 + \Delta E_2 = 11.5 \pm 0.2$ eV

## 下一步

交给 Builder 执行完整推导，包含所有计算步骤。
```

然后 Orchestrator 启动 standard 流程：
- Planner：基于 `final_strategy.md` 生成 `plan.md`
- Builder：执行 `plan.md`，生成 `solution.md`
- Evaluator：审查 `solution.md`，生成 `review.md`

## 优点

- 系统性探索，不会遗漏可能的解法
- 分层验证，节省计算资源
- Strategist 有完全自主权，可以灵活决策
- 保留完整探索历史，可追溯和复盘
- 适合高度不确定的前沿问题

## 局限

- 探索过程可能很长（需要多次迭代）
- Strategist 的决策质量直接影响效率
- 状态管理复杂（树结构 + 探索历史）
- Token 消耗可变（取决于探索深度）

## 与其他 Pipeline 的对比

| 特性 | Standard | Parallel | Iterative | Debate | Tree Search |
|------|----------|----------|-----------|--------|-------------|
| 探索方式 | 无 | 并行 N 个 | 循环迭代 | 多专家 | 树状搜索 |
| 决策者 | Planner | Meta-Planner | Explorer | Coordinator | Strategist |
| 回溯能力 | 无 | 无 | 有 | 无 | 有 |
| 验证深度 | 完整 | 完整 | 完整 | 完整 | 分层 |
| 适用问题 | 已知解法 | 多解法 | 开放性 | 跨领域 | 高度不确定 |

## 实现注意事项

1. **树的持久化**：探索树需要持久化到 JSON 文件，支持断点续传
2. **Strategist 的上下文**：每次决策时，需要传入完整探索历史
3. **工具调用解析**：Orchestrator 需要解析 Strategist 的 JSON 输出，调用对应 Agent
4. **终止保护**：设置最大迭代次数，防止无限探索
5. **最佳努力返回**：如果所有分支都失败，返回最接近成功的尝试
