# Pipeline 架构对比

系统提供 5 种 Pipeline 架构，通过 `config.json` 中的 `pipeline` 字段选择。

## 选择指南

| Pipeline | 适用场景 | 特点 | Token 消耗 | 实现状态 |
|----------|----------|------|-----------|----------|
| `standard` | 标准竞赛题，已知解法 | 线性流程，一次 REVISE 循环 | 低 | ✅ 已实现 |
| `parallel_paths` | 多解法并行探索 | 同时尝试 N 个方案，选最优 | 高 (×N) | 📝 设计中 |
| `iterative` | 开放性问题，需要实验 | Explorer 动态调整策略 | 中 | 📝 设计中 |
| `debate` | 跨领域问题 | 多专家辩论，综合意见 | 高 | 📝 设计中 |
| `tree_search` | 前沿研究，高度不确定 | 树状探索 + 回溯 | 可变 | 📝 设计中 |

## 配置示例

```json
{
  "pipeline": "tree_search",
  "model": "qwen3.6-plus",
  "timeout_seconds": 86400,
  "max_concurrent_problems": 3
}
```

## 共享基础设施

所有 Pipeline 共享：
- Git 版本控制（自动提交）
- 权限控制（AGENT_PROFILES）
- 断点续传（.state 文件）
- 流式日志（stream-json）
- 知识库查询（RAG）

## 文档结构

- [Standard Pipeline](standard.md) — 现有架构总结
- [Parallel Paths](parallel_paths.md) — 多路径并行
- [Iterative Exploration](iterative.md) — 迭代探索
- [Debate & Collaboration](debate.md) — 辩论协作
- [Tree Search](tree_search.md) — 树状搜索

## Pipeline 选择决策树

```
问题类型？
├── 标准竞赛题（有明确解法）
│   └── → standard
│
├── 有多种可能解法，想比较
│   └── → parallel_paths
│
├── 开放性问题，需要实验验证
│   └── → iterative
│
├── 跨领域，需要多角度分析
│   └── → debate
│
└── 前沿研究，答案未知，需要探索
    └── → tree_search
```

## 未来扩展

可以添加更多 Pipeline（如 `hybrid`、`simulation_driven`），只需：
1. 在 `prompts/pipelines/<name>/` 下创建 prompt 文件
2. 在 `run.py` 中注册新 Pipeline
3. 更新本文档
