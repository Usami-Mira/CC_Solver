# Deep Search Pipeline

## 概述

审题定位 crux → 发散生成 ≥3 个结构不同、视角多样的方向（各含验收判据 + 预测撞墙点）→ best-first 深挖 + 死端回溯 → 多专家围绕候选方案**辩论共识**（思想碰撞提出创新点，可动议 spawn 临时 Builder/Evaluator 解决分歧）→ Secretary 记录共识 → Verifier 审查 → Final Builder 执行 → Final Evaluator 审查。

这是为**难题**设计的主力流水线：crux 不明、候选路线多、易撞死端、方案必须经多视角碰撞达成共识。

## 集大成：各机制的来源

| 机制 | 来源 | 在 Deep Search 中的作用 |
|------|------|------------------------|
| 审题纪律（量纲/极限分析）+ crux 定位 | Standard Planner | 阶段 1：聚焦探索，不盲目开局 |
| 多提案、多视角、结构多样性 | Parallel | 阶段 1：≥3 个真不同的方向，防止"同一思路换皮" |
| 验收判据 + 树表 + best-first + 回溯 | Tree Search | 阶段 2：深挖搜索的骨架 |
| 临时 Builder-Evaluator 检查点 | Adaptive | 阶段 2：每步小结论先验证再继续；阶段 3：执行辩论动议 |
| 多专家辩论 + Secretary 共识 + 动议 | Debate | 阶段 3：思想碰撞产生创新点，共识成为定稿方案 |
| Verifier + 独立审查 + 修订争议协议 | Tree Search + Standard | 阶段 4-5：定稿质量闸门 |

**与 Tree Search 的关键升级**：① Planner 用解除"一种方法"限制的专用版（`agents/planner_deep.md`），发散生成是显式职责；② 每个方向附**预测撞墙点**，死端可预判；③ DONE 之后、定稿之前多一个**多专家辩论共识**阶段，专家可动议 spawn 临时验证解决事实分歧；④ 深挖允许单主线延续（不强制每层 ≥2 分支），回溯仍由树表保证。

## 核心机制

1. **审题与 crux 定位**：Planner 首轮写 strategy.md——题意、量纲预测（Buckingham π）、极限行为、把难点定位到**具体一步**（crux）
2. **发散生成**：≥3 个**结构不同**（不同出发点/定理/数学工具）且**视角多样**的方向，每个方向附机器可检的验收判据 + 预测撞墙点
3. **深挖 + 回溯**：best-first 选前沿节点展开；主线可单链深入；验收判据不满足 = 死端，回退换路
4. **辩论共识**：候选方案出来后，四位专家（Theorist/Computationalist/Experimentalist/Critic）围绕它碰撞——评估、互补、提出创新点；事实分歧（某个积分收敛吗、两个表达式数值相等吗、近似误差够小吗）任何专家可**动议** spawn 临时 Builder/Evaluator 算清楚；最后 Secretary 记录共识并改写 final_plan.md
5. **树表**：Orchestrator 在 `debug/.state` 维护**纯元数据**树表（节点/父节点/状态/裁决/轮次），不读任何物理内容

## 流程

```
阶段 1：审题 + 发散生成（Planner 第 1 轮）
    Planner → strategy.md（审题：理解/符号/量纲/极限/crux/路线划分理由）
            + ≥3 个 task_{id}.md（结构不同、视角多样，各含验收判据 + 预测撞墙点）
        ↓
阶段 2：深挖搜索（Planner 共 ≤ {max_iterations} 次调用）
    Best-first 选前沿节点 → Planner 展开：
        BRANCH → 每个子任务（顺序处理）：
                     Ephemeral Builder → calculation_{id}.md
                     Ephemeral Evaluator → verification_{id}.md（首行 PASS/FAIL，逐条对照验收判据）
                 → 更新树表（PASS→ALIVE，FAIL→DEAD）→ 回到 best-first
        DONE → final_plan.md（候选）→ 阶段 3
        FAIL → 该节点 DEAD → 回到 best-first
        ↓
    前沿全空 → 重规划（≤1 次：≥3 个本质不同的新根分支）
             → 再耗尽 → 强制收尾（选最优幸存路线，标注风险，写 final_plan.md）
        ↓
阶段 3：辩论共识（最多 {max_rounds} 轮）
    四专家并行发言 → 各自观点 + 动议（MOTION）
        MOTION → Ephemeral Builder/Evaluator 执行（累计 ≤ {max_motions} 个）→ 结果回流辩论
    Secretary 记录轮次 → debate_summary_round_{n}.md
    Critic SUMMARY 中 Critical: 0，或轮次用尽 → Secretary 综合共识 → final_plan.md（共识版）+ consensus.md
    否则 → 下一轮（专家互读观点 + 动议结果，碰撞修正）
        ↓
阶段 4：Verifier 审查方案
    Verifier → verification_plan.md（首行 SOUND / REVISE）
    SOUND → 阶段 5
    REVISE → Secretary 修订一次 → Verifier 复审
        （修订上限 1 轮：第二次无论什么裁决都放行）
        ↓
阶段 5：最终执行 + 审查
    Builder → solution.md
    Evaluator → review.md
    PASS → final_summary.md
    REVISE → 修订争议协议 → 回到 Final Builder（最多 {max_revisions} 次）
```

