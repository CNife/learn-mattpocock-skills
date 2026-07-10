# 翻译术语锚点表

本表供 `bilingual-html` worker 翻译时统一译法使用。覆盖跨技能重复出现、且译法可能分歧的核心术语；v1.1.0 起新增 to-spec/to-tickets/wayfinder 规划与寻路术语（见第八节）。

**使用规则**：
- 左栏英文术语出现时，右栏中文译法为强制标准，不得自行改写。
- 标注「保留英文」的术语，翻译时不译，原样保留。
- 本表未收录的术语，按上下文自然翻译，保持技能内部自洽。
- 图谱（index.html）已有的中文标签为最高优先级锚点，必须沿用。

## 一、流程动词 / 技能动作

| 英文 | 中文译法 | 备注 |
|---|---|---|
| grilling | 保留英文 | 技能名，不译 |
| grill | 保留英文 | 技能触发词，不译 |
| triage | 分诊 | 图谱标签锚点 |
| diagnose | 诊断 | |
| debug | 调试 | |
| implement | 实现 | 图谱标签锚点 |
| review | 审查 | code-review 场景下 |
| refactor | 重构 | |
| mock | 模拟 | 动词/名词均译「模拟」 |
| stub | 桩 | |
| spy | 间谍 | 测试替身语境 |
| bisect | 二分 | git bisect 场景 |
| stress-test | 压力测试 | |
| synthesise / synthesize | 综合 | to-spec 场景 |
| grill (someone) | 追问 | 作动词「拷问/追问」时 |

## 二、artifact / 产物类型

| 英文 | 中文译法 | 备注 |
|---|---|---|
| PRD | 保留英文 | Product Requirements Document，不译 |
| ADR | 保留英文 | Architecture Decision Record，不译 |
| CONTEXT.md | 保留英文 | 文件名，不译 |
| agent brief | 代理简报 | triage 产物 |
| issue | issue | 图谱标签「拆分为 Issue」；首字母小写时保留英文，不译为「议题/工单」 |
| Issue | Issue | 首字母大写时保留英文，遵源仓库 CONTEXT.md |
| Issue tracker | Issue 跟踪器 | 遵源仓库 CONTEXT.md，_Avoid_: backlog manager |
| PR | 保留英文 | Pull Request，不译 |
| spec | 规格说明 | to-spec 贯穿术语；PRD 仍保留英文 |
| regression test | 回归测试 | |
| acceptance criteria | 验收标准 | |
| user story | 用户故事 | |
| snapshot | 快照 | 测试语境 |
| fixture | 固定装置 | 测试输入数据 |
| seam | 接缝 | codebase-design 核心术语，_Avoid_: boundary |
| tracer bullet | 曳光弹 | to-tickets / tdd 术语 |

## 三、codebase-design 架构词汇（强制统一，禁止替换）

| 英文 | 中文译法 | 备注 |
|---|---|---|
| module | 模块 | _Avoid_: unit, component, service |
| interface | 接口 | _Avoid_: API, signature（此处含类型+不变量+约束） |
| implementation | 实现 | |
| depth | 深度 | |
| deep (module) | 深模块 | |
| shallow (module) | 浅模块 | |
| adapter | 适配器 | |
| leverage | 杠杆收益 | 调用方从深度获得的收益 |
| locality | 局部性 | 维护方从深度获得的收益 |
| port | 端口 | ports & adapters 模式 |
| dependency injection | 依赖注入 | |

## 四、triage 状态角色（遵源仓库 + setup-matt-pocock-skills）

| 英文 | 中文译法 | 备注 |
|---|---|---|
| needs-triage | needs-triage | 状态标签，保留英文 |
| needs-info | needs-info | 状态标签，保留英文 |
| ready-for-agent | ready-for-agent | 状态标签，保留英文 |
| ready-for-human | ready-for-human | 状态标签，保留英文 |
| ready-for-afk | ready-for-afk | 状态标签，保留英文 |
| wontfix | wontfix | 状态标签，保留英文 |
| Triage role | 分诊角色 | 遵源仓库 CONTEXT.md |

## 五、测试 / TDD 术语

