# Deep Search Pipeline

## 概述

单层**专家团循环**（Theorist / Computationalist / Experimentalist / Critic）取代 Planner 主脑：专家团从审题、发散生成、深挖搜索一路运行到共识（每轮思想碰撞，可动议 spawn 临时 Builder/Evaluator 把事实分歧算清楚）；**Secretary 边打边写**（轮次记录 + 活文档 `plan_draft.md` + 定稿 `final_plan.md`）；**Verifier 单闸审查**，不同意就带问题清单**打回专家团**重修，永不无条件放行；通过后 Final Builder 执行、Final Evaluator 三态裁决（`PASS` 收工 / `REVISE` 打回 Builder / `FAIL` = 完全无出路 → 打回专家团重开），Final Evaluator 还可请求 **Ephemeral Standard（Planner→Builder→Evaluator 三连）** 计算简单子问题辅助裁决。

这是为**难题**设计的主力流水线：crux 不明、候选路线多、易撞死端、方案必须经多视角碰撞达成共识。

## 集大成：各机制的来源

| 机制 | 来源 | 在 Deep Search 中的作用 |
|------|------|------------------------|
| 审题纪律（量纲/极限分析）+ crux 定位 | Standard Planner → 由专家团与 Secretary 继承 | 阶段 1 首轮：聚焦探索，不盲目开局 |
| 多提案、多视角、结构多样性 | Parallel | 首轮：每位专家各提 ≥1 个真不同的方向 |
| 验收判据 + 树表 + best-first + 回溯 | Tree Search | 阶段 1：深挖搜索的骨架 |
| 临时 Builder-Evaluator 检查点 | Adaptive | 阶段 1：每个分支先验证再继续；执行动议与子任务 |
| 多专家碰撞 + 动议 + Secretary 记录 | Debate | **并入单层循环**：碰撞每轮发生，不必等候选方案成型 |
| Verifier 单闸 + **打回协议** | 本版新设 | 阶段 2：有击杀权的质量闸门，永不无条件放行 |
| Final E 三态 + 子问题增援（Ephemeral Standard） | 本版新设 | 阶段 3：执行层证死可打回重开；简单子问题可增援 |

**与旧版的关键差异**：① **主脑 Planner 废除**——审题、发散、深挖决策全部由专家团承担，Planner 仅作为子问题增援的临时角色存活；② 搜索与辩论合并为**单层循环**，Secretary 增量维护活文档 `plan_draft.md`；③ Verifier 的 REVISE 不再是"最多修订 1 轮后放行"，而是**打回**专家团逐条 ACCEPT/REBUT 后复审，预算内反复，预算耗尽则运行终止；④ Final Evaluator 新增 `FAIL`（完全无出路 → 打回专家团）与 `PENDING`（请求子问题增援）两个状态。

## 核心机制

1. **审题与 crux 定位**：首轮三位专家各自审题，Secretary 综合写 `strategy.md`——题意、量纲预测（Buckingham π）、极限行为、把难点定位到**具体一步**（crux）
2. **发散生成**：每位专家各提 ≥1 个**结构不同**（不同出发点/定理/数学工具）且视角不同的方向，每个方向附机器可检的**验收判据**（题面硬性要求必须逐条编码进判据）+ **预测撞墙点**
3. **深挖 + 回溯**：best-first 选前沿节点；专家团提议后续任务；验收判据不满足 = 死端，回退换路
4. **每轮碰撞**：专家互读对方文件，评估、互补、提出创新点；事实分歧（某积分收敛吗、两式数值相等吗、误差够小吗）任何专家可**动议** spawn 临时 Builder/Evaluator 算清楚；Secretary 记录并把结论沉淀进 `plan_draft.md`
5. **Verifier 击杀权**：共识定稿后单闸审查；REVISE = 打回专家团，修订后复审；达 {max_verify_rounds} 轮仍不过 → **运行终止，永不放行**
6. **Final E 三态 + 增援**：`FAIL` = 路线被执行证死 → 打回专家团重开（至多 1 次）；审查中可请求 Ephemeral Standard 三连算简单子问题
7. **树表**：Orchestrator 在 `debug/.state` 维护**纯元数据**树表（节点/父节点/状态/裁决/轮次），不读任何物理内容

## 流程

```
阶段 1：专家团循环（单层，≤ {max_iterations} 轮）
    每轮：并行三专家（提议/写任务/动议）
          → 执行新任务（临时 Builder→Evaluator，跨分支可并行）+ 并行动议
          → 并行 Critic（批评 + 成熟判定）∥ Secretary（记录 + 更新活文档）
          → 路由：
              PLAN: READY → Secretary 定稿 → final_plan.md → 阶段 2
              PLAN: SEARCH → 下一轮
              树耗尽 → 重规划轮（≤1）→ 再耗尽 → 强制收尾 → 阶段 2
              轮次预算尽 → 强制收尾 → 阶段 2
        ↓
阶段 2：Verifier 单闸（打回协议）
    Verifier → verification_plan.md（首行 SOUND / REVISE）
    SOUND → 阶段 3
    REVISE → 打回轮：专家团逐条 ACCEPT/REBUT → Secretary 修订 → 复审
    verify_round 达 {max_verify_rounds} 仍 REVISE → 运行终止（永不放行）
        ↓
阶段 3：最终执行 + 审查
    Builder → solution.md
    Evaluator → review.md（首行 PASS / REVISE / FAIL；可 PENDING 请求子问题增援）
    PASS → final_summary.md
    REVISE → 修订争议协议 → 回到 Final Builder（最多 {max_revisions} 次）
    FAIL → 完全无出路：未重入过 → 打回阶段 1（重入轮）；已重入过 → 运行终止
```

