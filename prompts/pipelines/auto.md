# Auto Pipeline

## 概述

**Orchestrator 自组结构**：先派 Assessor 评估题目难度（元信息，不解题），再由 Orchestrator 依据**决策表**在**阶段词表**（封闭词表，7 个阶段）内为自己组装一条蓝图（`auto_plan.md`，纯调度元数据），然后逐阶段派活执行。执行过程中遭遇结构性失败（路线全灭、最终审查证死）可启动**升级协议**：把蓝图就地加强（只升不降）；预算与检查点脚手架保证长程运行的稳定性。

auto 不发明任何新的求解机制——它的全部阶段都复用现有流水线的成熟协议，只新增"自组 + 升级 + 预算脚手架"这一层。适用场景：**不想手选流水线**、题目难度事先未知、或希望系统按难度自适应分配算力。

## 集大成：各机制的来源

| 机制 | 来源 | 在 auto 中的作用 |
|------|------|------------------|
| 难度评估（元信息审题） | auto 新设 | 阶段 0：为蓝图提供依据 |
| 单路线规划 | Standard | `plan` 阶段 |
| 专家团发散 + 临时 Builder/Evaluator 逐支验证 + 树表 | Deep Search / Tree Search | `diverge` 阶段 |
| best-first 深挖、迭代加深 | Tree Search / Deep Search | `search` 阶段 |
| 多专家碰撞 + Critic 仲裁 + Secretary 记录 | Debate | `debate` 阶段 |
| Secretary 定稿 / 强制收尾 | Debate / Deep Search | `synthesize` 阶段 |
| Verifier 单闸 + 打回修订 + 永不放行 | Deep Search | `gate` 阶段 |
| Final Builder/Evaluator + 修订争议协议 | 通用编排器 | `final` 阶段 |
| 升级协议 + 预算/检查点脚手架 | auto 新设 | 长程稳定性 |

## 阶段词表（封闭集合——蓝图只许用这 7 个阶段名）

| 阶段 | 做什么 | 派活消耗（粗估） | 产出 |
|------|--------|------------------|------|
| `plan` | Planner 单路线规划 | 1 | `plan.md` |
| `diverge` | 三专家各提 ≥1 条结构不同路线（写成验证任务），临时 Builder→Evaluator 逐支验证 | 3 + 2×任务数 | 树表（`.state`） |
| `search` | 三专家读树表与记录，沿幸存路线提后续任务并执行（≤ {max_search_rounds} 轮） | 每轮 ≈ 3 + 2×新任务数 | 更深的树表 |
| `debate` | Critic 批评专家分析 → 专家回应 → Secretary 记录（≤ {max_debate_rounds} 轮） | 每轮 ≈ 5 | `debate_summary_round_{n}.md` |
| `synthesize` | Secretary 定稿：综合幸存路线/共识写 `final_plan.md` | 1 | `final_plan.md` |
| `gate` | Verifier 审查 `final_plan.md`；REVISE = 打回专家团逐条修订后复审（≤ {max_verify_rounds} 轮） | 1 + 每轮打回 ≈ 5 | `verification_plan.md` |
| `final` | Final Builder 执行 → Final Evaluator 三态裁决（修订争议协议） | 2 + 修订 | `solution.md` / `review.md` |

**序列硬约束**：
- 必须以 `final` 结尾
- `synthesize` 必须先于 `gate`（`gate` 审的是 `final_plan.md`）
- `diverge` 必须先于 `search`（深挖以发散产生的树表为前提）
- `debate` 必须在 `diverge` 或 `search` 之后（辩论对象是专家分析文件，由这两个阶段产生）
- 蓝图长度 ≤ {max_phases}

## 流程

```
阶段 0：评估（固定执行，不计入蓝图）
    Assessor → difficulty_assessment.md（首行 DIFFICULTY: ...）
        ↓
阶段 1：蓝图（Orchestrator 自写——纯调度元数据，零物理内容）
    决策表（难度 → 默认序列）+ Assessor 的 FORM/STEPS/RECOMMENDED 微调
    → auto_plan.md + .state（phases / phase_index: 0 / spawn_count: 0）
        ↓
阶段 2：按蓝图逐阶段执行（各阶段协议见下）
    每个阶段：开始前 cat .state 对表 → 执行 → 立即回写 .state
        ↓（执行中触发）
升级协议（≤ {max_escalations} 次）
    结构性失败 → 蓝图就地加强（只升不降）→ 重入对应阶段
    升级用尽 / 蓝图已最强 / 预算尽 → 强制收尾
        ↓
收工：final_summary.md
```

## 决策表（难度 → 默认蓝图）

| 难度 | 默认蓝图 | 派活粗估 |
|------|----------|----------|
| `EASY` | `plan > final` | ~3 |
| `MEDIUM` | `plan > synthesize > gate > final` | ~7 |
| `HARD` | `plan > diverge > synthesize > gate > final` | ~15 |
| `FRONTIER` | `diverge > search > debate > synthesize > gate > final` | ~30 |

