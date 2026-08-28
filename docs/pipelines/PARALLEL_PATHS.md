# Parallel Paths Pipeline

**状态：** 📝 设计中  
**适用场景：** 问题有多种可能解法，需要比较选择最优方案

## 架构

```
Orchestrator
  │
  ├── Meta-Planner
  │   └── 生成 N 个不同的解题策略
  │
  ├── 并行执行（滑动窗口，最多 max_concurrent 个）
  │   ├── 策略 A: Planner A → Builder A → Evaluator A
  │   ├── 策略 B: Planner B → Builder B → Evaluator B
  │   └── 策略 C: Planner C → Builder C → Evaluator C
  │
  └── Synthesizer
      └── 比较 N 个方案，选择最优或融合
```

## Agent 角色

| Agent | 职责 | 输入 | 输出 |
|-------|------|------|------|
| **Meta-Planner** | 分析题目，生成多个不同的解题策略 | problem.md | strategies.md（N 个策略） |
| **Planner X** | 细化第 X 个策略的具体计划 | problem.md, strategy_X | plan_X.md |
| **Builder X** | 执行第 X 个计划的推导 | problem.md, plan_X.md | solution_X.md |
| **Evaluator X** | 审查第 X 个方案 | problem.md, solution_X.md, plan_X.md | review_X.md |
| **Synthesizer** | 比较 N 个方案，选择最优或融合 | 所有 solution_X.md, review_X.md | final_solution.md |
| **Orchestrator** | 协调并行执行，管理状态 | - | final_summary.md |

## 工作流

### 阶段 1：策略生成

**Meta-Planner** 分析题目，生成 2-3 个不同的解题策略：

```markdown
# strategies.md

## 策略 A：解析方法
- 方法：使用拉格朗日力学
- 优点：精确解，物理图像清晰
- 风险：方程可能复杂

## 策略 B：数值方法
- 方法：有限差分 + 数值积分
- 优点：直接，易实现
- 风险：精度依赖步长

## 策略 C：近似估算
- 方法：量纲分析 + 极限情况
- 优点：快速验证
- 风险：可能不够精确
```

### 阶段 2：并行执行

对每个策略，启动独立的 `Planner → Builder → Evaluator` 流程：

```
策略 A → Planner A → plan_A.md → Builder A → solution_A.md → Evaluator A → review_A.md
策略 B → Planner B → plan_B.md → Builder B → solution_B.md → Evaluator B → review_B.md
策略 C → Planner C → plan_C.md → Builder C → solution_C.md → Evaluator C → review_C.md
```

**并行控制：**
- 使用滑动窗口，最多同时运行 `max_concurrent_paths` 个（默认 3）
- 每个路径独立，互不干扰
- 任一路径完成，立即补入下一个（如果有）

### 阶段 3：综合评估

**Synthesizer** 收集所有方案，进行对比分析：

```markdown
# final_solution.md

## 方案对比

| 策略 | PASS/REVISE | 优点 | 缺点 | 可信度 |
|------|-------------|------|------|--------|
| A（解析） | PASS | 精确，优雅 | 计算复杂 | 高 |
| B（数值） | PASS | 直观 | 精度有限 | 中 |
| C（估算） | REVISE | 快速 | 不够准确 | 低 |

## 最终选择

选择策略 A，因为：
1. 提供了精确解析解
2. 物理图像清晰
3. Evaluator 判断为 PASS

## 交叉验证

策略 B 的数值结果与策略 A 的解析解一致（误差 < 0.1%），进一步验证了答案的正确性。

## 最终答案

[策略 A 的解答]
```

## 状态管理

`.state` 文件扩展为 JSON：

```json
{
  "stage": "parallel",
  "strategies_generated": 3,
  "completed_paths": ["A", "B"],
  "pending_paths": ["C"],
  "next": "synthesizer"
}
```

**状态转换：**
```
strategies → parallel_A → parallel_B → parallel_C → synthesizer → done
```

## Git 提交策略

| 时机 | 提交消息 |
|------|----------|
| 策略生成后 | `strategies: 3 approaches generated` |
| 路径 A 完成后 | `path_A: solution complete (PASS)` |
| 路径 B 完成后 | `path_B: solution complete (PASS)` |
| 路径 C 完成后 | `path_C: solution complete (REVISE)` |
| 综合评估后 | `synthesis: selected approach A` |
| 最终汇总 | `final: summary` |

## 输出文件

```
problem.md                    # 输入
strategies.md                 # Meta-Planner 输出
├── plan_A.md                 # Planner A 输出
├── solution_A.md             # Builder A 输出
├── review_A.md               # Evaluator A 输出
├── plan_B.md                 # Planner B 输出
├── solution_B.md             # Builder B 输出
├── review_B.md               # Evaluator B 输出
├── plan_C.md                 # Planner C 输出
├── solution_C.md             # Builder C 输出
├── review_C.md               # Evaluator C 输出
final_solution.md             # Synthesizer 输出
final_summary.md              # Orchestrator 汇总
```

## 配置参数

```json
{
  "pipeline": "parallel_paths",
  "num_strategies": 3,
  "max_concurrent_paths": 3,
  "allow_partial_results": true
}
```

## 优点

- 同时探索多种解法，提高找到最优解的概率
- 方案间可以交叉验证，增加可信度
- 某个方案失败不影响其他方案
- 适合有明确最优解的问题

## 局限

- Token 消耗高（×N）
- 如果所有策略都错误，无法自我纠正
- 不适合需要迭代探索的开放性问题

## Meta-Planner Prompt 要点

```markdown
你是 Meta-Planner，负责分析问题并生成多个不同的解题策略。

要求：
1. 生成 2-3 个本质不同的策略（不是同一方法的小变体）
2. 每个策略包含：方法描述、优点、风险、适用条件
3. 策略之间应该有互补性（如：解析 vs 数值，精确 vs 近似）
4. 考虑问题的物理本质，选择最合适的数学工具

输出格式：strategies.md
```

## Synthesizer Prompt 要点

```markdown
你是 Synthesizer，负责比较多个解题方案并选择最优。

评估标准：
1. 物理正确性（量纲、极限情况、守恒律）
2. 数学严谨性（推导完整、无跳步）
3. 答案一致性（多个方案是否给出相同结果）
4. 简洁性和优雅性

输出：
- 方案对比表
- 最终选择的方案及理由
- 交叉验证结果（如果多个方案一致，增加可信度）
```

## 实现注意事项

1. **并行执行**：复用现有的滑动窗口机制，但改为管理多个路径而非多个题目
2. **状态恢复**：如果中断，从 `.state` 中恢复已完成的路径，继续未完成的路径
3. **资源限制**：每个路径有独立的 token 预算，避免某个路径耗尽资源
4. **失败处理**：如果某个路径失败（如 Builder 超时），记录失败原因，继续其他路径