## 职责划分（重要）

**所有物理内容都由各专家角色产出。Orchestrator 只做调度。样板任务文件一律写入 `{workspace}/tasks/`。**

| 文件 | 谁写 |
|------|------|
| `tasks/task_planner_{n}.md`（样板） | Orchestrator（只含调度指令 + 树表元数据，不含物理内容） |
| `tasks/task_{id}.md`（验证任务：物理细节 + **验收判据** + **预测撞墙点**） | **Planner** |
| `tasks/task_eval_{id}.md`（样板） | Orchestrator（固定模板，`{id}` 取自 Planner HANDOFF 的 `NEXT_TASKS`） |
| `tasks/task_motion_{k}.md`（动议任务，含物理细节） | **提出动议的专家** |
| 辩论样板（`task_theorist_{n}.md`、`task_critic_{n}.md`、`task_secretary_{n}.md` 等） | Orchestrator（固定模板） |
| `tasks/task_verifier.md`（样板） | Orchestrator（固定模板） |
| `strategy.md`、`final_plan.md`（候选版）、`calculations_history.md` | Planner |
| `theorist.md`、`computationalist.md`、`experimentalist.md` | 各专家 |
| `critic_round_{n}.md` | Critic |
| `debate_summary_round_{n}.md`、`consensus.md`、`final_plan.md`（共识版） | Secretary |
| `debug/.state` 中的树表（纯元数据） | Orchestrator |
| `verification_plan.md` | **Verifier** |
| `calculation_{id}.md`、`calculation_motion_{k}.md`、`solution.md` | Builder |
| `verification_{id}.md`、`verification_motion_{k}.md`、`review.md` | Evaluator |

## 节点状态词汇（树表元数据）

| 状态 | 含义 |
|------|------|
| `ALIVE` | Evaluator 裁决 PASS，尚未展开 |
| `DEAD` | Evaluator 裁决 FAIL（验收判据不满足 = 死端），或被 Planner 放弃 |
| `EXPANDED` | 曾为 ALIVE，已生成子节点 |
| `DONE` | Planner 判定该分支已完整解题，`final_plan.md` 已写 |
| `BLOCKED` | Builder 无法执行（未验证，留给 Planner 处理） |

## Orchestrator 执行协议

### 第 1 轮：审题 + 发散生成

写入样板任务文件 `tasks/task_planner_1.md`（不含物理内容）：

```markdown
# Task planner_1（审题 + 发散生成）

请阅读 `{workspace}/problem.md`。

然后：
1. 写 `{workspace}/strategy.md`：审题拆解——题意理解（自己的话重述）、符号约定表、
   Buckingham π 量纲预测、极限与特例行为、**crux**（难点定位到具体一步）、路线划分理由
2. 给出 **≥3 个结构不同**的求解方向（不同出发点/不同定理/不同数学工具；视角也要多样，
   不要同一思路换参数），每个方向写一个完整验证任务 `{workspace}/tasks/task_{id}.md`。每个任务文件必须包含：
   a. 完整物理细节（算什么、怎么算、全部参数）
   b. **验收判据**（机器可检，逐条编号）：结果形式约束、数值自检（符号结果与独立数值计算吻合，给出容差）、
      量纲与极限合理性（对照 strategy.md）、针对 crux 的专项检查
   c. **预测撞墙点**：预计死在哪一步、死成什么样子
   d. 与其他路线的结构差异说明
   e. 输出位置：结果写入 `{workspace}/calculation_{id}.md`（**禁止写 `solution.md`**——那是 Final Builder 的文件，覆盖会导致跨分支污染）

最终消息按 HANDOFF 格式：`STATUS: BRANCH` + `PARENT: ROOT` + `NEXT_TASKS: task_a.md, task_b.md, ...`
```