## 职责划分（重要）

**所有物理内容都由各专家角色产出。Orchestrator 只做调度。样板任务文件一律写入 `{workspace}/tasks/`。**

| 文件 | 谁写 |
|------|------|
| `tasks/task_council_{n}_<expert>.md`（样板：仅议程 + 树表元数据，不含物理内容；每轮为三位专家各写一份） | Orchestrator |
| `tasks/task_{id}.md`（验证任务：物理细节 + **验收判据** + **预测撞墙点**） | **专家团成员** |
| `tasks/task_eval_{id}.md`、`tasks/task_critic_{n}.md`、`tasks/task_secretary_*.md`、`tasks/task_verifier.md`、`tasks/task_final_builder.md`、`tasks/task_final_evaluator*.md`、`tasks/task_sub_build_{k}.md`、`tasks/task_sub_eval_{k}.md`（样板） | Orchestrator（固定模板） |
| `tasks/task_motion_{k}.md`（动议任务，含物理细节） | **提出动议的专家** |
| `tasks/task_sub_{k}.md`（子问题增援任务，含物理细节） | **Final Evaluator** |
| `strategy.md`、`council_round_{n}.md`、`plan_draft.md`、`calculations_history.md`、`final_plan.md` | Secretary |
| `theorist.md`、`computationalist.md`、`experimentalist.md` | 各专家 |
| `critic_round_{n}.md` | Critic |
| `verification_plan.md` | **Verifier** |
| `sub_plan_{k}.md` | 临时 Planner（子问题增援） |
| `calculation_{id}.md`、`calculation_motion_{k}.md`、`calculation_sub_{k}.md`、`solution.md` | Builder |
| `verification_{id}.md`、`verification_motion_{k}.md`、`verification_sub_{k}.md`、`review.md` | Evaluator |
| `debug/.state` 中的树表（纯元数据） | Orchestrator |

## 节点状态词汇（树表元数据）

| 状态 | 含义 |
|------|------|
| `ALIVE` | Evaluator 裁决 PASS，尚未展开 |
| `DEAD` | Evaluator 裁决 FAIL（验收判据不满足 = 死端），或被专家团放弃 |
| `EXPANDED` | 曾为 ALIVE，已生成子节点 |
| `BLOCKED` | Builder 无法执行（未验证，留给专家团处理） |

## Orchestrator 执行协议

### 阶段 1：专家团循环

#### 首轮（审题 + 发散生成）

为三位专家**分别**写样板任务文件——同一模板、**三个文件**，`{expert_file}` 与 `{id_namespace}` 替换为各自的值（不含物理内容）：
- Theorist → `tasks/task_council_1_theorist.md`（`{expert_file}` = `theorist.md`，`{id_namespace}` = `a`）
- Computationalist → `tasks/task_council_1_computationalist.md`（`{expert_file}` = `computationalist.md`，`{id_namespace}` = `b`）
- Experimentalist → `tasks/task_council_1_experimentalist.md`（`{expert_file}` = `experimentalist.md`，`{id_namespace}` = `c`）

```markdown
# Task council_1（审题 + 发散生成）
说明：专家团首轮——审题定位 crux，各专家提出结构不同的求解方向并写成验证任务

请阅读 `{workspace}/problem.md`。这是专家团首轮：尚无计算记录。

从你的视角：
1. 审题：题意重述、符号约定、Buckingham π 量纲预测、极限与特例行为、**crux**（难点定位到具体一步）
2. 提出 **≥1 个结构不同**的求解方向（不同出发点/不同定理/不同数学工具；不要同一思路换皮）
3. 每个方向写一个完整验证任务 `{workspace}/tasks/task_{id}.md`（标题后第一行写 `说明：<一句话目的>`）——`{id_namespace}` 中尚未使用的编号作为你的任务 id。每个任务文件必须包含：
   a. 完整物理细节（算什么、怎么算、全部参数）
   b. **验收判据**（机器可检，逐条编号）：结果形式约束、数值自检（符号结果与独立数值计算吻合，给出容差）、量纲与极限合理性、针对 crux 的专项检查；**题面写明的硬性要求**（解析解/闭合形式/精确系数/精度/结果形式等）必须逐条编码为判据，并标注"硬要求"
   c. **预测撞墙点**：预计死在哪一步、死成什么样子
   d. 与其他路线的结构差异说明
   e. 输出位置：结果写入 `{workspace}/calculation_{id}.md`（**禁止写 `solution.md`**——那是 Final Builder 的文件，覆盖会导致跨分支污染）

将审题与提案写入/更新 `{workspace}/{expert_file}`（追加"首轮"小节，保留历史）。
最终消息按你的系统提示汇报（STATUS/OUTPUT/NEXT_TASKS/MOTION/SUMMARY）。
```

三位专家的 `{expert_file}` / `{id_namespace}` 分别为：`theorist.md` / `a`（如 `task_a1.md`）、`computationalist.md` / `b`、`experimentalist.md` / `c`。

并行 spawn 三专家——**「`&` 派发 + 轮询等待」规范模式**（总则见通用编排器「并行 spawn 与轮询等待」节；等待期间你的每一次回应都必须是 Bash 工具调用，输出纯文本会立即终止会话并害死后台专家）：

派发（一个 Bash 调用，**不要**接 `wait`）：

