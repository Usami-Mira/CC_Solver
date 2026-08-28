# Iterative Exploration Pipeline

**状态：** 📝 设计中  
**适用场景：** 开放性问题，需要通过实验和迭代逐步逼近答案

## 架构

```
Orchestrator
  │
  └── 迭代循环（最多 max_iterations 次）
      │
      ├── Explorer
      │   └── 分析当前状态，提出假设和实验方案
      │
      ├── Builder
      │   └── 执行实验/计算，验证假设
      │
      ├── Evaluator
      │   └── 评估进展，判断方向
      │       ├── "有希望" → 继续细化
      │       ├── "死胡同" → 回退，尝试新方向
      │       └── "部分成功" → 提取有用部分
      │
      └── Explorer 根据反馈调整策略
```

## Agent 角色

| Agent | 职责 | 输入 | 输出 |
|-------|------|------|------|
| **Explorer** | 分析问题，提出假设，制定实验方案 | problem.md, exploration_history.md | hypothesis.md, experiment_plan.md |
| **Builder** | 执行实验/计算，验证假设 | hypothesis.md, experiment_plan.md | experiment_result.md |
| **Evaluator** | 评估实验结果，判断方向 | hypothesis.md, experiment_result.md | assessment.md |
| **Orchestrator** | 管理迭代循环，更新探索历史 | - | final_summary.md |

## 工作流

### 核心循环

```
迭代 1:
  Explorer → hypothesis_1.md（"我猜想系统是谐振子..."）
  Builder → experiment_1.md（数值模拟验证）
  Evaluator → assessment_1.md（"有希望，但阻尼项未考虑"）
  
迭代 2:
  Explorer → hypothesis_2.md（"加入阻尼，修正模型..."）
  Builder → experiment_2.md（修正后的模拟）
  Evaluator → assessment_2.md（"结果合理，但与实验数据有偏差"）
  
迭代 3:
  Explorer → hypothesis_3.md（"可能是非线性效应..."）
  Builder → experiment_3.md（非线性模型）
  Evaluator → assessment_3.md（"PASS，与实验一致"）
```

### 详细流程

**1. Explorer 阶段**

分析当前探索状态，提出下一步假设：

```markdown
# hypothesis_2.md

## 当前状态回顾

- 迭代 1：谐振子模型，未考虑阻尼，预测振幅不衰减
- 评估：方向正确，但忽略了能量耗散

## 新假设

系统应该是一个阻尼谐振子，阻尼力与速度成正比：
$$F_{damping} = -\gamma v$$

## 预期结果

加入阻尼后，振幅应指数衰减：
$$A(t) = A_0 e^{-\gamma t / 2m}$$

## 实验方案

1. 用数值方法求解阻尼谐振子方程
2. 拟合衰减曲线，提取 $\gamma$
3. 与实验数据对比
```

**2. Builder 阶段**

执行实验，验证假设：

```markdown
# experiment_2.md

## 实验执行

使用 scipy.integrate.solve_ivp 求解阻尼谐振子：

```python
import numpy as np
from scipy.integrate import solve_ivp

def damped_oscillator(t, y, gamma, k, m):
    x, v = y
    dxdt = v
    dvdt = -(k/m)*x - (gamma/m)*v
    return [dxdt, dvdt]

# 参数
m = 1.0
k = 10.0
gamma = 0.5

# 初始条件
y0 = [1.0, 0.0]

# 求解
sol = solve_ivp(damped_oscillator, [0, 10], y0, 
                args=(gamma, k, m), dense_output=True)

# 拟合衰减包络
t = np.linspace(0, 10, 100)
x = sol.sol(t)[0]
envelope = np.exp(-gamma*t/(2*m))

# 结果
print(f"衰减率 γ = {gamma}")
print(f"拟合误差 < 1%")
```

## 实验结果

- 阻尼模型与数值模拟一致
- 衰减率 $\gamma = 0.5 \pm 0.01$
- 但与实验数据对比，前 3 个周期吻合，后期偏差增大

## 观察

可能还存在其他效应（如非线性项）
```

**3. Evaluator 阶段**

评估进展，给出方向判断：

```markdown
# assessment_2.md

## 评估结果：部分成功

### 进展

✅ 阻尼模型在短期（前 3 个周期）与实验一致  
✅ 衰减率的量级正确  
❌ 长期行为（5 个周期后）偏差明显  

### 分析

偏差可能来自：
1. 阻尼力不是线性（可能是 $v^2$ 或其他形式）
2. 弹簧刚度随位移变化（非线性）
3. 测量误差累积

### 建议方向

- **继续当前路径**：尝试非线性阻尼模型
- **回退**：重新检查实验数据的可靠性
- **分支**：同时探索非线性弹簧和非线性阻尼

## 判断：继续细化，尝试非线性阻尼
```

**4. 迭代决策**

Orchestrator 根据 Evaluator 的判断决定下一步：

```python
if assessment.startswith("PASS"):
    # 成功，结束迭代
    write_final_summary()
    break
elif assessment.startswith("DEAD_END"):
    # 死胡同，回退到上一个分支点
    rollback_to_checkpoint()
elif assessment.startswith("PARTIAL"):
    # 部分成功，继续迭代
    continue_iteration()
elif iteration_count >= max_iterations:
    # 达到最大迭代次数
    write_best_effort_summary()
    break
```

## 状态管理