然后 `spawn.py Planner {workspace} agents/planner_deep task_planner_1 --timeout {deep_timeout}`，读 `debug/.Planner.result`，按 HANDOFF 路由（见下）。

### 常规轮（第 $n$ 轮）：展开指定节点

Best-first 选出待展开节点 `{id}` 后（选择规则见下），写入样板 `tasks/task_planner_{n}.md`：

```markdown
# Task planner_{n}（展开节点 {id}）

请阅读 `{workspace}/problem.md`、`{workspace}/strategy.md`、`{workspace}/calculations_history.md`（如存在），
以及节点 `{id}` 及其祖先节点相关的 `calculation_*.md`、`verification_*.md`。

当前搜索树（元数据，从 `debug/.state` 原样复制）：

    {tree_table}

三选一：
a. 节点 `{id}` 的路径已能完整解题 → 写 `{workspace}/final_plan.md`（按你的系统提示的结构：
   选定路线/步骤编号清单/已验证基础/风险标注/验收清单），汇报 `STATUS: DONE`
b. 需要继续深挖 → 写后续验证任务 `task_{id2}.md`（主线 1 个 + 可选的结构不同岔路；
   若只写 1 个任务，必须说明为何此处不存在结构不同的替代；每个任务含验收判据 + 预测撞墙点，
   注明结果写入 `calculation_{id2}.md`、禁止写 `solution.md`，继承父节点已确认的结论），
   汇报 `STATUS: BRANCH` + `PARENT: {id}` + `NEXT_TASKS: ...`
c. 节点 `{id}` 实为撞墙/无价值 → 明确描述墙是什么（对照你的预测撞墙点），
   汇报 `STATUS: FAIL`（Orchestrator 将其标记为 DEAD 并换下一个前沿）

若本轮有值得保留的新结论（包括死分支的"为什么死"），追加到 `{workspace}/calculations_history.md`。
```

然后 `spawn.py Planner {workspace} agents/planner_deep task_planner_{n} --timeout {deep_timeout}`，读 `debug/.Planner.result`。

### 根据 Planner 的 HANDOFF 路由

- `STATUS: BRANCH` + `PARENT: {id}` + `NEXT_TASKS: ...` → 树表中父节点（若曾为 ALIVE）记 `EXPANDED`；顺序处理每个分支（见下节）
- `STATUS: DONE` → 树表中该节点记 `DONE`，更新 `debug/.state`（`stage: debate`），进入阶段 3
- `STATUS: FAIL` → 树表中该节点记 `DEAD`，回到 best-first 选择（进入下一轮）；根展开轮/重规划轮无节点可记，直接进入下一轮

### 分支处理（对 `NEXT_TASKS` 中每个 `task_{id}.md`）

1. spawn Builder：`spawn.py Builder {workspace} agents/builder task_{id} --timeout {ephemeral_timeout}`，读 `debug/.Builder.result`
   - `STATUS: OK` → 继续第 2 步
   - `STATUS: BLOCKED` → 树表记 `BLOCKED`，跳过本分支的评估，处理下一个分支
   - `STATUS: FAIL` → 树表记 `DEAD`，处理下一个分支
2. 写样板 `tasks/task_eval_{id}.md` → spawn Evaluator：`spawn.py Evaluator {workspace} agents/evaluator task_eval_{id} --timeout {ephemeral_timeout}`
3. 读 `debug/.Evaluator.result` 的 `VERDICT`（可用 `head -1 verification_{id}.md` 交叉验证），更新树表：`PASS` → `ALIVE`，`FAIL` → `DEAD`
4. 处理下一个分支