```bash
python3 {project_root}/scripts/spawn.py Theorist {workspace} agents/theorist task_council_1_theorist --timeout {deep_timeout} &
python3 {project_root}/scripts/spawn.py Computationalist {workspace} agents/computationalist task_council_1_computationalist --timeout {deep_timeout} &
python3 {project_root}/scripts/spawn.py Experimentalist {workspace} agents/experimentalist task_council_1_experimentalist --timeout {deep_timeout} &
echo SPAWNED
```

轮询等待（重复执行，直到三路派活全部 `READY`；文件名 = `.<Role>_<任务名>.result`）：

```bash
for i in $(seq 1 38); do
  miss=""
  for f in "{workspace}/debug/.Theorist_task_council_1_theorist.result" "{workspace}/debug/.Computationalist_task_council_1_computationalist.result" "{workspace}/debug/.Experimentalist_task_council_1_experimentalist.result"; do
    [ -f "$f" ] || miss="$miss ${f##*/}"
  done
  [ -z "$miss" ] && break
  sleep 15
done
for f in "{workspace}/debug/.Theorist_task_council_1_theorist.result" "{workspace}/debug/.Computationalist_task_council_1_computationalist.result" "{workspace}/debug/.Experimentalist_task_council_1_experimentalist.result"; do
  if [ -f "$f" ]; then echo "${f##*/} READY"
  elif [ -f "${f%.result}.log" ]; then echo "${f##*/} RUNNING"
  else echo "${f##*/} NOT_STARTED"; fi
done
```

- 全部 `READY` → 收集结果
- 有 `RUNNING` → 立即再发起同一轮询调用（不输出纯文本）
- 有 `NOT_STARTED` → 该专家的 spawn 没启动：按上面的派发命令（绝对路径）重新派发该角色，继续轮询

收集三个 `.result`（`debug/.<Role>_<任务名>.result`）的 `NEXT_TASKS` 行（取文件名并集），对每个任务执行**分支处理**（见下）。随后并行 spawn Critic 与 Secretary（见下），路由。

#### 常规轮（第 $n$ 轮）

**预算检查**：写新一轮样板前，若 `council_round` 已达 `{max_iterations}`，不再开新轮，直接写**强制收尾**任务。（打回修订轮不计入此检查。）

Best-first 选出待展开节点 `{id}`（选择规则见下）后，为三位专家分别写样板——同一模板、三个文件 `tasks/task_council_{n}_theorist.md` / `task_council_{n}_computationalist.md` / `task_council_{n}_experimentalist.md`（`{expert_file}`/`{id_namespace}` 替换为各自的值）：

```markdown
# Task council_{n}（深挖轮）
说明：专家团第 {n} 轮——围绕焦点节点 {id} 提议后续验证任务或判断路线成熟/死亡

请阅读 `{workspace}/problem.md`、`strategy.md`、`plan_draft.md`、`calculations_history.md`（如存在）、
你的分析文件的历史内容、其他两位成员的分析文件（最新版本），
以及本轮焦点节点 `{id}` 及其祖先节点相关的 `calculation_*.md`、`verification_*.md`。

当前搜索树（元数据，从 `debug/.state` 原样复制）：

    {tree_table}

从你的视角提议下一步（可多项并行）：
a. 写后续验证任务 `tasks/task_{id2}.md`（格式同首轮：物理细节 + 验收判据【含硬要求编码】+ 预测撞墙点 + 输出位置；继承父节点已确认的结论；`{id_namespace}` 中未使用的编号作为任务 id；若本轮你认为不存在结构不同的替代，只写 1 个主线任务并说明理由）
b. 判断某路线已经成熟（验收判据已全部满足）或已是死端——给出理由，写入你的分析文件
c. 动议（MOTION）：对可用一次快速计算/验证解决的事实分歧，写 `tasks/task_motion_{k}.md`（编号从 {next_motion_id} 起，完整物理细节 + 通过标准，注明执行者 Builder 或 Evaluator 与输出文件）

将本轮分析写入/更新 `{workspace}/{expert_file}`（追加"第 {n} 轮"小节，保留历史）。
```

**重入轮**（Final Evaluator `FAIL` 打回后，见阶段 3）在上述样板中追加：

```markdown
上一轮最终方案被执行证死：请阅读 `{workspace}/review.md` 的 FAIL 理由与全部已有记录。
旧路线已不可挽救。请提出**本质不同**的新方向（写成新的根分支任务），并在你的分析文件中说明：
旧路线集体撞的是什么墙、新方向如何避开、crux 定位是否需要修正。
```

**重规划轮**（树耗尽且 `replan_used: 0`）改用议程：

```markdown
# Task council_{n}（重新规划）
说明：旧路线全部证死，专家团换本质不同的思路重新提出根分支方向

此前所有路线均已证死。请阅读 `{workspace}/problem.md`、`strategy.md`、`calculations_history.md`
及全部 `verification_*.md` 的失败原因（死端各卡在哪一步）。

换用与之前**本质不同**的思路，各提出 ≥1 个新的根分支方向（写成新的任务文件，格式同首轮：
验收判据同样逐条编码题面硬性要求），并在你的分析文件中说明：旧路线集体死亡撞的是什么共同的墙、
新方向如何避开、crux 的定位是否需要修正。
```

重规划轮完成后更新 `debug/.state`：`replan_used: 1`。

并行 spawn 三专家（命令同首轮，任务名换为 `task_council_{n}_theorist` / `_computationalist` / `_experimentalist`），收集 `NEXT_TASKS` 并集与 `MOTION` 行，然后：

