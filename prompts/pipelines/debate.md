# Debate Pipeline

## 概述

多个专家（Theorist, Computationalist, Experimentalist）辩论 → Critic 批评 → Secretary 记录 → 形成共识 → Builder 执行 → Evaluator 审查

## 流程

```
阶段 1：专家独立分析（并行）
    Theorist → theorist.md
    Computationalist → computationalist.md
    Experimentalist → experimentalist.md

阶段 2：辩论循环（最多 {max_rounds} 轮）
    Critic → critic_round_{N}.md
    专家回应 → theorist.md, computationalist.md, experimentalist.md（更新）
    Secretary → debate_summary_round_{N}.md

阶段 3：Secretary 撰写最终 Plan
    Secretary → final_plan.md

阶段 4：Builder 执行
    Builder → solution.md

阶段 5：Evaluator 审查
    Evaluator → review.md
    PASS → final_summary.md
    REVISE → 回到 Builder（最多 {max_revisions} 次）
```

## Agent 配置

### Theorist
- 使用专用版本：`agents/theorist.md`
- 输出：`theorist.md`
- 权限：读 problem.md，写 theorist.md

### Computationalist
- 使用专用版本：`agents/computationalist.md`
- 输出：`computationalist.md`

### Experimentalist
- 使用专用版本：`agents/experimentalist.md`
- 输出：`experimentalist.md`

### Critic
- 使用专用版本：`agents/critic.md`
- 输入：problem.md + 所有专家分析
- 输出：`critic_round_{N}.md`

### Secretary
- 使用专用版本：`agents/secretary.md`
- 输入：所有专家分析 + critic 文件
- 输出：`debate_summary_round_{N}.md` + `final_plan.md`

### Builder
- 使用基础版本：`agents/builder.md`
- 输入：problem.md + final_plan.md
- 输出：`solution.md`

### Evaluator
- 使用基础版本：`agents/evaluator.md`
- 输入：problem.md + solution.md
- 输出：`review.md`

## 状态管理

```
experts_initial
debate_round_1
  - critic_1
  - experts_respond_1
  - secretary_record_1
debate_round_2
  - critic_2
  - experts_respond_2
  - secretary_record_2
secretary_final_plan
builder
evaluator
builder_revise_1
evaluator_revise_1
done
```

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `max_rounds`: {max_rounds}