**微调规则**（只允许以下操作，且必须维持序列硬约束）：
1. 参考 Assessor 的 `RECOMMENDED` 行——它与默认表冲突时，以默认表为准，除非它满足下面第 2/3 条
2. `STEPS ≤ 3` 且 `FORM: numeric` → 可降为更简蓝图；`FORM: analytic` 且难度 ≥ `MEDIUM` → 蓝图必须含 `gate`
3. 插入或删除一个非 `final` 阶段（如给 `HARD` 追加 `search`），插入位置必须满足词表约束
4. 微调理由写入 `auto_plan.md` 的 `ADJUSTMENTS` 行（一句话，元数据，无物理内容）

## Orchestrator 执行协议

### 阶段 0：评估

写样板 `tasks/task_assessor.md`：

```markdown
# Task assessor
说明：评估题目难度与结构，为蓝图自组提供依据（只评估不求解）

请阅读 `{workspace}/problem.md`，按你的系统提示将评估写入 `{workspace}/difficulty_assessment.md`。
第一行必须是 `DIFFICULTY: <EASY|MEDIUM|HARD|FRONTIER>`。
```

`spawn.py Assessor {workspace} agents/assessor task_assessor --timeout {ephemeral_timeout}`，读 `debug/.Assessor_task_assessor.result`：

- `STATUS: OK` → 记录 `DIFFICULTY`/`FORM`/`STEPS`/`RECOMMENDED` 四行，进入阶段 1
- `STATUS: FAIL` → 重试一次（不加 `--resume`）；仍 `FAIL` → **保守兜底**：按 `HARD` 默认蓝图执行，在 `.state` 注明 `assessor: FAILED`

**本流水线信息管制补充**：`auto_plan.md`（你自己写的纯调度元数据）与 `difficulty_assessment.md` 的**第一行**（`head -1`）加入你的可读白名单；`difficulty_assessment.md` 正文仍属内容文件，不得读。

### 阶段 1：蓝图

1. 按决策表选默认序列，套用微调规则
2. 写 `{workspace}/auto_plan.md`（**纯调度元数据，零物理内容**）：

```markdown
# Auto Plan（蓝图）
DIFFICULTY: HARD
PHASES: plan > diverge > synthesize > gate > final
BUDGET: max_phases={max_phases} max_spawns={max_spawns} max_escalations={max_escalations}
ADJUSTMENTS: <微调说明一句话，或"无，采用默认">
CHECKLIST:
- [ ] plan
- [ ] diverge
- [ ] synthesize
- [ ] gate
- [ ] final
```

3. 写 `debug/.state`（见「状态管理」），`phase_index: 0`、`spawn_count: 1`（Assessor 已计入）

### 阶段 2：阶段库

**每个阶段的固定动作**（脚手架，见「长程脚手架」节）：开始前 `cat debug/.state` 核对 `phase_index` 与 `next`；结束后立即回写 `.state`（`phase_index` +1、`spawn_count`、`last_verdict`、`next`）并勾选 `auto_plan.md` 的 CHECKLIST。

#### plan

写样板 `tasks/task_plan.md`：

```markdown
# Task plan
说明：单路线规划——读题写 plan.md

请阅读 `{workspace}/problem.md`，按你的系统提示制定解题计划，写入 `{workspace}/plan.md`。
```

`spawn.py Planner {workspace} agents/planner task_plan`，读 `debug/.Planner_task_plan.result`：

- `STATUS: OK` → 阶段完成
- `STATUS: FAIL`/`BLOCKED` → 重试一次（不加 `--resume`）；仍失败 → **升级协议**（触发条件 1）

#### diverge

为三位专家**分别**写样板——同一模板、三个文件 `tasks/task_diverge_theorist.md` / `task_diverge_computationalist.md` / `task_diverge_experimentalist.md`（`{expert_file}` 与 `{id_namespace}` 替换为各自的值：`theorist.md`/`a`、`computationalist.md`/`b`、`experimentalist.md`/`c`；不含物理内容）：

