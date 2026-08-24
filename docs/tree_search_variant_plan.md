# Tree Search Variant: Planner-Driven with Ephemeral Builder-Evaluator Pairs

## 核心思想

**现有 Tree Search 的问题：** Strategist 只能通过 JSON 决策，无法真正"计算"东西来辅助判断。很多时候需要实际算一下某个小结论，才能决定下一步方向。

**新结构：** Planner 掌控大局，可以调用短暂的 Builder-Evaluator 对来计算和验证小结论，每个计算都经过验证，最后形成完整方案。

## Architecture

```
Planner (决策者 + 主控)
  ├─→ 思考：需要计算什么来辅助决策？
  ├─→ spawn Ephemeral Builder
  │     计算某个小结论（如：某个积分的值、某个极限情况）
  │     写入 calculation_{id}.md
  ├─→ spawn Ephemeral Evaluator
  │     验证计算是否正确
  │     写入 verification_{id}.md（PASS / FAIL）
  ├─→ 如果 FAIL → 让 Builder 修正或换个方法
  ├─→ 如果 PASS → 继续思考，决定下一步
  └─→ 最终：形成完整方案 → spawn Final Builder → Final Evaluator
```

## 与现有 Tree Search 的区别

| 特性 | 现有 Tree Search | 新变体 |
|------|-----------------|--------|
| 决策者 | Strategist（只输出 JSON） | Planner（可以计算东西） |
| 计算能力 | 只能调用 Builder 完整求解 | 可以调用 Builder 计算小结论 |
| 验证时机 | 只在最终验证 | 每次计算都验证 |
| 状态管理 | 复杂的树结构 JSON | 简单的计算历史列表 |
| 灵活性 | 受限于预定义 action | 自由决定需要计算什么 |

## Agent 角色

### Planner（主控 + 决策者）
**职责：**
- 读取 problem.md
- 分析题目，决定需要计算哪些小结论来辅助决策
- 为每个小结论 spawn Builder-Evaluator 对
- 根据计算结果调整策略
- 最终形成完整方案，spawn Final Builder

**输入：** problem.md + calculations_history.md
**输出：** strategy.md（思考过程 + 决策）+ final_plan.md（最终方案）

### Ephemeral Builder（临时计算者）
**职责：**
- 读取 Planner 的计算任务
- 执行具体计算（积分、极限、数值验证等）
- 写入 calculation_{id}.md

**输入：** problem.md + task_{id}.md（Planner 写的计算任务）
**输出：** calculation_{id}.md

### Ephemeral Evaluator（临时验证者）
**职责：**
- 验证 Builder 的计算是否正确
- 快速判断 PASS / FAIL

**输入：** problem.md + calculation_{id}.md
**输出：** verification_{id}.md（第一行：PASS / FAIL）

### Final Builder（最终求解者）
**职责：**
- 读取 Planner 的最终方案
- 执行完整推导
- 写入 solution.md

### Final Evaluator（最终审查者）
**职责：**
- 审查完整 solution
- 判断是否需要修正

## 工作流程

### 阶段 1：Planner 分析 + 计算循环

**主循环（最多 max_iterations 次）：**

1. **Planner 思考**
   - 读取 problem.md + calculations_history.md
   - 分析：还需要计算什么？
   - 写入 strategy.md：
     ```markdown
     # 当前思考
     
     ## 已知信息
     - [从之前的计算中学到的]
     
     ## 下一步计划
     - 需要计算：[描述]
     - 目的：[为什么需要这个]
     
     ## 计算任务
     写入 task_{id}.md
     ```
   
2. **Spawn Ephemeral Builder**
   - 创建 task_{id}.md："计算 [具体内容]"
   - spawn Builder，写入 calculation_{id}.md
   - 超时：300s（小计算不应该太久）

3. **Spawn Ephemeral Evaluator**
   - spawn Evaluator，验证 calculation_{id}.md
   - 写入 verification_{id}.md
   - 读取第一行：PASS / FAIL

4. **处理结果**
   - PASS → 追加到 calculations_history.md，继续循环
   - FAIL → 让 Builder 修正（最多重试 1 次）或放弃这个计算

5. **Planner 判断是否足够**
   - 如果信息足够 → 写入 final_plan.md，退出循环
   - 如果不够 → 继续循环

### 阶段 2：Final Builder 执行

- 读取 problem.md + final_plan.md
- 执行完整推导
- 写入 solution.md

### 阶段 3：Final Evaluator 审查

- 读取 problem.md + solution.md
- 写入 review.md（PASS / REVISE）
- 如果 REVISE → Builder 修正（最多 2 次）

