# Iterative Pipeline

## 概述

Explorer 提出假设 → Builder 验证 → Evaluator 评估 → 循环迭代直到收敛

## 流程

```
循环（最多 {max_iterations} 次）：
    Explorer → hypothesis_{N}.md
        ↓
    Builder → experiment_{N}.md
        ↓
    Evaluator → assessment_{N}.md
        ↓
    PASS → final_solution.md → 结束
    PARTIAL → 继续迭代
    DEAD_END → 回溯或结束
```

## Agent 配置

### Explorer
- 使用专用版本：`agents/explorer.md`
- 输入：problem.md + exploration_history.md
- 输出：`hypothesis_{N}.md`
- 权限：读 problem.md + exploration_history.md，写 hypothesis_{N}.md

### Builder
- 使用基础版本：`agents/builder.md`
- 输入：problem.md + hypothesis_{N}.md
- 输出：`experiment_{N}.md`
- 权限：读 problem.md + hypothesis_{N}.md，写 experiment_{N}.md

### Evaluator
- 使用基础版本：`agents/evaluator.md`
- 输入：problem.md + hypothesis_{N}.md + experiment_{N}.md
- 输出：`assessment_{N}.md`（第一行：PASS / PARTIAL / DEAD_END）
- 权限：读相关文件，写 assessment_{N}.md
- **差分：** 迭代评估模式下 `VERDICT` 词表为 `PASS` / `PARTIAL` / `DEAD_END`（以任务文件为准）；同时负责把本轮结论追加到 `exploration_history.md`（见执行协议）

## Orchestrator 执行协议

第 $n$ 轮循环（n 从 1 开始，最多 {max_iterations} 轮）。每轮依次写三个样板任务文件到 `{workspace}/tasks/`：

`task_explorer_{n}.md`：

```markdown
# Task explorer_{n}
说明：第 {n} 轮——提出新的求解假设

请阅读 `{workspace}/problem.md` 和 `{workspace}/exploration_history.md`（如不存在则为第一轮）。
提出一个新的假设，写入 `{workspace}/hypothesis_{n}.md`。
```

`task_builder_{n}.md`：

```markdown
# Task builder_{n}
说明：第 {n} 轮——验证假设 {n}，产出实验记录

请阅读 `{workspace}/problem.md` 和 `{workspace}/hypothesis_{n}.md`，验证这个假设。
将验证过程与结果写入 `{workspace}/experiment_{n}.md`，计算脚本放在 `{workspace}/scripts/builder/iter_{n}/`。
```

`task_evaluator_{n}.md`：

```markdown
# Task evaluator_{n}
说明：第 {n} 轮——评估假设验证结果（PASS/PARTIAL/DEAD_END）

请阅读 `{workspace}/problem.md`、`{workspace}/hypothesis_{n}.md` 和 `{workspace}/experiment_{n}.md`，评估本轮进展
（审计 `{workspace}/scripts/builder/` 下的代码——只读，不运行；你自己的验证脚本放 `{workspace}/scripts/evaluator/iter_{n}/`，从 problem.md 独立转录）。
1. 将评估写入 `{workspace}/assessment_{n}.md`，**第一行必须是 PASS、PARTIAL 或 DEAD_END 之一**
2. 将本轮结论追加到 `{workspace}/exploration_history.md`（假设要点 + 裁决 + 经验教训，不超过 5 行）
```

**路由（只依据 `debug/.<Role>.result` 的 HANDOFF，`VERDICT` 与 `assessment_{n}.md` 第一行一致）：**

- Explorer `BLOCKED` → 重试一次；仍失败 → 记入 `debug/.errors.log`，终止并写 final_summary.md
- Builder `BLOCKED` → 本轮按 DEAD_END 处理，直接进入下一轮
- Evaluator `VERDICT: PASS` → 再 spawn 一次 Builder，样板任务：「请基于 `{workspace}/hypothesis_{n}.md` 和 `{workspace}/experiment_{n}.md`，整理出完整解答，写入 `{workspace}/final_solution.md`」→ 写 final_summary.md，结束
- `PARTIAL` / `DEAD_END` → 更新 `debug/.state`，进入第 n+1 轮；达到 {max_iterations} 轮仍未 PASS → 写 final_summary.md（注明未收敛及最后一轮裁决）结束

## 状态管理

写入 `{workspace}/debug/.state`（key: value 格式）：

```
pipeline: iterative
stage: iteration
iteration: 2
last_verdict: PARTIAL
next: Explorer task_explorer_3.md
```

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `max_iterations`: {max_iterations}