```markdown
# Task diverge（审题 + 发散生成）
说明：专家团发散——审题定位 crux，提出结构不同的求解方向并写成验证任务

请阅读 `{workspace}/problem.md`。这是发散轮：尚无计算记录
〔若蓝图含 plan 阶段，追加：已有单路线规划 `{workspace}/plan.md` 可作参考，但你完全可以提出与之结构不同的路线〕
〔若为重入轮（升级协议触发），追加：此前路线已被证死，请阅读 `{workspace}/review.md` 的 FAIL 理由；提出**本质不同**的新方向〕

从你的视角：
1. 审题：题意重述、符号约定、Buckingham π 量纲预测、极限与特例行为、**crux**（难点定位到具体一步）
2. 提出 **≥1 个结构不同**的求解方向（不同出发点/不同定理/不同数学工具；不要同一思路换皮）
3. 每个方向写一个完整验证任务 `{workspace}/tasks/task_{id}.md`（标题后第一行写 `说明：<一句话目的>`）——`{id_namespace}` 中尚未使用的编号作为你的任务 id。每个任务文件必须包含：
   a. 完整物理细节（算什么、怎么算、全部参数）
   b. **验收判据**（机器可检，逐条编号）：结果形式约束、数值自检（符号结果与独立数值计算吻合，给出容差）、量纲与极限合理性、针对 crux 的专项检查；**题面写明的硬性要求**（解析解/闭合形式/精确系数/精度/结果形式等）必须逐条编码为判据，并标注"硬要求"
   c. **预测撞墙点**：预计死在哪一步、死成什么样子
   d. 与其他路线的结构差异说明
   e. 输出位置：结果写入 `{workspace}/calculation_{id}.md`（**禁止写 `solution.md`**——那是 Final Builder 的文件）

将审题与提案写入/更新 `{workspace}/{expert_file}`（追加小节，保留历史）。
最终消息按你的系统提示汇报（STATUS/OUTPUT/NEXT_TASKS/MOTION/SUMMARY）。
```

并行 spawn 三专家——**「`&` 派发 + 轮询等待」规范模式**（总则见通用编排器「并行 spawn 与轮询等待」节；等待期间你的每一次回应都必须是 Bash 工具调用，输出纯文本会立即终止会话并害死后台专家）：

```bash
python3 {project_root}/scripts/spawn.py Theorist {workspace} agents/theorist task_diverge_theorist --timeout {deep_timeout} &
python3 {project_root}/scripts/spawn.py Computationalist {workspace} agents/computationalist task_diverge_computationalist --timeout {deep_timeout} &
python3 {project_root}/scripts/spawn.py Experimentalist {workspace} agents/experimentalist task_diverge_experimentalist --timeout {deep_timeout} &
echo SPAWNED
```

轮询等待（重复执行，直到三路派活全部 `READY`）：

```bash
for i in $(seq 1 38); do
  miss=""
  for f in "{workspace}/debug/.Theorist_task_diverge_theorist.result" "{workspace}/debug/.Computationalist_task_diverge_computationalist.result" "{workspace}/debug/.Experimentalist_task_diverge_experimentalist.result"; do
    [ -f "$f" ] || miss="$miss ${f##*/}"
  done
  [ -z "$miss" ] && break
  sleep 15
done
for f in "{workspace}/debug/.Theorist_task_diverge_theorist.result" "{workspace}/debug/.Computationalist_task_diverge_computationalist.result" "{workspace}/debug/.Experimentalist_task_diverge_experimentalist.result"; do
  if [ -f "$f" ]; then echo "${f##*/} READY"
  elif [ -f "${f%.result}.log" ]; then echo "${f##*/} RUNNING"
  else echo "${f##*/} NOT_STARTED"; fi
done
```

- 全部 `READY` → 收集结果
- 有 `RUNNING` → 立即再发起同一轮询调用（不输出纯文本）
- 有 `NOT_STARTED` → 按上面的派发命令重新派发该角色，继续轮询

收集三个 `.result` 的 `NEXT_TASKS` 行（取文件名并集；auto 不使用动议——`MOTION` 行一律忽略，事实分歧留给 `debate` 阶段）。对每个新验证任务执行**分支处理**：

**分支处理**：同一分支内 Builder → Evaluator 必须顺序执行；**跨分支可以并行**——运行时文件按派活隔离，互不覆盖。建议同时在跑不超过 {max_concurrent_agents} 个分支（见 config），更多则分批。

1. `spawn.py Builder {workspace} agents/builder task_{id} --timeout {ephemeral_timeout}`，读 `debug/.Builder_task_{id}.result`
   - `STATUS: OK` → 继续第 2 步
   - `STATUS: BLOCKED` → 树表记 `BLOCKED`，跳过本分支评估
   - `STATUS: FAIL` → 树表记 `DEAD`（路线级死端）
2. 写样板 `tasks/task_eval_{id}.md` → `spawn.py Evaluator {workspace} agents/evaluator task_eval_{id} --timeout {ephemeral_timeout}`
3. 读 `debug/.Evaluator_task_eval_{id}.result` 的 `VERDICT`（可用 `head -1 verification_{id}.md` 交叉验证），更新树表：`PASS` → `ALIVE`，`FAIL` → `DEAD`

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

**路由**：树表出现 ≥1 个 `ALIVE` → 阶段完成；全部 `DEAD`/`BLOCKED` 且无 `ALIVE` → **升级协议**（触发条件 2）。

#### search

深挖轮（第 $n$ 轮，$n$ 从 1 到 {max_search_rounds}）。Best-first 选焦点：`ALIVE` 且未展开节点中轮次最大者优先；无 `ALIVE` 但有 `BLOCKED` → 焦点取 `BLOCKED` 节点；前沿全空 → **升级协议**（触发条件 2）。

