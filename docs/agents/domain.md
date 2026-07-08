# 领域文档

工程技能在探索代码库时如何消费本 repo 的领域文档。

## 探索前先读

- repo root 的 **`CONTEXT.md`**，或
- 若存在 repo root 的 **`CONTEXT-MAP.md`**--它指向每个 context 一个 `CONTEXT.md`。读与主题相关的每个。
- **`docs/adr/`**--读涉及你即将工作区域的 ADR。Multi-context repo 还需检查 `src/<context>/docs/adr/` 的 context 范围决策。

若这些文件不存在，**静默继续**。不要标记其缺失；不要预先建议创建。`/domain-modeling` 技能（经 `/grill-with-docs` 和 `/improve-codebase-architecture` 到达）会在术语或决策真正需要解决时懒创建它们。

## 文件结构

Single-context repo（多数 repo）：

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Multi-context repo（repo root 有 `CONTEXT-MAP.md`）：

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← 系统级决策
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context 特定决策
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## 使用 glossary 的词汇

当你的输出命名领域概念（issue 标题、重构提案、假设、测试名），使用 `CONTEXT.md` 中定义的术语。不要漂移到 glossary 明确避免的同义词。

若你需要的概念尚不在 glossary，那是个信号--要么你在发明项目不用的语言（重新考虑），要么有真实缺口（记下给 `/domain-modeling`）。

## 标记 ADR 冲突

若你的输出与现有 ADR 矛盾，显式提出而非静默覆盖：

> _与 ADR-0007（event-sourced orders）矛盾--但值得重开，因为…_