**所有分支处理完后**更新 `debug/.state`（树表 + `iteration` + `last_verdict`），回到 best-first 选择。

**样板 `tasks/task_eval_{id}.md`：**

```markdown
# Task eval_{id}

请审查 `{workspace}/calculation_{id}.md`（参考 `{workspace}/problem.md` 与 `{workspace}/tasks/task_{id}.md`，并审计 `{workspace}/scripts/builder/` 下的代码——只读，不运行）。
你的验证脚本放 `{workspace}/scripts/evaluator/task_eval_{id}/`（从 problem.md 独立转录）。
必须**逐条对照任务文件中的验收判据**给出 满足/不满足 及证据；若不满足，说明失败是否命中任务文件中的**预测撞墙点**。
将结果写入 `{workspace}/verification_{id}.md`。**输出第一行只写 `PASS` 或 `FAIL` 这一个词**（标题等一律从第二行开始）。
```

### Best-first 选择（纯元数据判断，不读内容）

1. 有 `DONE` 节点 → 进入阶段 3
2. 否则，在 `ALIVE` 且未展开的节点中：**轮次最大（最深层）者优先**；同轮次取最近一次 `PASS` 的节点 → 写展开任务
3. 无 `ALIVE` 未展开节点、但树中仍有 `BLOCKED` 节点 → 让 Planner 处理（展开任务中注明）
4. 前沿全空（全部 `DEAD`/`EXPANDED`）→ **树耗尽**：
   - 本轮题尚未重新规划过（`replan_used: 0`）→ 写重规划任务（见下）
   - 已重规划过一次 → 写强制收尾任务（见下）

**预算检查**：写入**展开类** Planner 任务前，若 Planner 调用计数已达 `{max_iterations}`，不再展开，直接写强制收尾任务。（修订类任务——Verifier REVISE 后的修订——不计入此检查。）

### 重规划任务（树耗尽，至多 1 次）

样板 `tasks/task_planner_{n}.md`：

```markdown
# Task planner_{n}（重新规划）

此前所有路线均已证死。请阅读 `{workspace}/problem.md`、`{workspace}/strategy.md`、`{workspace}/calculations_history.md`
及全部 `verification_*.md` 的失败原因（死端各卡在哪一步）。

换用与之前**本质不同**的思路，重新给出 ≥3 个结构不同的根分支（每个 `task_{id}.md` 含验收判据 + 预测撞墙点），
并在 `{workspace}/strategy.md` 中说明：旧路线集体死亡撞的是什么共同的墙、新路线如何避开、crux 的定位是否需要修正。
```

路由同根展开（`spawn.py Planner {workspace} agents/planner_deep task_planner_{n} --timeout {deep_timeout}`）。更新 `debug/.state`：`replan_used: 1`。

### 强制收尾任务（预算耗尽或重规划后再次耗尽）

样板 `tasks/task_planner_{n}.md`：

```markdown
# Task planner_{n}（强制收尾）

搜索预算已用尽。请阅读 `{workspace}/problem.md` 与现有全部记录，
选择最有希望的幸存路线（或部分结果组合），写出 `{workspace}/final_plan.md`；
对未经验证的环节在方案中明确标注风险。完成后汇报 `STATUS: DONE`。
```

### 阶段 3：辩论共识

**目标不是决出胜负，而是思想碰撞**：专家们围绕候选方案互相激发、提出创新点，用动议把事实分歧算清楚，最后由 Secretary 记录共识。

#### 每一轮（第 $r$ 轮，最多 {max_rounds} 轮）

**第 1 步——四专家并行发言。** 写四个样板任务。专家样板以 Theorist 为例（`tasks/task_theorist_{r}.md`；Computationalist / Experimentalist 措辞同理，换成各自专业视角与输出文件）：

