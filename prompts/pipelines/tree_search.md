# Tree Search Pipeline

## 概述

Planner 展开搜索树（一次生成 ≥2 个结构不同的分支）→ 每个分支由临时 Builder-Evaluator 验证 → Orchestrator 按 best-first 选择下一个前沿节点 → 死端回溯 → 某分支完整解题后形成方案 → Verifier 审查方案 → Final Builder 执行 → Final Evaluator 审查

**与线性迭代的本质区别**：多个候选分支同时存活于搜索树中；某分支被判死端后，搜索回到分叉点换路，而不是沿单条路走到黑。

## 核心机制

1. **分支**：Planner 每次展开必须给出 ≥2 个**结构不同**的验证任务（不同出发点、不同定理、不同积分/求解路径）
2. **验收判据**：每个验证任务必须附带机器可检的判据（结果形式约束、数值自检、量纲/极限检查）——这是死端检测的客观依据
3. **树表**：Orchestrator 在 `debug/.state` 维护**纯元数据**的树表（节点/父节点/状态/裁决/轮次），不读任何物理内容
4. **Best-first 选择**：按元数据优先级挑下一个展开节点，不需要理解内容
5. **回溯**：死端节点不再展开、改选下一个前沿节点——这就是回溯，无需专门机制

## 流程

```
阶段 1：树搜索（最多 {max_iterations} 次 Planner 调用）
    Planner → strategy.md + ≥2 个 task_{id}.md（各含验收判据）
        ↓
    每个分支（顺序处理）：
        Ephemeral Builder → calculation_{id}.md
        Ephemeral Evaluator → verification_{id}.md（首行 PASS/FAIL，逐条对照验收判据）
        ↓
    Orchestrator 更新树表：PASS → ALIVE，FAIL → DEAD
        ↓
    Best-first 选下一个前沿节点 → Planner 展开它（或判定 DONE / 放弃）
        ↓
    某分支完整解题 → Planner 沿该路径写 final_plan.md + STATUS: DONE
    树耗尽仍无解 → 重新规划一次（新根分支）；再耗尽 → 选最优幸存分支强行收尾

阶段 2：Verifier 审查方案
    Verifier → verification_plan.md（首行 SOUND / REVISE）
    SOUND → 阶段 3
    REVISE → Planner 修订一次 → Verifier 复审
        （修订上限 1 轮：第二次无论什么裁决都放行）

阶段 3：Final Builder 执行
    Builder → solution.md

阶段 4：Final Evaluator 审查
    Evaluator → review.md
    PASS → final_summary.md
    REVISE → 回到 Final Builder（最多 {max_revisions} 次）
```

## 职责划分（重要）

**所有物理内容都由 Planner / Builder / Evaluator 产出。Orchestrator 只做调度。样板任务文件一律写入 `{workspace}/tasks/`。**

| 文件 | 谁写 |
|------|------|
| `tasks/task_planner_{n}.md`（样板） | Orchestrator（只含调度指令 + 树表元数据，不含物理内容） |
| `tasks/task_{id}.md`（验证任务，含物理细节 + **验收判据**） | **Planner** |
| `tasks/task_eval_{id}.md`（样板） | Orchestrator（固定模板，`{id}` 取自 Planner HANDOFF 的 `NEXT_TASKS`） |
| `tasks/task_verifier.md`（样板） | Orchestrator（固定模板） |
| `strategy.md`、`final_plan.md`、`calculations_history.md` | Planner |
| `debug/.state` 中的树表（纯元数据） | Orchestrator |
| `verification_plan.md` | **Verifier** |
| `calculation_{id}.md`、`solution.md` | Builder |
| `verification_{id}.md`、`review.md` | Evaluator |

## 节点状态词汇（树表元数据）

| 状态 | 含义 |
|------|------|
| `ALIVE` | Evaluator 裁决 PASS，尚未展开 |
| `DEAD` | Evaluator 裁决 FAIL（验收判据不满足 = 死端），或被 Planner 放弃 |
| `EXPANDED` | 曾为 ALIVE，已生成子节点 |
| `DONE` | Planner 判定该分支已完整解题，`final_plan.md` 已写 |
| `BLOCKED` | Builder 无法执行（未验证，留给 Planner 处理） |

## Orchestrator 执行协议

### 第 1 轮：根展开

写入样板任务文件 `tasks/task_planner_1.md`（不含物理内容）：