为三位专家分别写样板 `tasks/task_search_{n}_theorist.md` / `_computationalist.md` / `_experimentalist.md`（`{expert_file}`/`{id_namespace}` 同上）：

```markdown
# Task search_{n}（深挖轮）
说明：专家团深挖第 {n} 轮——围绕焦点节点 {id} 提议后续验证任务或判断路线成熟/死亡

请阅读 `{workspace}/problem.md`、你的分析文件的历史内容、其他两位成员的分析文件（最新版本），
以及焦点节点 `{id}` 及其祖先节点相关的 `calculation_*.md`、`verification_*.md`
〔蓝图含 plan 阶段且 plan.md 存在时追加：与 `{workspace}/plan.md`〕。

当前搜索树（元数据，从 `debug/.state` 原样复制）：

    {tree_table}

从你的视角提议下一步（可多项）：
a. 写后续验证任务 `tasks/task_{id2}.md`（格式同发散轮：物理细节 + 验收判据【含硬要求编码】+ 预测撞墙点 + 输出位置 `calculation_{id2}.md`；继承父节点已确认的结论；`{id_namespace}` 中未使用的编号作为任务 id；若本轮你认为不存在结构不同的替代，只写 1 个主线任务并说明理由）
b. 判断某路线已经成熟（验收判据已全部满足）或已是死端——给出理由，写入你的分析文件

本轮无动议机制（事实分歧留待 debate 阶段）：`MOTION` 行写 NONE。
将本轮分析写入/更新 `{workspace}/{expert_file}`（追加"深挖第 {n} 轮"小节，保留历史）。
```

并行 spawn 三专家（任务名 `task_search_{n}_theorist` / `_computationalist` / `_experimentalist`，命令与轮询同 `diverge`，文件清单换名），收集 `NEXT_TASKS` 并集：

- 并集非空 → 对新任务执行**分支处理**（同 `diverge`），更新树表与 `spawn_count`
- 并集为空（三专家均 `NEXT_TASKS: NONE`）→ 深挖收敛，阶段完成
- 新验证后前沿全空（无 `ALIVE`）→ **升级协议**（触发条件 2）
- $n$ 达 {max_search_rounds} → 阶段完成（带着现有树表前进）

#### debate

辩论轮（第 $n$ 轮，$n$ 从 1 到 {max_debate_rounds}）。前提：三位专家的分析文件已存在（来自 `diverge`/`search`；若蓝图不含它们——不应出现，序列约束保证 `debate` 前已有专家文件）。

1. 写样板 `tasks/task_debate_critic_{n}.md`：

```markdown
# Task debate_critic_{n}
说明：辩论第 {n} 轮——批评三份专家分析，判定是否已达成共识

请阅读 `{workspace}/problem.md`、`{workspace}/theorist.md`、`{workspace}/computationalist.md`、`{workspace}/experimentalist.md`
以及已有的 `critic_round_*.md`、`debate_summary_round_*.md`（如有）。
将批评写入 `{workspace}/critic_round_{n}.md`；问题分 Critical（阻碍定稿）/ Major 两级。
**共识判定**：存在任一路线其论证已足够完整、无 Critical 问题、可据此定稿 → `PLAN: READY`；否则 `PLAN: SEARCH`。
```

`spawn.py Critic {workspace} agents/critic task_debate_critic_{n} --timeout {deep_timeout}`，读 `debug/.Critic_task_debate_critic_{n}.result`：

- `PLAN: READY` 或 SUMMARY 中 `Critical: 0` → 共识达成，阶段完成
- 否则继续第 2 步

2. 专家回应——写三个样板 `tasks/task_debate_respond_{n}_theorist.md` / `_computationalist.md` / `_experimentalist.md`（措辞同理）：

```markdown
# Task debate_respond_{n}
说明：辩论第 {n} 轮——Theorist 回应批评并更新分析

请阅读 `{workspace}/problem.md`、`{workspace}/critic_round_{n}.md` 和你此前的分析 `{workspace}/theorist.md`。
回应批评（逐条：接受并修正 / 反驳并给证据），原地更新 `{workspace}/theorist.md`。
`NEXT_TASKS` 行写 NONE；`MOTION` 行写 NONE。
```

三专家并行派发与轮询（规范模式，文件清单 `.Theorist_task_debate_respond_{n}_theorist.result` 等）。

3. 写样板 `tasks/task_debate_secretary_{n}.md`：

```markdown
# Task debate_secretary_{n}
说明：记录辩论第 {n} 轮要点

请阅读 `{workspace}/problem.md`、三份专家分析（最新版本）和 `{workspace}/critic_round_{n}.md`。
将第 {n} 轮辩论记录写入 `{workspace}/debate_summary_round_{n}.md`。
```