1. **分支处理**（对每个新验证任务，跨分支可并行，见下节）
2. **动议执行**（并行，见下节）
3. 并行 spawn Critic ∥ Secretary（见下）
4. 路由（见下）

#### 分支处理（对每个新的 `task_{id}.md`）

同一分支内 Builder → Evaluator 必须顺序执行（Evaluator 依赖 Builder 的产出）；**跨分支可以并行**——运行时文件按派活隔离（`debug/.<Role>_<任务名>.result`），互不覆盖。建议同时在跑不超过 {max_concurrent_agents} 个分支（见 config），更多则分批。

每个分支的处理步骤：

1. spawn Builder：`spawn.py Builder {workspace} agents/builder task_{id} --timeout {ephemeral_timeout}`，读 `debug/.Builder_task_{id}.result`
   - `STATUS: OK` → 继续第 2 步
   - `STATUS: BLOCKED` → 树表记 `BLOCKED`，跳过本分支的评估
   - `STATUS: FAIL` → 树表记 `DEAD`（路线级死端）
2. 写样板 `tasks/task_eval_{id}.md` → spawn Evaluator：`spawn.py Evaluator {workspace} agents/evaluator task_eval_{id} --timeout {ephemeral_timeout}`
3. 读 `debug/.Evaluator_task_eval_{id}.result` 的 `VERDICT`（可用 `head -1 verification_{id}.md` 交叉验证），更新树表：`PASS` → `ALIVE`，`FAIL` → `DEAD`

并行多个分支时，把各分支的 Builder 派发命令写进同一个 Bash 调用（每行以 `&` 结尾）一次派出，按「并行 spawn 与轮询等待」节的文件清单轮询模板等待各 `.<Role>_<任务名>.result` 就绪；Builder 全部就绪后再同样并行派发各分支的 Evaluator。

**样板 `tasks/task_eval_{id}.md`：**

```markdown
# Task eval_{id}
说明：独立复核 {id} 号分支计算，逐条对照验收判据给结论

请审查 `{workspace}/calculation_{id}.md`（参考 `{workspace}/problem.md` 与 `{workspace}/tasks/task_{id}.md`，并审计 `{workspace}/scripts/builder/` 下的代码——只读，不运行）。
你的验证脚本放 `{workspace}/scripts/evaluator/task_eval_{id}/`（从 problem.md 独立转录）。
必须**逐条对照任务文件中的验收判据**给出 满足/不满足 及证据；标注"硬要求"的判据逐条单独列出。
**方法学审计**：若题面要求解析解/闭合形式，检查承担证明负担的步骤是否为解析完成——用数值步骤替代证明按相应判据判不满足。
若不满足，说明失败是否命中任务文件中的**预测撞墙点**。
将结果写入 `{workspace}/verification_{id}.md`。**输出第一行只写 `PASS` 或 `FAIL` 这一个词**（标题等一律从第二行开始）。
```

#### 动议执行

读专家角色各 `.result`（`debug/.<Role>_<任务名>.result`）的 `MOTION` 行（三专家与后续动议轮）。对每个动议，按其指定执行者派活——**多个动议可以并行派发（包括同一执行者角色的多个动议）**：运行时文件按任务名隔离，互不覆盖。并行时必须走「并行 spawn 与轮询等待」规范模式（轮询清单列出实际派发的每个 `.result` 文件名）：

- `-> Builder`：`spawn.py Builder {workspace} agents/builder task_motion_{k} --timeout {ephemeral_timeout}`
- `-> Evaluator`：`spawn.py Evaluator {workspace} agents/evaluator task_motion_{k} --timeout {ephemeral_timeout}`

只记录各自的 STATUS/VERDICT 完成状态（**不判断内容**——结果留给专家下轮阅读）。累计动议数（`motions_used`）不得超过 {max_motions}，超出的跳过并在 `debug/.state` 注明。

#### Critic 与 Secretary（每轮，并行）

为 Critic 写样板 `tasks/task_critic_{n}.md`：

```markdown
# Task critic_{n}
说明：第 {n} 轮评审——审查专家团产出、体检验收判据、判定方案是否成熟

请阅读三位专家团成员的分析文件（最新版本）、本轮新写的验证任务 `tasks/task_*.md`（如有）、
本轮新的计算/验证记录（如有），以及 `plan_draft.md`。

职责：
1. 审查三份分析与新任务：弱点、错误、冗余、结构重复，每个问题附改进建议
2. **验收判据体检**：题面硬性要求（解析解/闭合形式/精度/结果形式等）是否被各任务的验收判据逐条编码？判据是否机器可检？
3. 问题分级：**Critical**（阻碍共识、定稿前必须解决）/ **Major**（应当解决）
4. **成熟判定**：存在任一路线其验收判据已全被满足、结果形式符合题面硬性要求、且无未解决的 Critical 问题 → `PLAN: READY`；否则 → `PLAN: SEARCH`

将结果写入 `{workspace}/critic_round_{n}.md`。
```

`spawn.py Critic {workspace} agents/critic task_critic_{n} --timeout {deep_timeout}`。

为 Secretary 写样板 `tasks/task_secretary_{n}.md`：