| 英文 | 中文译法 | 备注 |
|---|---|---|
| red → green | 红 → 绿 | TDD 循环 |
| red-green-refactor | 红-绿-重构 | |
| vertical slice | 垂直切片 | _Avoid_: horizontal slice |
| horizontal slice | 水平切片 | |
| prefactor | 预重构 | 「先让改动变容易，再做容易的改动」 |
| tautological (test) | 同义反复（测试） | 断言重算实现逻辑 |
| implementation-coupled | 耦合实现细节 | |
| test double | 测试替身 | |

## 六、code-review 双轴术语

| 英文 | 中文译法 | 备注 |
|---|---|---|
| Standards (axis) | 规范（轴） | |
| Spec (axis) | 规格（轴） | |
| smell (code smell) | 坏味道 | Fowler 代码坏味道 |
| smell baseline | 坏味道基线 | |
| merge-base | 合并基点 | git 三点 diff |
| scope creep | 范围蔓延 | |

## 七、Matt 生态专有词 / 通用角色

| 英文 | 中文译法 | 备注 |
|---|---|---|
| agent | 代理 | AFK agent = 离线代理 |
| AFK | 保留英文 | Away From Keyboard，不译 |
| maintainer | 维护者 | |
| reporter | 报告人 | issue 提交者 |
| collaborator | 协作者 | |
| sub-agent | 子代理 | |
| out-of-scope | 超出范围 | 既指状态也指目录 |
| gold-plating | 镀金 | 过度装饰 |
| throwaway (prototype/harness) | 一次性（原型/测试架） | |
| throwaway branch | 一次性分支 | prototype 收尾：原型留在一次性分支（离开 main），main 只保留已验证决策 |
| primary source | 一手来源 | prototype 收尾：结论与验证过的原型作为一手来源，写入 issue/commit |
| feedback loop | 反馈循环 | diagnosing-bugs 核心 |
| hitl / HITL | 保留英文 | Human-In-The-Loop，不译 |

## 八、v1.1.0 规划 / wayfinder 术语

| 英文 | 中文译法 | 备注 |
|---|---|---|
| to-spec | 保留英文 | 技能名/命令，不译 |
| to-tickets | 保留英文 | 技能名/命令，不译 |
| wayfinder | 保留英文 | 技能名/命令，不译 |
| wayfinding | 寻路 | wayfinder 的活动/过程 |
| ticket | 保留英文 | 上游 CONTEXT.md 将 ticket 标为 _Avoid_（域术语用 Issue），但 to-tickets/wayfinder 技能原文以 ticket 为工作术语；翻译时保留英文以匹配原文，不译「工单/议题」 |
| map | 地图 | wayfinder:map issue；_Avoid_: 技能图谱（站点 index.html 专属，见 CONTEXT.md） |
| destination | 目的地 | wayfinder 锚定词 |
| frontier | 前沿 | 开放、未阻塞、未认领的 ticket--已知边缘 |
| fog of war | 战争迷雾 | |
| fog | 迷雾 | |
| route | 路线 | |
| Not yet specified | 尚未明确 | 地图章节名；范围内尚未可成 ticket 的迷雾 |
| Decisions so far | 已作决策 | 地图章节名 |
| Out of scope | 超出范围 | 地图章节名；同 out-of-scope（第七节） |
| claim | 认领 | 认领 ticket（通过指派） |
| child issue | 子 issue | issue 保留英文 |
| parent issue | 父 issue | |
| blocking edge | 阻塞边 | to-tickets/wayfinder 术语 |
| Blocked by | 阻塞于 | ticket 模板章节名 |
| unblocked | 未阻塞 | |
| resolution comment | 结论评论 | 关闭 ticket 时发布的答案 |
| graduate | 转化 | 迷雾/尚未明确转化为 ticket；不译「毕业」（毕业保留给技能桶晋升） |
| task | 任务 | wayfinder 票型之一；标签 `wayfinder:task` 保留英文 |
| wide refactor | 大范围重构 | to-tickets 例外切片 |
| blast radius | 影响半径 | |
| expand–contract | 扩展-收缩 | 大范围重构序列 |
| call site | 调用点 | |
| integration branch | 集成分支 | |