`spawn.py Secretary {workspace} agents/secretary task_debate_secretary_{n} --timeout {ephemeral_timeout}`，确认 `OUTPUT` 含 `debate_summary_round_{n}.md`。

**路由**：`PLAN: SEARCH` 且 $n$ < {max_debate_rounds} → 下一轮；否则阶段完成（带着现有共识/分歧进入 `synthesize`，分歧由定稿的风险标注承接）。

#### synthesize

写样板 `tasks/task_synthesize.md`：

```markdown
# Task synthesize（定稿）
说明：综合全部记录定稿 final_plan.md

请阅读已有全部记录：`plan.md`（如有）、三位专家分析文件的最终版本、所有 `critic_round_*.md`、
`debate_summary_round_*.md`（如有）、全部 `calculation_*.md` 与 `verification_*.md` 的结论。

综合幸存路线与共识，将 `{workspace}/final_plan.md` 写为**定稿**（结构按你系统提示的定稿工作）：
选定路线（注明数值/解析约定）/步骤编号清单/已验证基础（引用 calculation_*.md 中已确认的结论）/
风险标注（含未解决分歧）/验收清单。
```

`spawn.py Secretary {workspace} agents/secretary task_synthesize --timeout {deep_timeout}`，读 `debug/.Secretary_task_synthesize.result`：

- `OUTPUT` 含 `final_plan.md` 且文件非空（`wc -c` 验证）→ 阶段完成
- 否则重试一次；仍失败 → 记 `debug/.errors.log`，**升级协议**（触发条件 4）

#### gate

写样板 `tasks/task_verifier.md`：

```markdown
# Task verifier
说明：单闸审查定稿方案——题意/硬要求一致性与结构健全性，输出 SOUND 或 REVISE

请审查 `{workspace}/final_plan.md`（对照 `{workspace}/problem.md`；如需上下文可读已有的计算/验证记录与专家分析文件）。
抽查脚本（如有）放 `{workspace}/scripts/verifier/`。
将结果写入 `{workspace}/verification_plan.md`。输出第一行必须是 SOUND 或 REVISE。
```

`spawn.py Verifier {workspace} agents/verifier task_verifier`，读 `debug/.Verifier_task_verifier.result` 的 `VERDICT`（可用 `head -1 verification_plan.md` 交叉验证）：

- `SOUND` → 阶段完成
- `REVISE` 且 `verify_round` < {max_verify_rounds} → **打回轮**（见下）
- `REVISE` 且 `verify_round` 已达 {max_verify_rounds} → **运行终止**：写 `final_summary.md`（记录 `VERIFIER REJECTED after {max_verify_rounds} bounce-backs`，问题详情见 `verification_plan.md`），git 提交。**永不放行**——质量闸门不接受升级绕过。

**打回轮**（第 $m$ 轮，$m$ = 新 `verify_round`）：

1. 更新 `.state`：`verify_round: {m}`
2. 为三位专家分别写样板 `tasks/task_gate_revise_{m}_theorist.md` / `_computationalist.md` / `_experimentalist.md`：

```markdown
# Task gate_revise_{m}（Verifier 打回）
说明：打回轮 {m}——对 Verifier 问题清单逐条 ACCEPT/REBUT 并提修正提议

Verifier 驳回了方案。请阅读 `{workspace}/verification_plan.md` 的问题清单、
`{workspace}/final_plan.md` 与相关计算/验证记录。

对问题清单逐条回应：`问题k: ACCEPT`（认可，给出修正提议）或 `问题k: REBUT — 理由与证据`。
将回应写入/更新 `{workspace}/{expert_file}`（追加"打回轮 {m}"小节）。
`NEXT_TASKS` 行写 NONE；`MOTION` 行写 NONE。
```

三专家并行派发与轮询（规范模式）。

3. 写样板 `tasks/task_gate_secretary_{m}.md`：「说明：打回轮 {m} 修订——按问题清单逐条修订 final_plan.md。请阅读 `{workspace}/verification_plan.md` 的问题清单与三位专家的最新回应（其分析文件的"打回轮 {m}"小节）。逐条修订 `{workspace}/final_plan.md`：ACCEPT 的问题落实修正；REBUT 的问题保留原状并在方案风险标注中说明理由。」→ `spawn.py Secretary {workspace} agents/secretary task_gate_secretary_{m} --timeout {deep_timeout}`
4. 重写 `tasks/task_verifier.md` → 重新 spawn Verifier，回到 gate 的裁决路由

#### final

**Final Builder**——写样板 `tasks/task_final_builder.md`：

```markdown
# Task final_builder
说明：按定稿方案执行完整求解，产出 solution.md

请阅读 `{workspace}/problem.md` 与定稿方案——`{workspace}/final_plan.md`（若蓝图未含 synthesize 阶段而不存在，则读 `{workspace}/plan.md`），执行完整求解。
将完整推导写入 `{workspace}/solution.md`，最终答案用 $\boxed{}$ 标注。
计算脚本放 `{workspace}/scripts/builder/final/`；按方案步骤编号更新进度文件（见你的系统提示）。
```