```markdown
# Task secretary_{n}
说明：第 {n} 轮记录——轮次纪要、增量更新方案草稿与计算历史

请阅读三位专家团成员的分析文件（最新版本）、`critic_round_{n}.md`、本轮新的计算/验证记录，
以及已有的 `plan_draft.md`、`calculations_history.md`、`strategy.md`（如存在）。

做三件事：
1. 写本轮记录 `{workspace}/council_round_{n}.md`：关键观点/主要分歧/新任务与动议/本轮验证结果/下轮重点
2. 增量更新 `{workspace}/plan_draft.md`（活文档）：当前最优路线/已验证基础（引用 calculation_*.md 中已确认的结论）/风险标注/验收状态
3. 将本轮值得保留的结论（包括死分支的"为什么死"）追加到 `{workspace}/calculations_history.md`
[首轮追加：4. 综合三位成员的审题写 `{workspace}/strategy.md`：题意重述、符号约定表、量纲预测、极限行为、crux、路线图，并建 `plan_draft.md` v1]
[重规划轮追加：4. 更新 `{workspace}/strategy.md`，说明旧路线集体死亡的共同墙与新路线如何避开、crux 是否修正]
```

`spawn.py Secretary {workspace} agents/secretary task_secretary_{n} --timeout {ephemeral_timeout}`。

两者互不依赖，可并行——同样走「`&` 派发 + 轮询等待」规范模式：

```bash
python3 {project_root}/scripts/spawn.py Critic {workspace} agents/critic task_critic_{n} --timeout {deep_timeout} &
python3 {project_root}/scripts/spawn.py Secretary {workspace} agents/secretary task_secretary_{n} --timeout {ephemeral_timeout} &
echo SPAWNED
```

轮询等待（重复执行，直到两路派活全部 `READY`）：

```bash
for i in $(seq 1 38); do
  miss=""
  for f in "{workspace}/debug/.Critic_task_critic_{n}.result" "{workspace}/debug/.Secretary_task_secretary_{n}.result"; do
    [ -f "$f" ] || miss="$miss ${f##*/}"
  done
  [ -z "$miss" ] && break
  sleep 15
done
for f in "{workspace}/debug/.Critic_task_critic_{n}.result" "{workspace}/debug/.Secretary_task_secretary_{n}.result"; do
  if [ -f "$f" ]; then echo "${f##*/} READY"
  elif [ -f "${f%.result}.log" ]; then echo "${f##*/} RUNNING"
  else echo "${f##*/} NOT_STARTED"; fi
done
```

`NOT_STARTED` → 按派发命令重新派发该角色；`RUNNING` → 继续轮询。

#### 路由

读 `debug/.Critic_task_critic_{n}.result` 的 `PLAN` 行与树表：

- `PLAN: READY` → **定稿**：写样板 `tasks/task_secretary_final.md`（见下）→ `spawn.py Secretary {workspace} agents/secretary task_secretary_final --timeout {deep_timeout}`，确认其 `OUTPUT` 含 `final_plan.md` → 更新 `debug/.state`（`stage: plan_verification`）→ 进入阶段 2
- `PLAN: SEARCH` → 更新 `debug/.state`（树表 + `council_round` + `last_verdict` + `motions_used`），回到常规轮
- 前沿全空（全部 `DEAD`/`EXPANDED`，无 `ALIVE` 未展开节点）→ 树耗尽：
  - `replan_used: 0` → 写**重规划轮**样板，继续循环
  - `replan_used: 1` → 写**强制收尾**任务 → 进入阶段 2
- `council_round` 达 `{max_iterations}` → 写**强制收尾**任务 → 进入阶段 2

**定稿样板 `tasks/task_secretary_final.md`：**

```markdown
# Task secretary_final（定稿）
说明：共识已达成，综合全部记录定稿 final_plan.md

请阅读三位专家团成员分析文件的最终版本、所有 `critic_round_*.md`、所有 `council_round_*.md`、
全部动议与验证结果，以及 `plan_draft.md`、`calculations_history.md`。

综合共识，将 `{workspace}/final_plan.md` 写为**定稿**（结构按你系统提示的定稿工作）：
选定路线/步骤编号清单/已验证基础（引用 calculation_*.md 中已确认的结论）/风险标注（含未解决分歧）/验收清单。
同时增量更新 `plan_draft.md`。
```

**强制收尾样板 `tasks/task_secretary_wrapup.md`：**

```markdown
# Task secretary_wrapup（强制收尾）
说明：预算耗尽，按最优幸存路线强制写出 final_plan.md

搜索预算已用尽（或路线全部耗尽且无重规划机会）。请阅读 `{workspace}/problem.md`、
`plan_draft.md`、`calculations_history.md` 与现有全部计算/验证记录。

选择最有希望的幸存路线（或部分结果组合），写出 `{workspace}/final_plan.md`（结构按你系统提示的定稿工作）；
对未经验证的环节在方案中明确标注风险。同时增量更新 `plan_draft.md`。
```

#### Best-first 选择（纯元数据判断，不读内容）

1. 在 `ALIVE` 且未展开的节点中：**轮次最大（最深层）者优先**；同轮次取最近一次 `PASS` 的节点 → 作为常规轮焦点节点 `{id}`
2. 无 `ALIVE` 未展开节点、但树中仍有 `BLOCKED` 节点 → 让专家团处理（常规轮样板中注明 `{id}` 为 BLOCKED 节点）
3. 前沿全空 → 按路由节的树耗尽处理

### 阶段 2：方案验证（Verifier 单闸 + 打回协议）

写入样板任务文件 `tasks/task_verifier.md`：

```markdown
# Task verifier
说明：单闸审查定稿方案——题意/硬要求一致性与结构健全性，输出 SOUND 或 REVISE

请审查 `{workspace}/final_plan.md`（对照 `{workspace}/problem.md`；如需上下文可读 `{workspace}/plan_draft.md`、`{workspace}/strategy.md` 和已有的计算/验证记录）。
抽查脚本（如有）放 `{workspace}/scripts/verifier/`。
将结果写入 `{workspace}/verification_plan.md`。输出第一行必须是 SOUND 或 REVISE。
```

