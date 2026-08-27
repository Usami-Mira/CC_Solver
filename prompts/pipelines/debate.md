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

## Orchestrator 执行协议

### 阶段 1：专家并行独立分析

写三个样板任务到 `{workspace}/tasks/`（仅角色与输出文件名不同），并行 spawn（Bash `&` + `wait`；spawn.py 的自动快照用文件锁互斥，并行安全）：

`task_theorist.md`：

```markdown
# Task theorist

请阅读 `{workspace}/problem.md`，进行理论分析。
将分析写入 `{workspace}/theorist.md`。
```

（Computationalist → `computationalist.md`，Experimentalist → `experimentalist.md`，措辞同理）

```bash
python3 {project_root}/scripts/spawn.py Theorist {workspace} agents/theorist task_theorist.md &
python3 {project_root}/scripts/spawn.py Computationalist {workspace} agents/computationalist task_computationalist.md &
python3 {project_root}/scripts/spawn.py Experimentalist {workspace} agents/experimentalist task_experimentalist.md &
wait
```

### 阶段 2：辩论循环（第 $n$ 轮，最多 {max_rounds} 轮）

`task_critic_{n}.md`：

```markdown
# Task critic_{n}

请阅读 `{workspace}/problem.md`、`{workspace}/theorist.md`、`{workspace}/computationalist.md`、`{workspace}/experimentalist.md`。
将批评写入 `{workspace}/critic_round_{n}.md`。
```

**收敛判断**：读 `debug/.Critic.result` 的 SUMMARY（含 `Critical: X, Major: Y` 计数）。若 Critical 为 0，跳过回应与后续轮次，直接进入阶段 3；否则继续。

专家回应（三个角色可并行），样板任务以 Theorist 为例：

`task_theorist_respond_{n}.md`：

```markdown
# Task theorist_respond_{n}

请阅读 `{workspace}/problem.md`、`{workspace}/critic_round_{n}.md` 和你此前的分析 `{workspace}/theorist.md`。
回应批评，原地更新 `{workspace}/theorist.md`。
```

（Computationalist / Experimentalist 同理，更新各自的文件）

`task_secretary_{n}.md`：

```markdown
# Task secretary_{n}

请阅读 `{workspace}/problem.md`、三份专家分析（最新版本）和 `{workspace}/critic_round_{n}.md`。
将第 {n} 轮辩论记录写入 `{workspace}/debate_summary_round_{n}.md`。
```

Secretary 的 `debug/.Secretary.result` 中 `OUTPUT` 应为 `debate_summary_round_{n}.md`；确认后进入下一轮或阶段 3。

### 阶段 3：Secretary 撰写最终 Plan

`task_secretary_final.md`：

```markdown
# Task secretary_final

请阅读 `{workspace}/problem.md`、三份专家分析（最终版本）、所有 `critic_round_*.md` 和所有 `debate_summary_round_*.md`。
综合共识，将最终解题计划写入 `{workspace}/final_plan.md`。
```

Secretary 的 `debug/.Secretary.result` 中 `OUTPUT` 为 `final_plan.md` → 进入阶段 4。

### 阶段 4 / 5：Builder / Evaluator

样板任务与路由同 Standard Pipeline（task_builder.md 读 problem.md + final_plan.md；task_evaluator.md；PASS/REVISE 循环；**REVISE 先走修订争议协议**，见通用编排器，修订最多 {max_revisions} 次）。

**通用路由：** 任一角色 `BLOCKED` → 重试一次，仍失败记入 `debug/.errors.log` 并按阶段跳过或终止。

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
dispute_rebuttal_1（仅 REVISE 时）
builder_revise_1
evaluator_revise_1
done
```

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `max_rounds`: {max_rounds}