```markdown
# Task theorist_{r}（辩论第 {r} 轮）

搜索阶段已产生候选方案 `{workspace}/final_plan.md`。请阅读它，以及 `{workspace}/problem.md`、
`{workspace}/strategy.md`、`{workspace}/calculations_history.md`（如存在）与相关的
`calculation_*.md`、`verification_*.md`{debate_context}。

从理论视角：
1. 评估候选方案：理论基础哪里扎实、哪里脆弱
2. **提出创新点**：更好的表示、更优雅的路线、对各分支已确认结论的复用或组合
3. 回应其他专家的观点与上一轮的批评（如有）：吸收合理意见，修正或辩护自己的主张

将完整观点写入 `{workspace}/theorist.md`{update_mode}。

**动议机制**：对可以用一次快速计算/验证解决的事实分歧（如某积分是否收敛、两式数值是否一致、
某近似误差是否够小），可写动议任务 `{workspace}/tasks/task_motion_{k}.md`——任务须含完整物理细节
（算什么/验什么、方法、全部参数、通过标准，注明结果写 `calculation_motion_{k}.md` 或
`verification_motion_{k}.md`，执行者禁止写 `solution.md`）；`k` 从 {next_motion_id} 开始。

最终消息汇报：
HANDOFF
STATUS: OK
OUTPUT: theorist.md
MOTION: task_motion_1.md -> Builder, task_motion_2.md -> Evaluator（无动议写 MOTION: NONE）
SUMMARY: ≤2 行
```

Critic 用 `tasks/task_critic_{r}.md`，在上述要求之外：把问题分为 **Critical**（阻碍共识、定稿前必须解决）/ **Major**（应当解决）两级，每个问题附改进建议；输出写 `critic_round_{r}.md`；SUMMARY 按你的系统提示惯例附 `Critical: X, Major: Y` 计数。

并行 spawn（spawn.py 的自动快照用文件锁互斥，并行安全）：

```bash
python3 {project_root}/scripts/spawn.py Theorist {workspace} agents/theorist task_theorist_{r} --timeout {deep_timeout} &
python3 {project_root}/scripts/spawn.py Computationalist {workspace} agents/computationalist task_computationalist_{r} --timeout {deep_timeout} &
python3 {project_root}/scripts/spawn.py Experimentalist {workspace} agents/experimentalist task_experimentalist_{r} --timeout {deep_timeout} &
python3 {project_root}/scripts/spawn.py Critic {workspace} agents/critic task_critic_{r} --timeout {deep_timeout} &
wait
```

**第 2 步——执行动议。** 读四个 `debug/.{Role}.result` 的 `MOTION` 行，对每个动议（可并行，`&` + `wait`）：

- `-> Builder`：`spawn.py Builder {workspace} agents/builder task_motion_{k} --timeout {ephemeral_timeout}`
- `-> Evaluator`：`spawn.py Evaluator {workspace} agents/evaluator task_motion_{k} --timeout {ephemeral_timeout}`

只记录各自的 STATUS/VERDICT 完成状态（**不判断内容**——结果留给专家下轮阅读）。累计动议数（`motions_used`）不得超过 {max_motions}，超出的跳过并在 `debug/.state` 注明。

**第 3 步——Secretary 记录本轮。** 写样板 `tasks/task_secretary_{r}.md`：

```markdown
# Task secretary_{r}

请阅读 `{workspace}/theorist.md`、`computationalist.md`、`experimentalist.md`（最新版本）、
`{workspace}/critic_round_{r}.md`，以及本轮动议结果 `calculation_motion_*.md` / `verification_motion_*.md`（如有）。
将第 {r} 轮辩论记录写入 `{workspace}/debate_summary_round_{r}.md`
（关键观点/主要分歧/提出的创新点/动议结论/下轮重点）。
```

`spawn.py Secretary {workspace} agents/secretary task_secretary_{r} --timeout {ephemeral_timeout}`。

**第 4 步——收敛判断。** 读 `debug/.Critic.result` 的 SUMMARY（`Critical: X, Major: Y`）：

- `Critical: 0`，或 `debate_round` 已达 {max_rounds} → **共识定稿**：写 `tasks/task_secretary_final.md`（见下），`spawn.py Secretary {workspace} agents/secretary task_secretary_final --timeout {deep_timeout}`；完成后更新 `debug/.state`（`stage: plan_verification`，`last_verdict: CONSENSUS`），进入阶段 4
- 否则 → `debate_round +1`，进入下一轮：下一轮专家样板中 `{debate_context}` 填「，以及上一轮其他专家的观点（`theorist.md`、`computationalist.md`、`experimentalist.md`、`critic_round_{r}.md`——只读与你相关的部分）、上一轮辩论记录 `debate_summary_round_{r}.md`、动议结果」，`{update_mode}` 填「（追加『第 {r+1} 轮』小节，保留历史内容）」；`{next_motion_id}` 始终取 `motions_used + 1`