`spawn.py Builder {workspace} agents/builder task_final_builder --timeout {timeout_seconds}`，读 `debug/.Builder_task_final_builder.result`（`OK` → 继续；`BLOCKED` → 重试一次；仍失败 → **升级协议**触发条件 3 按 `FAIL` 处理）。

**Final Evaluator（三态）**——写样板 `tasks/task_final_evaluator.md`：

```markdown
# Task final_evaluator
说明：最终审查 solution.md——三态裁决（PASS/REVISE/FAIL）

请审查 `{workspace}/solution.md`（对照 `{workspace}/problem.md` 与定稿方案 `{workspace}/final_plan.md`——不存在则 `{workspace}/plan.md`；并审计 `{workspace}/scripts/builder/` 下的代码——只读，不运行）。
你的验证脚本放 `{workspace}/scripts/evaluator/final/`（从 problem.md 独立转录）。
将结果写入 `{workspace}/review.md`。

裁决词表（第一行只写一个词）：
- `PASS`：答案正确且满足题面全部要求
- `REVISE`：存在可修复的缺陷（问题逐条列出）
- `FAIL`：**完全无出路**——路线本身被执行证死，同一路线换法执行也无法挽救（如方法与题面硬性要求冲突且路线内无替代、结果形式根本不匹配）

**方法学审计**：若题面要求解析解/闭合形式，审计 solution.md 中承担证明负担的步骤是否解析完成——用数值步骤（拟合/数值佐证/"识别"）替代证明按相应条目判不满足。
```

`spawn.py Evaluator {workspace} agents/evaluator task_final_evaluator --timeout {timeout_seconds}`，读 `debug/.Evaluator_task_final_evaluator.result`：

- `VERDICT: PASS` → 生成 `final_summary.md`（见通用编排器），收工
- `VERDICT: REVISE` → **修订争议协议**（见通用编排器：Builder 回击 → 必要时 Evaluator 复审，达成共识或达 {max_disputes} 上限后才修订），重写样板任务（追加"请先阅读 review.md、rebuttal/rejoin 的最终结论并修正；未解决的争议点单独标注"），重新 spawn Final Builder（修订最多 {max_revisions} 次）；修订次数耗尽仍 `REVISE` → 收工（`final_summary.md` 记录未决争议）
- `VERDICT: FAIL` → **升级协议**（触发条件 3）

## 升级协议（escalation，≤ {max_escalations} 次）

**触发条件**：
1. `plan` 阶段重试后仍失败
2. `diverge`/`search` 后前沿全空（无 `ALIVE` 节点）
3. `final` 阶段 Final Builder 重试后仍失败，或 Final Evaluator 判 `FAIL`
4. `synthesize` 重试后仍失败

**协议**：

1. 检查 `escalations_used`：已达 {max_escalations}，或蓝图已是**最强形态**（含 `diverge`+`search`+`debate`），或 `spawn_count` + 估算新阶段开销 > {max_spawns} → **强制收尾**（见下）
2. 否则 `escalations_used` +1，**升级蓝图**（只升不降，只许以下操作）：
   - 触发 1 → 弃用 `plan`，剩余序列替换为 `diverge > search > synthesize > gate > final`（超长则截去 `search`）
   - 触发 2 → 蓝图缺 `search` 则在当前位置插入 `search`；已有 `search` 则插入 `debate`；两者皆备则强制收尾
   - 触发 3 → 在 `final` 之前插入 `diverge`（附重入议程：读 `review.md` 的 FAIL 理由，提本质不同的新路线；旧树表全部记 `DEAD` 保留历史）；已有 `diverge` 则插 `debate`；皆备则强制收尾
   - 触发 4 → 直接强制收尾（让 Secretary 在收尾任务里按最优幸存记录硬写 `final_plan.md`）
   - 升级后序列长度仍须 ≤ {max_phases}（超出则按上表顺序截去最弱的可截阶段：`debate` → `search` → `gate`——**`final` 与 `synthesize` 不可截**）
3. 重写 `auto_plan.md`：追加一段 `UPGRADE {k}`（触发条件、旧 PHASES、新 PHASES），更新 PHASES 与 CHECKLIST（已完成的阶段保持勾选）
4. 更新 `.state`（`phases`、`phase_index` 指向新序列中的当前位置、`escalations_used`），重入对应阶段