```markdown
# Task planner_1（根展开）

请阅读 `{workspace}/problem.md`。

然后：
1. 写 `{workspace}/strategy.md`（题意理解 + 路线划分理由）
2. 给出 **≥2 个结构不同**的求解路线（不同出发点/定理/积分路径），每条路线写一个完整验证任务 `{workspace}/tasks/task_{id}.md`。每个任务文件必须包含：
   a. 完整物理细节（算什么、怎么算、全部参数）
   b. **验收判据**（机器可检），例如：
      - 结果形式约束（如"闭式，不含 $\mathrm{EllipticE}$/$\mathrm{EllipticF}$ 等特殊函数"）
      - 数值自检（符号结果与独立数值计算吻合，给出容差）
      - 量纲与极限合理性检查
   c. 与其他路线的结构差异说明
   d. 输出位置：结果写入 `{workspace}/calculation_{id}.md`（**禁止写 `solution.md`**——那是 Final Builder 的文件，覆盖会导致跨分支污染）
3. 若最新一轮验证的结论应保留，将其要点追加到 `{workspace}/calculations_history.md`

最终消息按 HANDOFF 格式：`STATUS: BRANCH` + `PARENT: ROOT` + `NEXT_TASKS: task_a.md, task_b.md, ...`
```

然后 `spawn.py Planner {workspace} agents/planner_deep task_planner_1`，读 `debug/.Planner.result`，按 HANDOFF 路由（见下）。

### 常规轮（第 $n$ 轮）：展开指定节点

Best-first 选出待展开节点 `{id}` 后（选择规则见下），写入样板 `tasks/task_planner_{n}.md`：

```markdown
# Task planner_{n}（展开节点 {id}）

请阅读 `{workspace}/problem.md`、`{workspace}/strategy.md`、`{workspace}/calculations_history.md`（如存在），
以及节点 `{id}` 及其祖先节点相关的 `calculation_*.md`、`verification_*.md`。

当前搜索树（元数据，从 `debug/.state` 原样复制）：

    {tree_table}

三选一：
a. 节点 `{id}` 的路径已能完整解题 → 写 `{workspace}/final_plan.md`，汇报 `STATUS: DONE`
b. 需要继续分支 → 写 ≥2 个结构不同的后续验证任务 `task_{id2}.md`（各含验收判据，注明结果写入 `calculation_{id2}.md`、禁止写 `solution.md`，继承父节点已确认的结论），汇报 `STATUS: BRANCH` + `PARENT: {id}` + `NEXT_TASKS: ...`
c. 节点 `{id}` 实为死端/无价值 → 汇报 `STATUS: FAIL`（Orchestrator 将其标记为 DEAD 并换下一个前沿）

若本轮有值得保留的新结论，追加到 `{workspace}/calculations_history.md`。
```

然后 `spawn.py Planner {workspace} agents/planner_deep task_planner_{n}`，读 `debug/.Planner.result`。

### 根据 Planner 的 HANDOFF 路由

- `STATUS: BRANCH` + `NEXT_TASKS: ...` + `PARENT: {id}` → 顺序处理每个分支（见下节）；分支数不足 2 个则照常执行（视为线性深入，树退化为单链）
- `STATUS: DONE` → 更新 `debug/.state`（该节点记 `DONE`），进入阶段 2
- `STATUS: FAIL` → 树表中该节点记 `DEAD`，回到 best-first 选择（进入下一轮）；根展开轮无节点可记，直接进入下一轮

### 分支处理（对 `NEXT_TASKS` 中每个 `task_{id}.md`）

1. spawn Builder：`spawn.py Builder {workspace} agents/builder task_{id}`（临时任务加 `--timeout {ephemeral_timeout}`），读 `debug/.Builder.result`
   - `STATUS: OK` → 继续第 2 步
   - `STATUS: BLOCKED` → 树表记 `BLOCKED`，跳过本分支的评估，处理下一个分支
   - `STATUS: FAIL` → 树表记 `DEAD`，处理下一个分支
2. 写样板 `tasks/task_eval_{id}.md` → spawn Evaluator（`agents/evaluator task_eval_{id}`，加 `--timeout {ephemeral_timeout}`）
3. 读 `debug/.Evaluator.result` 的 `VERDICT`（可用 `head -1 verification_{id}.md` 交叉验证），更新树表：`PASS` → `ALIVE`，`FAIL` → `DEAD`
4. 处理下一个分支

**所有分支处理完后**更新 `debug/.state`（树表 + `iteration` + `last_verdict`），回到 best-first 选择。

**样板 `tasks/task_eval_{id}.md`：**

```markdown
# Task eval_{id}

请审查 `{workspace}/calculation_{id}.md`（参考 `{workspace}/problem.md` 与 `{workspace}/tasks/task_{id}.md`，并审计 `{workspace}/scripts/builder/` 下的代码——只读，不运行）。
你的验证脚本放 `{workspace}/scripts/evaluator/task_eval_{id}/`（从 problem.md 独立转录）。
必须**逐条对照任务文件中的验收判据**给出 满足/不满足 及证据。
将结果写入 `{workspace}/verification_{id}.md`。**输出第一行只写 `PASS` 或 `FAIL` 这一个词**（标题等一律从第二行开始）。
```