#### 共识定稿样板 `tasks/task_secretary_final.md`

```markdown
# Task secretary_final

请阅读三位专家观点的最终版本、所有 `critic_round_*.md`、所有 `debate_summary_round_*.md`、
全部动议结果，以及候选方案原文。

综合共识，做两件事：
1. 将共识记录写入 `{workspace}/consensus.md`：各专家一致的结论、采纳的创新点（来源与理由）、
   每个主要分歧是如何解决的（动议结论优先于口头争论）、剩余风险
2. 将 `{workspace}/final_plan.md` 改写为**共识版**（候选版留在 git 历史中），保持结构：
   选定路线/步骤编号清单/已验证基础（引用 calculation_*.md 中已确认的结论）/风险标注（含未解决分歧）/验收清单
```

Secretary 的 `debug/.Secretary.result` 中 `OUTPUT` 应含 `final_plan.md` → 进入阶段 4。

### 阶段 4：方案验证（Verifier）

写入样板任务文件 `tasks/task_verifier.md`：

```markdown
# Task verifier

请审查 `{workspace}/final_plan.md`（对照 `{workspace}/problem.md`；如需上下文可读 `{workspace}/consensus.md`、`{workspace}/strategy.md` 和已有的计算/验证记录）。
抽查脚本（如有）放 `{workspace}/scripts/verifier/`。
将结果写入 `{workspace}/verification_plan.md`。输出第一行必须是 SOUND 或 REVISE。
```

然后 `spawn.py Verifier {workspace} agents/verifier task_verifier`，读 `debug/.Verifier.result` 的 `VERDICT` 字段（可用 `head -1 verification_plan.md` 交叉验证）：

- `SOUND` → 更新 `debug/.state`（`stage: final`），进入阶段 5（Final Builder）
- `REVISE` 且 `debug/.state` 中尚无 `verify_round`（第一次）：
  1. 更新 `debug/.state`：`verify_round: 1`
  2. 写样板 `tasks/task_secretary_revise.md`：「请阅读 `{workspace}/verification_plan.md` 中的问题清单，对照 `{workspace}/consensus.md` 与专家观点的最终版本，逐条修订 `{workspace}/final_plan.md`（保持共识的平衡；无法采纳的意见在方案风险标注中说明理由）。完成后汇报 `STATUS: OK`，`OUTPUT: final_plan.md`。」
  3. `spawn.py Secretary {workspace} agents/secretary task_secretary_revise --timeout {deep_timeout}`，读 `debug/.Secretary.result`；`STATUS: OK` 则回到本阶段重新验证
- `REVISE` 且 `debug/.state` 已有 `verify_round: 1`（第二次）：**直接放行进入阶段 5**——在 `debug/.state` 记录 `last_verdict: REVISE` 后继续，不再循环

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
- 基础版本：`agents/planner_deep.md`（**深度搜索专用版**：解除"一种方法"限制；职责 = 审题找 crux + 发散生成 ≥3 个结构不同、视角多样的方向（各含验收判据 + 预测撞墙点）+ 深挖/放弃/收尾决策）
- 最终消息为 HANDOFF 格式（`STATUS: BRANCH/DONE/FAIL`，BRANCH 时附 `PARENT` 与 `NEXT_TASKS`）
- 超时 `{deep_timeout}` 秒（深度思考任务比普通调度更耗时）

### Builder（临时模式）
- 基础版本：`agents/builder.md`
- **差分：** 只验证小结论或执行动议；结果必须写入任务指定的 `calculation_{id}.md` / `calculation_motion_{k}.md`，**禁止写 `solution.md`**（那是 Final Builder 的文件，覆盖会导致跨分支污染）；超时 `{ephemeral_timeout}` 秒；最终消息为 HANDOFF 格式

### Evaluator（临时模式）
- 基础版本：`agents/evaluator.md`
- **差分：** 输出 `verification_{id}.md`（或动议的 `verification_motion_{k}.md`），第一行必须 `PASS` 或 `FAIL`；验证任务必须**逐条对照任务文件中的验收判据**给出 满足/不满足 及证据（验收判据不满足 = 死端信号），失败时说明是否命中预测撞墙点；超时 `{ephemeral_timeout}` 秒；最终消息为 HANDOFF 格式（`VERDICT`）