**强制收尾**：
- `final_plan.md` 不存在 → 写样板 `tasks/task_wrapup.md`：「说明：预算耗尽，按最优幸存记录强制写出 final_plan.md。请阅读 `{workspace}/problem.md` 与现有全部记录（plan.md、专家分析、calculation_*.md、verification_*.md、debate 记录）。选择最有希望的幸存路线（或部分结果组合）写出 `{workspace}/final_plan.md`；未经验证的环节明确标注风险。」→ `spawn.py Secretary {workspace} agents/secretary task_wrapup --timeout {deep_timeout}`
- 随后蓝图跳至 `final`（若 `final` 恰是当前被触发的阶段——触发 3 的收尾：直接写 `final_summary.md` 记录 `AUTO EXHAUSTED after escalations`，**运行终止**）
- 没有任何幸存记录（树表全 `DEAD` 且无 `plan.md`）→ 写 `final_summary.md` 记录 `AUTO EXHAUSTED: no surviving route`，运行终止

## 长程脚手架（硬纪律）

1. **检查点纪律**：每个阶段开始前 `cat debug/.state` 核对 `phase_index` 与 `next`；结束后立即回写（`phase_index` +1、`spawn_count`、`last_verdict`、`next`）。auto-compact 或续跑后，你必须仅凭 `.state` + `auto_plan.md` 完整恢复"现在该做什么"——不得依赖记忆
2. **派活预算**：每次派发（含并行批次中的每一路）计入 `spawn_count`。派发批次前先核对：`spawn_count` + 本批派活数 ≤ {max_spawns}，超出则削减批次（优先保留靠前的专家/任务）；`spawn_count` 达 {max_spawns} → 跳过剩余阶段，强制收尾
3. **阶段数上限**：蓝图（含升级插入）长度始终 ≤ {max_phases}
4. **卡住检测**：同一任务派发两次（含重试）仍 `FAIL`/`BLOCKED`/产出缺失 → 跳过该任务并在 `.state` 注明；同一阶段内连续两个任务被跳过 → 按该阶段的失败路由处理（升级或阶段跳过）
5. **路由单点**：阶段间跳转只按本文件的协议执行；不得临时发明新阶段、新角色、新裁决词
6. **不读内容**：升级判断只依据 `.result` 行、`.state` 树表、裁决文件首行——任何"想了解更多"的冲动都派下一个 Agent 去做，而不是你自己读原文

## 职责划分（重要）

**所有物理内容都由各角色产出。Orchestrator 只做调度。样板任务文件一律写入 `{workspace}/tasks/`。**

| 文件 | 谁写 |
|------|------|
| `auto_plan.md`、`debug/.state`（含树表） | Orchestrator（纯调度元数据，零物理内容） |
| `tasks/task_assessor.md`、`task_plan.md`、`task_diverge_*.md`、`task_search_{n}_*.md`、`task_eval_{id}.md`、`task_debate_*.md`、`task_synthesize.md`、`task_verifier.md`、`task_gate_revise_{m}_*.md`、`task_gate_secretary_{m}.md`、`task_final_builder.md`、`task_final_evaluator.md`、`task_wrapup.md`（样板） | Orchestrator |
| `tasks/task_{id}.md`（验证任务：物理细节 + 验收判据 + 预测撞墙点） | **专家团成员** |
| `difficulty_assessment.md` | Assessor |
| `plan.md` | Planner |
| `theorist.md`、`computationalist.md`、`experimentalist.md` | 各专家 |
| `critic_round_{n}.md` | Critic |
| `debate_summary_round_{n}.md`、`final_plan.md` | Secretary |
| `verification_plan.md` | **Verifier** |
| `calculation_{id}.md`、`solution.md` | Builder |
| `verification_{id}.md`、`review.md` | Evaluator |

## 节点状态词汇（树表元数据）

| 状态 | 含义 |
|------|------|
| `ALIVE` | Evaluator 裁决 PASS，尚未展开 |
| `DEAD` | Evaluator 裁决 FAIL（验收判据不满足 = 死端），或被专家团放弃 |
| `EXPANDED` | 曾为 ALIVE，已生成子节点 |
| `BLOCKED` | Builder 无法执行（未验证，留给专家团处理） |

## Agent 配置

### Assessor（auto 专属）
- 基础版本：`agents/assessor.md`
- 只评估不求解：`difficulty_assessment.md` 首行 `DIFFICULTY: EASY|MEDIUM|HARD|FRONTIER`；HANDOFF 含 `DIFFICULTY`/`FORM`/`STEPS`/`RECOMMENDED` 行
- 超时 `{ephemeral_timeout}` 秒

### Planner（plan 阶段）
- 基础版本：`agents/planner.md`（"一种方法"纪律适用）
- 输出 `plan.md`；HANDOFF `STATUS: OK/FAIL`

### Theorist / Computationalist / Experimentalist（专家团）
- 基础版本：`agents/theorist.md`、`agents/computationalist.md`、`agents/experimentalist.md`
- **差分：** 四种议程——发散（审题 + 各提 ≥1 个结构不同方向 + 写完整任务书：验收判据逐条编码题面硬性要求 + 预测撞墙点）、深挖（后续任务/成熟判断）、打回（对问题清单逐条 ACCEPT/REBUT）、重入（升级触发 3 后读 review.md 的 FAIL 理由提本质不同新方向）；HANDOFF 含 `NEXT_TASKS` 行；**auto 不使用动议**，`MOTION` 行一律 NONE
- 超时 `{deep_timeout}` 秒