然后 `spawn.py Verifier {workspace} agents/verifier task_verifier`，读 `debug/.Verifier_task_verifier.result` 的 `VERDICT` 字段（可用 `head -1 verification_plan.md` 交叉验证）：

- `SOUND` → 更新 `debug/.state`（`stage: final`），进入阶段 3
- `REVISE` 且 `verify_round < {max_verify_rounds}` → **打回**（见下）
- `REVISE` 且 `verify_round` 已达 `{max_verify_rounds}` → **运行终止**：写 `{workspace}/final_summary.md`（记录：pipeline、到达阶段、`VERIFIER REJECTED after {max_verify_rounds} bounce-backs`、问题详情见 `verification_plan.md`），git 提交。**永不放行。**

#### 打回轮（第 $m$ 轮，$m$ = 新 `verify_round`）

1. 更新 `debug/.state`：`verify_round: {m}`、`stage: plan_verification`
2. 为三位专家分别写样板——同一模板、三个文件 `tasks/task_council_revise_{m}_theorist.md` / `task_council_revise_{m}_computationalist.md` / `task_council_revise_{m}_experimentalist.md`（`{expert_file}` 替换为各自的值）：

```markdown
# Task council_revise_{m}（Verifier 打回）
说明：打回轮 {m}——对 Verifier 问题清单逐条 ACCEPT/REBUT 并提修正提议

Verifier 驳回了方案。请阅读 `{workspace}/verification_plan.md` 的问题清单、
`{workspace}/final_plan.md`、`plan_draft.md` 与相关计算/验证记录。

对问题清单逐条回应：`问题k: ACCEPT`（认可，给出修正提议）或 `问题k: REBUT — 理由与证据`。
需要算清事实才能回应的，可写动议 `tasks/task_motion_{k}.md`（编号从 {next_motion_id} 起，规则同常规轮）。
将回应写入/更新 `{workspace}/{expert_file}`（追加"打回轮 {m}"小节）。
```

并行 spawn 三专家（任务名 `task_council_revise_{m}_theorist` / `_computationalist` / `_experimentalist`，其余同首轮规范模式）→ 执行动议（如有，计入 `motions_used`）。

3. 写样板 `tasks/task_critic_revise_{m}.md`：「说明：打回轮 {m} 评审——评估专家团对问题清单的回应是否可行。请阅读 `{workspace}/verification_plan.md` 的问题清单与三位专家的最新回应（其分析文件的"打回轮 {m}"小节）。评估每个 ACCEPT 的修正方向是否可行、每个 REBUT 的理由是否成立；问题分 Critical/Major 级。本轮不做成熟判定，`PLAN: NA`。写入 `{workspace}/critic_round_{n}.md`。」→ spawn Critic
4. 写样板 `tasks/task_secretary_revise_{m}.md`：「说明：打回轮 {m} 修订——按问题清单逐条修订 final_plan.md。请阅读 `{workspace}/verification_plan.md` 的问题清单、三位专家的回应与 `critic_round_{n}.md`。逐条修订 `{workspace}/final_plan.md`：ACCEPT 的问题落实修正；REBUT 且理由被 Critic 认可的保留原状并在方案风险标注中说明理由；同时增量更新 `plan_draft.md`。」→ spawn Secretary（`--timeout {deep_timeout}`）
5. 重新 spawn Verifier（重写 `tasks/task_verifier.md` 后 `spawn.py Verifier {workspace} agents/verifier task_verifier`），回到阶段 2 的裁决路由

### 阶段 3：最终执行 + 审查

#### Final Builder

```markdown
# Task final_builder
说明：按定稿方案执行完整求解，产出 solution.md

请阅读 `{workspace}/problem.md` 和 `{workspace}/final_plan.md`，执行完整求解。
将完整推导写入 `{workspace}/solution.md`，最终答案用 $\boxed{}$ 标注。
计算脚本放 `{workspace}/scripts/builder/final/`；按 final_plan 的步骤编号更新进度文件（见你的系统提示）。
```

`spawn.py Builder {workspace} agents/builder task_final_builder --timeout {timeout_seconds}`。

#### Final Evaluator（三态 + 子问题增援）

写样板 `tasks/task_final_evaluator.md`：

```markdown
# Task final_evaluator
说明：最终审查 solution.md——三态裁决（PASS/REVISE/FAIL），必要时请求子问题增援

请审查 `{workspace}/solution.md`（对照 `{workspace}/problem.md`、`{workspace}/final_plan.md`，并审计 `{workspace}/scripts/builder/` 下的代码——只读，不运行）。
你的验证脚本放 `{workspace}/scripts/evaluator/final/`（从 problem.md 独立转录）。
将结果写入 `{workspace}/review.md`。

裁决词表（第一行只写一个词）：
- `PASS`：答案正确且满足题面全部要求
- `REVISE`：存在可修复的缺陷（问题逐条列出）
- `FAIL`：**完全无出路**——路线本身被执行证死，同一路线换法执行也无法挽救（如方法与题面硬性要求冲突且路线内无替代、结果形式根本不匹配）
- `PENDING`：仅用于请求子问题增援（见下），此时若写 review.md，第一行写 PENDING（部分分析可继续写）

**方法学审计**：若题面要求解析解/闭合形式，审计 solution.md 中承担证明负担的步骤是否解析完成——用数值步骤（拟合/数值佐证/"识别"）替代证明按相应条目判不满足。

**子问题增援**：遇到必须独立算清才能裁决的**简单子问题**（引理验证、独立方法交叉核算、参数敏感性等），
写完整子任务文件 `{workspace}/tasks/task_sub_{k}.md`（标题后第一行写 `说明：<一句话目的>`；算什么/方法/全部参数/通过标准；注明执行者先写简案到 `sub_plan_{k}.md`、结果写 `calculation_sub_{k}.md`；k 从 {next_subtask_id} 起），
然后汇报 `VERDICT: PENDING` + `SUBTASKS:` 行。子任务预算剩余 {subtasks_left}；预算为 0 时**必须直接给出最终裁决**。
```

