# Tree Search Architecture

## 流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator                              │
│  (读取 problem.md, 解析决策, 调用 Agent, 管理树状态)        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  初始化          │
                  │  - 创建 tree_state.json
                  │  - 创建 decision_log.md
                  └──────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │  主循环开始             │
              │  iteration < max?       │
              └─────────────────────────┘
                       │
            ┌──────────┴──────────┐
            │                     │
           Yes                    No
            │                     │
            ▼                     ▼
  ┌──────────────────┐    ┌──────────────┐
  │  Strategist      │    │  强制 terminate
  │  (决策)          │    │  选择最优节点
  │  → decision.json │    └──────────────┘
  └──────────────────┘
            │
            ▼
  ┌──────────────────┐
  │  解析决策        │
  │  action = ?      │
  └──────────────────┘
            │
    ┌───────┴───────┬──────────────┬──────────────┬──────────────┐
    │               │              │              │              │
    ▼               ▼              ▼              ▼              ▼
  expand         validate        build        backtrack      terminate
    │               │              │              │              │
    ▼               ▼              ▼              ▼              │
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│生成新节点 │  │Validator │  │ Builder  │  │更新路径   │         │
│更新树     │  │快速验证   │  │完整计算   │  │回溯到父节点│         │
└──────────┘  └──────────┘  └──────────┘  └──────────┘         │
    │               │              │              │              │
    └───────────────┴──────────────┴──────────────┘              │
                            │                                    │
                            ▼                                    │
                  ┌──────────────────┐                           │
                  │  更新树状态      │                           │
                  │  更新决策日志    │                           │
                  │  iteration++     │                           │
                  └──────────────────┘                           │
                            │                                    │
                            └────────────────────────────────────┘
                                         │
                                         ▼
                               ┌──────────────────┐
                               │  总结阶段        │
                               │  - 选择成功节点  │
                               │  - Evaluator 审查│
                               │  - final_summary │
                               └──────────────────┘
```

## 状态转换

```
tree_search_init
tree_search_iteration_1
tree_search_iteration_2
...
tree_search_iteration_N
tree_search_evaluator
tree_search_builder_revise_1
tree_search_evaluator_revise_1
tree_search_done
```

## 文件流

**输入：**
- `problem.md` — 物理题目

**状态文件：**
- `tree_state.json` — 探索树状态（JSON）
- `decision_log.md` — 决策日志

**每次迭代文件：**
- `decision.json` — Strategist 的决策
- `validation_{node_id}.md` — Validator 的验证结果
- `solution_{node_id}.md` — Builder 的计算结果

**输出：**
- `solution.md` — 最终求解（从成功的节点复制）
- `review.md` — Evaluator 的审查结果
- `final_summary.md` — 最终总结报告

## 探索树结构

```
root
├── A (能量密度积分)
│   ├── A1 (轴线电场积分)
│   │   └── status: DEAD_END
│   └── A2 (离轴电场展开)
│       └── status: UNCERTAIN
├── B (直接面积分 + 椭圆积分)
│   ├── B1 (标准椭圆积分)
│   │   └── status: SUCCESS ✓
│   └── B2 (级数展开近似)
│       └── status: PENDING
└── C (叠加原理：同心圆环)
    └── status: PENDING
```

## 节点状态

- `pending` — 未探索
- `validating` — 正在验证
- `building` — 正在计算
- `success` — 成功
- `failed` — 失败
- `dead_end` — 死胡同

## Strategist 决策类型

### expand
生成新的子节点（新策略）

### validate
快速验证策略可行性
- 输出：PROMISING / DEAD_END / UNCERTAIN

### build
完整计算策略
- 输出：solution_{node_id}.md

### backtrack
回溯到父节点或祖先节点

### terminate
结束搜索

## 关键特性

1. **智能搜索**：Strategist 根据验证结果决定探索方向
2. **快速验证**：Validator 快速筛选，避免浪费时间
3. **回溯机制**：失败时可以回溯，不浪费已探索的路径
4. **并行探索**：可以同时展开多个分支（通过多次 expand）

## 适用场景

- 问题有多种可能的解法，需要探索
- 不确定哪种方法最有效
- 需要从失败中学习并调整策略
- 问题复杂，需要逐步逼近

## 搜索策略

### 启发式排序

Strategist 按以下优先级选择行动：

1. **如果有成功的节点** → terminate
2. **如果当前节点无子节点** → expand
3. **如果当前节点未验证** → validate
4. **如果验证结果为 PROMISING** → build
5. **如果验证结果为 DEAD_END** → backtrack
6. **如果验证结果为 UNCERTAIN** → 选择 backtrack 或 build

### 探索顺序

**早期（迭代 1-5）：** 广度优先
- 展开多个分支
- 快速验证每个分支

**中期（迭代 6-15）：** 深度优先
- 深入 PROMISING 的分支
- 完整计算有希望的策略

**后期（迭代 16+）：** 收敛
- 选择最优分支
- 终止搜索

## 终止条件

1. **成功终止**：找到 status = "success" 的节点
2. **迭代上限**：达到 max_iterations（默认 20）
3. **所有分支失败**：所有节点 status = "dead_end" 或 "failed"
4. **Strategist 主动 terminate**：Strategist 判断已经找到足够好的方案

## 与 Standard Pipeline 的关系

Tree Search 找到成功方案后，进入标准流程：
1. 将成功的 solution_{node_id}.md 复制为 solution.md
2. 启动 Evaluator 审查
3. 如果 REVISE，启动 Builder 修正
4. 生成 final_summary.md

## 优势与劣势

### 优势
- **探索能力强**：可以探索多个方向
- **失败容忍**：失败可以回溯，不浪费资源
- **智能决策**：Strategist 根据验证结果调整策略

### 劣势
- **Token 消耗高**：需要多次调用 Strategist 和 Validator
- **状态管理复杂**：需要维护探索树和决策日志
- **Strategist 质量关键**：如果 Strategist 决策差，搜索效率低