### Best-first 选择（纯元数据判断，不读内容）

1. 有 `DONE` 节点 → 进入阶段 2
2. 否则，在 `ALIVE` 且未展开的节点中：**轮次最大（最深层）者优先**；同轮次取最近一次 `PASS` 的节点 → 写展开任务
3. 无 `ALIVE` 未展开节点、但树中仍有 `BLOCKED` 节点 → 让 Planner 处理（展开任务中注明）
4. 前沿全空（全部 `DEAD`/`EXPANDED`）→ **树耗尽**：
   - 本轮题尚未重新规划过 → 写重规划任务（见下）
   - 已重规划过一次 → 写强制收尾任务（见下）

**预算检查**：每次写入 Planner 任务前，若 Planner 调用计数已达 `{max_iterations}`，不再展开，直接写强制收尾任务。

### 重规划任务（树耗尽，至多 1 次）

样板 `tasks/task_planner_{n}.md`：

```markdown
# Task planner_{n}（重新规划）

此前所有路线均已证死。请阅读 `{workspace}/problem.md`、`{workspace}/strategy.md`、`{workspace}/calculations_history.md`
及全部 `verification_*.md` 的失败原因（死端各卡在哪一步）。

换用与之前**本质不同**的思路，重新给出 ≥2 个结构不同的根分支（每个 `task_{id}.md` 含验收判据），
并在 `{workspace}/strategy.md` 中说明为何旧路线集体失败、新路线如何避开。
```

路由同根展开。

### 强制收尾任务（预算耗尽或重规划后再次耗尽）

样板 `tasks/task_planner_{n}.md`：

```markdown
# Task planner_{n}（强制收尾）

搜索预算已用尽。请阅读 `{workspace}/problem.md` 与现有全部记录，
选择最有希望的幸存路线（或部分结果组合），写出 `{workspace}/final_plan.md`；
对未经验证的环节在方案中明确标注风险。完成后汇报 `STATUS: DONE`。
```

### 阶段 2：方案验证（Verifier）

写入样板任务文件 `tasks/task_verifier.md`：

```markdown
# Task verifier

请审查 `{workspace}/final_plan.md`（对照 `{workspace}/problem.md`；如需上下文可读 `{workspace}/strategy.md` 和已有的计算/验证记录）。
抽查脚本（如有）放 `{workspace}/scripts/verifier/`。
将结果写入 `{workspace}/verification_plan.md`。输出第一行必须是 SOUND 或 REVISE。
```

然后 `spawn.py Verifier {workspace} agents/verifier task_verifier`，读 `debug/.Verifier.result` 的 `VERDICT` 字段（可用 `head -1 verification_plan.md` 交叉验证）：

- `SOUND` → 更新 `debug/.state`，进入阶段 3（Final Builder）
- `REVISE` 且 `debug/.state` 中尚无 `verify_round`（第一次）：
  1. 更新 `debug/.state`：`verify_round: 1`
  2. 写样板 `tasks/task_planner_{n}.md`（`{n}` 为下一个迭代编号），内容只有一句：「请阅读 `{workspace}/verification_plan.md` 中的问题清单，针对性修订 `{workspace}/final_plan.md`，完成后按原格式汇报 `STATUS: DONE`。」
  3. `spawn.py Planner {workspace} agents/planner_deep task_planner_{n}`，读 `debug/.Planner.result`；`STATUS: DONE` 则回到本阶段重新验证（`STATUS: BRANCH/FAIL` 则按树搜索路由处理）
- `REVISE` 且 `debug/.state` 已有 `verify_round: 1`（第二次）：**直接放行进入阶段 3**——在 `debug/.state` 记录 `last_verdict: REVISE` 后继续，不再循环

**验证最多 1 轮修订**：第二次 Verifier 裁决无论是什么都放行。

### 最终阶段样板任务文件（Final Builder / Final Evaluator）

```markdown
# Task final_builder

请阅读 `{workspace}/problem.md` 和 `{workspace}/final_plan.md`，执行完整求解。
将完整推导写入 `{workspace}/solution.md`，最终答案用 $\boxed{}$ 标注。
计算脚本放 `{workspace}/scripts/builder/final/`；按 final_plan 的步骤编号更新进度文件（见你的系统提示）。
```