`spawn.py Evaluator {workspace} agents/evaluator task_final_evaluator --timeout {timeout_seconds}`，读 `debug/.Evaluator_task_final_evaluator.result`：

- `VERDICT: PASS` → 生成 `final_summary.md`（见通用编排器），收工
- `VERDICT: REVISE` → **修订争议协议**（见通用编排器：Builder 回击 → 必要时 Evaluator 复审，达成共识或达 {max_disputes} 上限后才修订），重写样板任务（追加"请先阅读 review.md、rebuttal/rejoin 的最终结论并修正；未解决的争议点单独标注"），重新 spawn Final Builder（修订最多 {max_revisions} 次）
- `VERDICT: FAIL` → **打回专家团重开**：
  - `reentry_used: 0` → 更新 `debug/.state`（`reentry_used: 1`，`stage: council`），写**重入轮**样板（常规轮样板追加重入议程），回到阶段 1 循环
  - `reentry_used: 1` → **运行终止**：写 `final_summary.md`（记录：两次最终审查均判 FAIL、无出路理由见 `review.md`），git 提交
- `VERDICT: PENDING` → **子问题增援协议**（见下）

#### 子问题增援协议（Ephemeral Standard 三连）

1. 读 `SUBTASKS` 行的任务文件列表；`subtasks_used` + 本轮个数超过 `{max_subtasks}` 的，只执行到预算上限，其余在 `debug/.state` 注明跳过
2. 对每个 `tasks/task_sub_{k}.md` 执行三连（单个子任务内三步必须顺序——后一步依赖前一步产出；多个子任务之间可以并行，走「并行 spawn 与轮询等待」规范模式）：
   ```bash
   python3 {project_root}/scripts/spawn.py Planner {workspace} agents/planner task_sub_{k} --timeout {ephemeral_timeout}
   # Planner（基础版）读子任务，写简案 sub_plan_{k}.md
   ```
   写样板 `tasks/task_sub_build_{k}.md`：「说明：执行子问题 {k} 的计算（简案见 sub_plan_{k}.md）。请阅读 `{workspace}/tasks/task_sub_{k}.md` 和 `{workspace}/sub_plan_{k}.md`，执行计算。将过程与结果写入 `{workspace}/calculation_sub_{k}.md`；脚本放 `{workspace}/scripts/builder/sub_{k}/`。」→ `spawn.py Builder {workspace} agents/builder task_sub_build_{k} --timeout {ephemeral_timeout}`
   写样板 `tasks/task_sub_eval_{k}.md`：「说明：独立复核子问题 {k} 的计算结果。请审查 `{workspace}/calculation_sub_{k}.md`（对照 `{workspace}/tasks/task_sub_{k}.md` 的通过标准；独立转录，你的脚本放 `{workspace}/scripts/evaluator/sub_eval_{k}/`）。将结果写入 `{workspace}/verification_sub_{k}.md`，第一行 PASS 或 FAIL。」→ `spawn.py Evaluator {workspace} agents/evaluator task_sub_eval_{k} --timeout {ephemeral_timeout}`
   更新 `subtasks_used`
3. 写样板 `tasks/task_final_evaluator_cont_{m}.md`：「说明：基于子问题增援结果完成最终裁决。你此前请求了子问题增援。请阅读 `{workspace}/review.md`（你此前的分析）与全部 `sub_plan_{k}.md`、`calculation_sub_{k}.md`、`verification_sub_{k}.md`、`tasks/task_sub_{k}.md`。基于增援结果完成对 `{workspace}/solution.md` 的审查，重写 `{workspace}/review.md`（第一行为最终裁决）。〔预算耗尽时追加：子问题预算已用完，本轮必须直接给出 PASS/REVISE/FAIL，不允许再 PENDING。〕」→ `spawn.py Evaluator {workspace} agents/evaluator task_final_evaluator_cont_{m} --timeout {timeout_seconds}`
4. 回到 Final Evaluator 的裁决路由。防御规则：再次 `PENDING` 但 `SUBTASKS` 为空、或 `subtasks_used` 已达 `{max_subtasks}` → 按 `REVISE` 路由（在 `debug/.state` 记录该防御处理）

## Agent 配置

### Theorist / Computationalist / Experimentalist（专家团成员，主脑）
- 基础版本：`agents/theorist.md`、`agents/computationalist.md`、`agents/experimentalist.md`
- **差分：** 三种议程——首轮（审题 + 各提 ≥1 个结构不同方向 + 写完整任务书：验收判据逐条编码题面硬性要求 + 预测撞墙点）、常规轮（深挖提议/成熟判断/动议）、打回轮（对问题清单逐条 ACCEPT/REBUT）；HANDOFF 含 `NEXT_TASKS` 与 `MOTION` 行
- 超时 `{deep_timeout}` 秒