### 阶段 4：总结

- 生成 final_summary.md
- 包含：问题、答案、计算历史、审查结论

## 状态管理

### calculations_history.md

```markdown
# 计算历史

## Calculation 1
**任务：** 计算 $\int_0^{2\pi} \frac{d\phi}{\sqrt{r^2+R^2-2rR\cos\phi}}$
**结果：** $\frac{4}{r+R} K\left(\frac{4rR}{(r+R)^2}\right)$
**验证：** PASS

## Calculation 2
**任务：** 验证 $r \to 0$ 极限
**结果：** $W \to \frac{Q^2}{8\pi\epsilon_0 R}$（球壳结果）
**验证：** PASS

...
```

### strategy.md（每次迭代更新）

```markdown
# 当前策略

## 迭代 3

### 已知信息
- 角度积分给出椭圆积分 $K(m)$
- $r \to 0$ 极限正确
- $r \to R$ 时 $K(m) \to \infty$（对数发散）

### 下一步
- 需要计算径向积分 $\int_0^R r' K(m) dr'$
- 可能需要数值方法

### 计算任务
写入 task_3.md
```

## 文件结构

```
{workspace}/
├── problem.md
├── strategy.md（Planner 思考过程）
├── task_1.md, task_2.md, ...（计算任务）
├── calculation_1.md, calculation_2.md, ...（计算结果）
├── verification_1.md, verification_2.md, ...（验证结果）
├── calculations_history.md（汇总）
├── final_plan.md（最终方案）
├── solution.md（完整求解）
├── review.md（最终审查）
└── final_summary.md（总结）
```

## 优势

1. **更灵活的决策**：Planner 可以计算东西来辅助判断，不只是"猜测"
2. **更高的可靠性**：每个小计算都经过验证，避免错误累积
3. **更清晰的思路**：Planner 的思考过程显式记录在 strategy.md
4. **更好的调试**：如果最终答案错误，可以回溯看哪个小计算出错

## 实现挑战

1. **Planner 的 prompt 设计**：需要教会 Planner 何时需要计算、计算什么
2. **任务描述格式**：task_{id}.md 需要有清晰的格式，让 Builder 知道要算什么
3. **迭代次数控制**：避免 Planner 无限循环计算
4. **计算粒度**：太小的计算浪费时间，太大的计算失去意义

## Prompt 文件清单

1. `prompts/orchestrator_tree_search_v2.md` - 编排逻辑（~120 行）
2. `prompts/planner_tree_search.md` - Planner prompt（~80 行）
3. `prompts/builder_ephemeral.md` - 临时 Builder（~40 行）
4. `prompts/evaluator_ephemeral.md` - 临时 Evaluator（~30 行）
5. `prompts/architecture_tree_search_v2.md` - 流程图（~40 行）

**总计：~310 行**

## 示例流程（带电圆盘）

```
Planner 迭代 1:
  思考：需要知道角度积分的结果
  任务：计算 $\int_0^{2\pi} \frac{d\phi}{\sqrt{a - b\cos\phi}}$
  Builder → calculation_1.md: $\frac{4}{\sqrt{a+b}} K\left(\frac{2b}{a+b}\right)$
  Evaluator → PASS

Planner 迭代 2:
  思考：需要验证极限情况
  任务：计算 $r \to 0$ 时 $K(m)$ 的行为
  Builder → calculation_2.md: $K(m) \to \frac{\pi}{2}$
  Evaluator → PASS

Planner 迭代 3:
  思考：需要知道径向积分是否可解析
  任务：尝试解析计算 $\int_0^R r' K\left(\frac{4rR}{(r+R)^2}\right) dr'$
  Builder → calculation_3.md: 无法解析，建议数值方法
  Evaluator → PASS

Planner 迭代 4:
  思考：信息足够，形成最终方案
  写入 final_plan.md: 使用数值积分，SciPy quad

Final Builder → solution.md
Final Evaluator → PASS
```

## 实施建议

1. **先实现最小版本**：只做 1-2 次迭代，验证可行性
2. **逐步扩展**：添加更多计算类型、更复杂的决策逻辑
3. **对比测试**：用同一道题测试现有 Tree Search 和新变体，比较效果
4. **调参**：调整 max_iterations、Builder/Evaluator 超时时间等

## 不实施的原因

- 现有 5 种 pipeline 已经足够覆盖常见场景
- 新变体复杂度较高，需要更多测试
- 可以先观察现有 Tree Search 的实际表现，再决定是否实现
- 用户可以手动选择现有 pipeline，不需要自动选择最优 pipeline