### Theorist / Computationalist / Experimentalist
- 基础版本：`agents/theorist.md`、`agents/computationalist.md`、`agents/experimentalist.md`
- **差分：** 输入是候选方案 + 搜索记录（不是裸题）；目标是评估、互补、**提出创新点**、趋向共识；HANDOFF 追加 `MOTION` 行（动议时自己写动议任务文件，注明执行者与编号）
- 超时 `{deep_timeout}` 秒

### Critic
- 基础版本：`agents/critic.md`
- **差分：** 作为**建设性批评者**参与辩论——指出候选方案与各专家观点的弱点，但每个问题必须附改进建议，目标是把方案变得更好而不是否定它；问题分 Critical（阻碍共识、定稿前必须解决）/ Major 两级；SUMMARY 惯例不变（Orchestrator 用 Critical 计数判断收敛）；动议机制同上
- 超时 `{deep_timeout}` 秒

### Secretary
- 基础版本：`agents/secretary.md`
- **差分：** 除每轮记录（`debate_summary_round_{r}.md`）外，最终写 `consensus.md` 并把 `final_plan.md` 改写为共识版；也承担 Verifier REVISE 后的逐条修订
- 记录轮次超时 `{ephemeral_timeout}` 秒；共识定稿与修订超时 `{deep_timeout}` 秒

### Verifier
- 基础版本：`agents/verifier.md`
- 输入：problem.md + final_plan.md（+ consensus.md、strategy.md 等上下文）
- 输出：`verification_plan.md`，第一行必须 `SOUND` 或 `REVISE`；最终消息为 HANDOFF 格式（`VERDICT`）
- 职责：在 Final Builder 启动前审查方案的题意一致性、内部自洽性与结构健全性（允许短小数值抽查，禁止完整推导）

### Builder / Evaluator（最终模式）
- 使用基础版本（无差分），最终消息为 HANDOFF 格式

## 状态管理

`debug/.state` 示例（每完成一个阶段更新；树表为纯元数据）：

深挖阶段：

```
pipeline: deep_search
stage: deep_dive
iteration: 3
last_verdict: PASS
tree:
  A: parent=ROOT status=DEAD round=1
  B: parent=ROOT status=EXPANDED round=1
  B1: parent=B status=ALIVE round=2
replan_used: 0
next: Planner task_planner_4.md (expand B1)
```

辩论阶段：

```
pipeline: deep_search
stage: debate
iteration: 6
debate_round: 2
motions_used: 3
last_verdict: DONE
tree:
  ...
  B1a: parent=B1 status=DONE round=6
replan_used: 0
next: Experts round 2
```

进入方案验证后：

```
pipeline: deep_search
stage: plan_verification
verify_round: 0
last_verdict: CONSENSUS
next: Verifier task_verifier.md
```

- `debate_round`：当前辩论轮次（1..{max_rounds}）
- `motions_used`：累计已执行动议数，上限 {max_motions}
- `replan_used` 取值 0/1，强制执行"重新规划至多 1 次"
- `verify_round` 只在发生修订时写（取值 1），用于强制执行"最多修订 1 轮"
- 进入修订争议协议时写 `dispute_round: <n>`

## 定位：何时选哪条流水线

| 流水线 | 适用场景 |
|--------|----------|
| `deep_search` | **难题默认**：crux 不明、候选路线多、易撞死端、方案须经多视角碰撞达成共识（前沿问题首选） |
| `tree_search` | 数条结构不同路线竞争、题意明确、不需要辩论共识 |
| `adaptive` | 方向明确、单路径深入验证 |
| `standard` | 方法明确、一步到位的题 |

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `max_iterations`: {max_iterations}
- `max_rounds`: {max_rounds}（辩论轮数）
- `max_motions`: {max_motions}（辩论动议总数上限）
- `ephemeral_timeout`: {ephemeral_timeout}（临时 Builder/Evaluator、动议执行、辩论轮次记录）
- `deep_timeout`: {deep_timeout}（Planner 深度思考、专家发言、共识定稿）