### Critic
- 基础版本：`agents/critic.md`
- **差分：** 建设性批评者 + 验收判据体检（硬要求编码完整性）+ **成熟判定**；HANDOFF 的 `PLAN: READY | SEARCH | NA` 是 Orchestrator 的路由依据；问题分 Critical（阻碍共识、定稿前必须解决）/ Major 两级；SUMMARY 含 `Critical: X, Major: Y` 计数
- 超时 `{deep_timeout}` 秒

### Secretary
- 基础版本：`agents/secretary.md`
- **差分：** 三工作——轮次记录（`council_round_{n}.md` + 增量更新活文档 `plan_draft.md` + 追加 `calculations_history.md`；首轮另写 `strategy.md`）、定稿（`final_plan.md`）、打回修订（按 `verification_plan.md` 问题清单逐条修订）；也承担强制收尾
- 轮次记录超时 `{ephemeral_timeout}` 秒；定稿与打回修订超时 `{deep_timeout}` 秒

### Verifier
- 基础版本：`agents/verifier.md`
- 输入：problem.md + final_plan.md（+ plan_draft.md、strategy.md 等上下文）
- 输出：`verification_plan.md`，第一行必须 `SOUND` 或 `REVISE`；最终消息为 HANDOFF 格式（`VERDICT`）
- 职责：审查方案的题意一致性（含题面硬性要求）、内部自洽性与结构健全性（允许短小数值抽查，禁止完整推导）；**REVISE = 打回专家团**，修订后复审，上限 `{max_verify_rounds}` 轮，耗尽即运行终止——永不放行

### Builder（临时模式）
- 基础版本：`agents/builder.md`
- **差分：** 只验证小结论、执行动议或子任务增援；结果必须写入任务指定的 `calculation_{id}.md` / `calculation_motion_{k}.md` / `calculation_sub_{k}.md`，**禁止写 `solution.md`**（那是 Final Builder 的文件，覆盖会导致跨分支污染）；超时 `{ephemeral_timeout}` 秒；最终消息为 HANDOFF 格式

### Evaluator（临时模式）
- 基础版本：`agents/evaluator.md`
- **差分：** 输出 `verification_{id}.md`（或动议/子任务的 `verification_motion_{k}.md` / `verification_sub_{k}.md`），第一行必须 `PASS` 或 `FAIL`；验证任务必须**逐条对照任务文件中的验收判据**给出 满足/不满足 及证据（验收判据不满足 = 死端信号），失败时说明是否命中预测撞墙点；超时 `{ephemeral_timeout}` 秒；最终消息为 HANDOFF 格式（`VERDICT`）

### Planner（仅子问题增援，临时模式）
- 基础版本：`agents/planner.md`（"一种方法"纪律适用于简单子问题）
- 输入：Final Evaluator 写的 `tasks/task_sub_{k}.md`；输出：`sub_plan_{k}.md`（简案）
- 超时 `{ephemeral_timeout}` 秒

### Builder / Evaluator（最终模式）
- 使用基础版本（无差分），最终消息为 HANDOFF 格式；最终审查裁决词表为 `PASS / REVISE / FAIL`（可 `PENDING` + `SUBTASKS` 请求增援）

## 状态管理

`debug/.state` 示例（每完成一个阶段更新；树表为纯元数据）：

专家团循环：

```
pipeline: deep_search
stage: council
council_round: 3
last_verdict: PASS
motions_used: 2
replan_used: 0
reentry_used: 0
subtasks_used: 0
tree:
  a1: parent=ROOT status=DEAD round=1
  b1: parent=ROOT status=EXPANDED round=1
  b2: parent=b1 status=ALIVE round=2
next: Council round 4 (expand b2)
```

方案验证（打回中）：

```
pipeline: deep_search
stage: plan_verification
council_round: 7
verify_round: 1
last_verdict: REVISE
next: Council revise round 1 (task_council_revise_1_*)
```

最终阶段（子问题增援中）：

```
pipeline: deep_search
stage: final
verify_round: 2
last_verdict: PENDING
subtasks_used: 1
next: Subtask triad task_sub_2 + Final Evaluator continuation
```

- `council_round`：专家团循环轮次（1..{max_iterations}）
- `verify_round`：已执行的打回轮数（0 = 首次审查），上限 {max_verify_rounds}
- `motions_used`：累计已执行动议数，上限 {max_motions}
- `replan_used` 取值 0/1，强制执行"重新规划至多 1 次"
- `reentry_used` 取值 0/1，强制执行"Final E FAIL 打回重开至多 1 次"
- `subtasks_used`：累计已执行子任务增援数，上限 {max_subtasks}
- 进入修订争议协议时写 `dispute_round: <n>`

## 定位：何时选哪条流水线

| 流水线 | 适用场景 |
|--------|----------|
| `deep_search` | **难题默认**：crux 不明、候选路线多、易撞死端、方案须经多视角碰撞达成共识（前沿问题首选） |
| `tree_search` | 数条结构不同路线竞争、题意明确、不需要专家团共识 |
| `adaptive` | 方向明确、单路径深入验证 |
| `standard` | 方法明确、一步到位的题 |

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `max_iterations`: {max_iterations}（专家团循环轮数）
- `max_verify_rounds`: {max_verify_rounds}（Verifier 打回轮数上限，耗尽即终止）
- `max_motions`: {max_motions}（动议总数上限）
- `max_subtasks`: {max_subtasks}（Final E 子问题增援总数上限）
- `ephemeral_timeout`: {ephemeral_timeout}（临时 Builder/Evaluator、动议执行、子问题三连、轮次记录）
- `deep_timeout`: {deep_timeout}（专家发言、Critic、Verifier、定稿与打回修订）