### Critic（debate 阶段）
- 基础版本：`agents/critic.md`
- **差分：** 批评三份专家分析 + 共识判定（`PLAN: READY | SEARCH`）；SUMMARY 含 Critical/Major 计数
- 超时 `{deep_timeout}` 秒

### Secretary
- 基础版本：`agents/secretary.md`
- **差分：** 三工作——辩论记录（`debate_summary_round_{n}.md`）、定稿（`synthesize`/`final_plan.md`）、打回修订（按 `verification_plan.md` 问题清单逐条修订）；也承担强制收尾（`task_wrapup.md`）
- 记录超时 `{ephemeral_timeout}` 秒；定稿与修订超时 `{deep_timeout}` 秒

### Verifier（gate 阶段）
- 基础版本：`agents/verifier.md`
- 输入：problem.md + final_plan.md；输出 `verification_plan.md`（首行 SOUND/REVISE）
- REVISE = 打回专家团，上限 {max_verify_rounds} 轮，耗尽即运行终止——**永不放行**

### Builder / Evaluator（临时模式，分支处理）
- 基础版本：`agents/builder.md` / `agents/evaluator.md`
- **差分：** Builder 只执行验证任务，结果写 `calculation_{id}.md`，**禁止写 `solution.md`**；Evaluator 输出 `verification_{id}.md`（首行 PASS/FAIL），逐条对照验收判据，失败时说明是否命中预测撞墙点
- 超时 `{ephemeral_timeout}` 秒

### Builder / Evaluator（最终模式）
- 使用基础版本（无差分）；最终审查裁决词表为 `PASS / REVISE / FAIL`

## 状态管理

`debug/.state` 示例（每完成一个阶段更新；树表为纯元数据）：

蓝图刚写成：

```
pipeline: auto
stage: phase:plan
difficulty: HARD
phases: plan>diverge>synthesize>gate>final
phase_index: 0
spawn_count: 1
escalations_used: 0
verify_round: 0
search_round: 0
debate_round: 0
last_verdict: -
next: phase plan (task_plan)
```

diverge 后（带树表）：

```
pipeline: auto
stage: phase:diverge
difficulty: HARD
phases: plan>diverge>synthesize>gate>final
phase_index: 1
spawn_count: 11
escalations_used: 0
last_verdict: PASS
tree:
  a1: parent=ROOT status=DEAD round=1
  b1: parent=ROOT status=ALIVE round=1
  c1: parent=ROOT status=EXPANDED round=1
next: branch handling done; phase synthesize (task_synthesize)
```

升级后（触发 3，final FAIL → 插入 diverge 重入）：

```
pipeline: auto
stage: phase:diverge
difficulty: FRONTIER
phases: diverge>debate>synthesize>final
phase_index: 0
spawn_count: 27
escalations_used: 1
reentry: 1
last_verdict: FAIL
tree:
  a1: parent=ROOT status=DEAD round=1
next: reentry diverge (task_diverge_* with reentry agenda)
```

- `phase_index`：当前执行到 `phases` 的第几个（0 起）
- `spawn_count`：累计派活数（含 Assessor 与一切重试），上限 {max_spawns}
- `escalations_used`：已用升级次数，上限 {max_escalations}
- `verify_round`/`search_round`/`debate_round`：各自阶段的内部轮次
- 进入修订争议协议时写 `dispute_round: <n>`

## 定位：何时选 auto

| 场景 | 推荐 |
|------|------|
| 不确定题目难度、不想手选流水线 | `auto` |
| 批量跑难度混杂的题集 | `auto` |
| 已知是难题/前沿题，想直接上最强结构 | `deep_search`（比 auto 的升级路径更省派活） |
| 已知方法明确的简单题 | `standard`（比 auto 少一次评估与蓝图开销） |

## 参数

- `timeout_seconds`: {timeout_seconds}
- `max_revisions`: {max_revisions}
- `max_phases`: {max_phases}（蓝图阶段数上限）
- `max_spawns`: {max_spawns}（全程派活总数上限，含重试）
- `max_escalations`: {max_escalations}（升级次数上限）
- `max_search_rounds`: {max_search_rounds}（search 阶段轮数上限）
- `max_debate_rounds`: {max_debate_rounds}（debate 阶段轮数上限）
- `max_verify_rounds`: {max_verify_rounds}（gate 打回轮数上限，耗尽即终止）
- `max_concurrent_agents`: {max_concurrent_agents}（同时在跑的分支/派活建议上限，见 config）
- `ephemeral_timeout`: {ephemeral_timeout}（Assessor、临时 Builder/Evaluator、辩论记录）
- `deep_timeout`: {deep_timeout}（专家发言、Critic、定稿与打回修订）