`.state` 文件扩展为 JSON：

```json
{
  "stage": "iteration",
  "current_iteration": 2,
  "max_iterations": 5,
  "exploration_history": [
    {
      "iteration": 1,
      "hypothesis": "harmonic_oscillator",
      "assessment": "PARTIAL",
      "key_findings": "未考虑阻尼"
    },
    {
      "iteration": 2,
      "hypothesis": "damped_oscillator",
      "assessment": "PARTIAL",
      "key_findings": "短期吻合，长期偏差"
    }
  ],
  "next": "explorer"
}
```

## 探索历史文件

维护 `exploration_history.md`，记录所有迭代：

```markdown
# 探索历史

## 迭代 1：谐振子模型

**假设**：系统是简谐振子  
**实验**：数值求解 $m\ddot{x} + kx = 0$  
**结果**：振幅不衰减，与实验不符  
**评估**：方向正确，但忽略能量耗散  
**关键发现**：需要考虑阻尼  

---

## 迭代 2：阻尼谐振子模型

**假设**：加入线性阻尼 $F_{damping} = -\gamma v$  
**实验**：求解 $m\ddot{x} + \gamma\dot{x} + kx = 0$  
**结果**：短期（3 周期）吻合，长期偏差  
**评估**：部分成功  
**关键发现**：可能是非线性效应  

---

## 迭代 3：非线性阻尼模型

**假设**：阻尼力与 $v^2$ 成正比  
**实验**：...  
**结果**：...  
**评估**：PASS  
**关键发现**：最终模型为 $m\ddot{x} + \gamma\dot{x}^2 + kx = 0$
```

## Git 提交策略

| 时机 | 提交消息 |
|------|----------|
| 迭代 1 - Explorer | `iter1: hypothesis - harmonic oscillator` |
| 迭代 1 - Builder | `iter1: experiment - numerical solution` |
| 迭代 1 - Evaluator | `iter1: assessment - PARTIAL, need damping` |
| 迭代 2 - Explorer | `iter2: hypothesis - damped oscillator` |
| 迭代 2 - Builder | `iter2: experiment - damped solution` |
| 迭代 2 - Evaluator | `iter2: assessment - PARTIAL, long-term deviation` |
| 迭代 3 - Explorer | `iter3: hypothesis - nonlinear damping` |
| 迭代 3 - Builder | `iter3: experiment - nonlinear solution` |
| 迭代 3 - Evaluator | `iter3: assessment - PASS` |
| 最终汇总 | `final: summary after 3 iterations` |

## 输出文件

```
problem.md                      # 输入
exploration_history.md          # 探索历史（累积更新）
├── hypothesis_1.md             # 迭代 1：Explorer
├── experiment_1.md             # 迭代 1：Builder
├── assessment_1.md             # 迭代 1：Evaluator
├── hypothesis_2.md             # 迭代 2：Explorer
├── experiment_2.md             # 迭代 2：Builder
├── assessment_2.md             # 迭代 2：Evaluator
├── hypothesis_3.md             # 迭代 3：Explorer
├── experiment_3.md             # 迭代 3：Builder
├── assessment_3.md             # 迭代 3：Evaluator
final_solution.md               # 最终方案
final_summary.md                # 汇总
```

## 配置参数

```json
{
  "pipeline": "iterative",
  "max_iterations": 5,
  "allow_backtracking": true,
  "checkpoint_interval": 2
}
```

## Explorer Prompt 要点

```markdown
你是 Explorer，负责提出假设和设计实验方案。

核心能力：
1. 分析当前探索状态，识别知识缺口
2. 提出可验证的假设
3. 设计实验/计算方案来验证假设
4. 根据反馈调整策略

输出要求：
- 明确假设（可证伪）
- 实验方案可执行（用 Python/数值方法）
- 预期结果清晰
- 说明如何判断假设是否成立

避免：
- 重复已尝试过的方向
- 提出无法验证的假设
- 忽略之前的关键发现
```

## Evaluator Prompt 要点

```markdown
你是 Evaluator，负责评估实验进展并给出方向判断。

评估维度：
1. 假设是否得到验证？
2. 结果是否与已知物理一致？
3. 相比上一次迭代，进展如何？
4. 当前路径是否还有潜力？

输出格式：
- 首行：PASS / PARTIAL / DEAD_END
- 进展总结
- 关键发现
- 下一步建议（继续/回退/分支）

重要：
- 如果方向明显错误，及时标记 DEAD_END
- 如果有部分进展，提取有用信息
- 避免无限循环（重复相同错误）
```

## 优点

- 模拟真实研究过程（假设-实验-评估循环）
- 可以逐步逼近答案，不需要一次性猜对
- 保留完整的探索历史，可追溯
- 适合开放性问题

## 局限

- 迭代次数可能很多，耗时长
- 需要 Explorer 有良好的策略调整能力
- 可能陷入局部最优（需要回退机制）
- 不适合有明确标准解法的问题

## 与 Standard Pipeline 的区别

| 特性 | Standard | Iterative |
|------|----------|-----------|
| 目标 | 找到正确答案 | 逐步逼近答案 |
| 流程 | 线性（最多 1 次 REVISE） | 循环（多次迭代） |
| Planner 角色 | 制定完整计划 | Explorer 动态调整 |
| 失败处理 | REVISE 修正 | 回退/换方向 |
| 适用问题 | 已知解法 | 开放性问题 |