```markdown
# Task final_evaluator

请审查 `{workspace}/solution.md`（对照 `{workspace}/problem.md`、`{workspace}/final_plan.md`，并审计 `{workspace}/scripts/builder/` 下的代码——只读，不运行）。
你的验证脚本放 `{workspace}/scripts/evaluator/final/`（从 problem.md 独立转录）。
将结果写入 `{workspace}/review.md`。输出第一行必须是 PASS 或 REVISE。
```

REVISE 时：**先执行修订争议协议**（见通用编排器的"修订争议协议"一节：Builder 回击 → 必要时 Evaluator 复审，达成共识或达 {max_disputes} 轮上限后才修订），然后更新 `debug/.state` 中的修订计数，重写样板任务（追加"请先阅读 review.md、rebuttal/rejoin 的最终结论并修正；未解决的争议点单独标注"），重新 spawn Builder（修订最多 {max_revisions} 次）。

## Agent 配置

### Planner
- 基础版本：`agents/planner_deep.md`（解除"一种方法"限制、原生支持 `BRANCH` 分支汇报的深度规划版。基础 `agents/planner.md` 的"一种方法"纪律与树搜索的 ≥2 分支要求直接冲突，故不用）
- **差分：** 树搜索模式下输出 `strategy.md`、`task_{id}.md`（**必须含验收判据**）、`calculations_history.md`、`final_plan.md`；最终消息为 HANDOFF 格式（`STATUS: BRANCH/DONE/FAIL`，BRANCH 时附 `PARENT` 与 `NEXT_TASKS`）。根展开按任务文件要求给 **≥2** 个分支（该版本系统提示默认 ≥3，以任务文件的具体要求为准）
- 职责：划分结构不同的路线、展开节点、判定某分支是否已完整解题、识别死端并放弃

### Builder（临时模式）
- 基础版本：`agents/builder.md`
- **差分：** 只验证小结论；结果必须写入 `calculation_{id}.md`，**禁止写 `solution.md`**（那是 Final Builder 的文件，覆盖会导致跨分支污染）；超时 `{ephemeral_timeout}` 秒；最终消息为 HANDOFF 格式

### Evaluator（临时模式）
- 基础版本：`agents/evaluator.md`
- **差分：** 输出 `verification_{id}.md`，第一行必须 `PASS` 或 `FAIL`；**必须逐条对照任务文件中的验收判据**给出 满足/不满足 及证据（验收判据不满足 = 死端信号）；超时 `{ephemeral_timeout}` 秒；最终消息为 HANDOFF 格式（`VERDICT`）

### Verifier
- 基础版本：`agents/verifier.md`
- 输入：problem.md + final_plan.md（+ strategy.md 等上下文）
- 输出：`verification_plan.md`，第一行必须 `SOUND` 或 `REVISE`；最终消息为 HANDOFF 格式（`VERDICT`）
- 职责：在 Final Builder 启动前审查方案的题意一致性、内部自洽性与结构健全性（允许短小数值抽查，禁止完整推导）

### Builder / Evaluator（最终模式）
- 使用基础版本（无差分），最终消息为 HANDOFF 格式

## 状态管理

`debug/.state` 示例（每完成一个阶段更新；树表为纯元数据）：

```
pipeline: tree_search
stage: iteration
iteration: 3
last_verdict: PASS
tree:
  A: parent=ROOT status=DEAD round=1
  B: parent=ROOT status=EXPANDED round=1
  B1: parent=B status=ALIVE round=2
  B2: parent=B status=DEAD round=2
replan_used: 0
next: Planner task_planner_4.md (expand B1)
```

进入方案验证后：

```
pipeline: tree_search
stage: plan_verification
verify_round: 0
last_verdict: DONE
next: Verifier task_verifier.md
```

`replan_used` 取值 0/1，强制执行"重新规划至多 1 次"。`verify_round` 只在发生修订时写（取值 1），用于强制执行"最多修订 1 轮"。进入修订争议协议时写 `dispute_round: <n>`。

## 与 Adaptive 的区别

| 特性 | Tree Search | Adaptive |
|------|-------------|----------|
| 决策方式 | 分支展开（≥2 个结构不同分支）+ best-first 选择 + 死端回溯 | 线性迭代 + 自适应调整 |
| 状态管理 | `debug/.state` 树表（多前沿节点并存，纯元数据） | 简单历史记录（单路径） |
| 死端处理 | 验收判据 + Evaluator 裁决 → 换分支 | Planner 看到 FAIL 后自行调整 |
| 适用场景 | 多条结构不同路线竞争、易撞死端的题 | 单路径深入验证 |
| Planner 职责 | 生成/展开分支（含验收判据）、判定 DONE | 自适应决策 + 动态调整 |

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `max_iterations`: {max_iterations}
- `ephemeral_timeout`: {ephemeral_timeout}
