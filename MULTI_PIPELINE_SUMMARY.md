# Multi-Pipeline Architecture - Implementation Summary

## Overview

Successfully implemented 4 alternative pipeline strategies for the physics problem-solving agent system, in addition to the existing Standard pipeline.

## Implemented Pipelines

### 1. Standard (原有)
- **流程**: Planner → Builder → Evaluator
- **适用场景**: 简单直接的物理问题
- **Token 消耗**: 低

### 2. Parallel Paths (新增)
- **流程**: 3个 Planner 并行 → Meta-Planner 选择 → Builder → Evaluator
- **适用场景**: 问题有多种可能解法，需要探索创新思路
- **Token 消耗**: 中-高
- **文件**: orchestrator_parallel.md, meta_planner.md, architecture_parallel.md

### 3. Iterative (新增)
- **流程**: Explorer 提出假设 → Builder 验证 → Evaluator 评估 → 循环迭代
- **适用场景**: 需要逐步逼近的复杂问题
- **Token 消耗**: 中
- **文件**: orchestrator_iterative.md, explorer.md, architecture_iterative.md

### 4. Debate (新增)
- **流程**: 3个专家并行分析 → 辩论循环(2-3轮) → Coordinator 综合 → Builder → Evaluator
- **适用场景**: 复杂问题需要多角度分析
- **Token 消耗**: 高
- **文件**: orchestrator_debate.md, 4个专家 prompt, coordinator.md, architecture_debate.md

### 5. Tree Search (新增)
- **流程**: Strategist 生成探索树 → Validator 快速验证 → Builder 完整计算 → 失败则回溯
- **适用场景**: 需要探索多种可能性，从失败中学习
- **Token 消耗**: 高
- **文件**: orchestrator_tree_search.md, strategist.md, validator.md, architecture_tree_search.md

## Usage

### 通过 config.json 选择 pipeline

编辑 `config.json`:
```json
{
  "model": "qwen3.6-plus",
  "pipeline": "parallel",  // 可选: standard, parallel, iterative, debate, tree_search
  "timeout_seconds": 86400,
  "max_concurrent_problems": 3
}
```

### 通过命令行参数选择 pipeline

```bash
# Standard (默认)
python3 run.py problems/disk_energy

# Parallel Paths
python3 run.py problems/disk_energy --pipeline parallel

# Iterative
python3 run.py problems/disk_energy --pipeline iterative

# Debate
python3 run.py problems/disk_energy --pipeline debate

# Tree Search
python3 run.py problems/disk_energy --pipeline tree_search
```

## File Structure

```
prompts/
├── orchestrator.md                    # Standard pipeline
├── orchestrator_parallel.md           # Parallel Paths
├── orchestrator_iterative.md          # Iterative
├── orchestrator_debate.md             # Debate
├── orchestrator_tree_search.md        # Tree Search
│
├── planner.md                         # 标准 Planner (所有 pipeline 共用)
├── builder.md                         # 标准 Builder (所有 pipeline 共用)
├── evaluator.md                       # 标准 Evaluator (所有 pipeline 共用)
├── architecture.md                    # 标准架构图
│
├── meta_planner.md                    # Parallel: 元规划者
├── architecture_parallel.md           # Parallel: 架构图
│
├── explorer.md                        # Iterative: 探索者
├── architecture_iterative.md          # Iterative: 架构图
│
├── coordinator.md                     # Debate: 协调者
├── architecture_debate.md             # Debate: 架构图
├── experts/
│   ├── theorist.md                    # Debate: 理论物理学家
│   ├── computationalist.md            # Debate: 计算物理学家
│   ├── experimentalist.md             # Debate: 实验物理学家
│   └── critic.md                      # Debate: 批评家
│
├── strategist.md                      # Tree Search: 策略师
├── validator.md                       # Tree Search: 验证者
└── architecture_tree_search.md        # Tree Search: 架构图
```

## Implementation Details

### Phase 1: Infrastructure
- 更新 `config.json` 添加 `pipeline` 字段
- 修改 `run.py` 支持 pipeline 路由和 `--pipeline` 命令行参数
- 支持动态加载不同 pipeline 的 prompt 文件

### Phase 2: Parallel Paths
- 3 个 Planner 并行启动，各自写 plan_1.md, plan_2.md, plan_3.md
- Meta-Planner 评估并选择最优方案，写 plan.md
- 后续流程同 Standard

### Phase 3: Iterative
- Explorer 基于 exploration_history.md 提出假设
- Builder 验证假设
- Evaluator 评估进展 (PASS/PARTIAL/DEAD_END)
- 循环迭代直到收敛或达到 max_iterations (默认 5)

### Phase 4: Debate
- 3 个专家 (Theorist, Computationalist, Experimentalist) 并行分析
- Critic 批评所有专家意见
- 专家回应批评，修正方案
- 重复 2-3 轮辩论
- Coordinator 综合共识
- Builder 执行共识方案

### Phase 5: Tree Search
- Strategist 生成探索树，决定下一步行动 (expand/validate/build/backtrack/terminate)
- Validator 快速验证策略可行性 (PROMISING/DEAD_END/UNCERTAIN)
- Builder 完整计算有希望的策略
- 失败时回溯到父节点
- 找到成功方案后进入标准流程

## Testing Strategy

使用同一个测试题 (均匀带电圆盘) 测试所有 pipeline:

```bash
# 测试所有 pipeline
for pipeline in standard parallel iterative debate tree_search; do
    echo "Testing $pipeline..."
    python3 run.py problems/disk_energy --pipeline $pipeline
done
```

**验证指标**:
- 最终答案是否正确 ($W = \frac{2Q^2}{3\pi\epsilon_0 R}$)
- Token 消耗
- 用时
- 是否发现"绕过椭圆积分的方法"

## Key Features

### Parallel Paths
- ✅ 并行探索多个方案
- ✅ Meta-Planner 综合评估
- ✅ 方案融合能力
- ✅ 增加找到创新方案的概率

### Iterative
- ✅ 渐进式探索
- ✅ 从失败中学习
- ✅ 历史积累 (exploration_history.md)
- ✅ 灵活调整策略

### Debate
- ✅ 多视角分析
- ✅ 批评机制提高质量
- ✅ 迭代改进
- ✅ 共识综合

### Tree Search
- ✅ 智能搜索
- ✅ 快速验证筛选
- ✅ 回溯机制
- ✅ 启发式决策

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Pipeline 逻辑复杂 | 每个 pipeline 独立测试 |
| Token 消耗过高 | 设置 max_iterations/max_rounds 上限 |
| 状态管理混乱 | 统一用 JSON/text，清晰的状态转换 |
| Strategist/Explorer 决策质量差 | Prompt 中给明确的决策框架 |
| 多 Agent 并行时 Git 冲突 | 每个 Agent 写不同文件 |

## Future Extensions

- **Pipeline 自动选择**: 根据问题特征自动推荐 pipeline
- **混合策略**: 先 Parallel 粗筛，再 Tree Search 深入
- **可视化**: 生成探索树/辩论图的 HTML 报告
- **性能优化**: 并行执行多个 Validator/Builder

## Conclusion

成功实现了 4 种新的 pipeline 策略，共计新增 ~18 个 prompt 文件。所有 pipeline 都可以通过 config.json 或命令行参数选择使用。

下一步：在测试题上运行所有 pipeline，比较性能和结果质量。
