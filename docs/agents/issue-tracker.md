# Issue 跟踪器：GitHub

本 repo 的 issue 和 PRD 以 GitHub issues 形式管理。所有操作使用 `gh` CLI。

## 约定

- **创建 issue**：`gh issue create --title "..." --body "..."`。多行 body 用 heredoc。
- **读取 issue**：`gh issue view <number> --comments`，用 `jq` 过滤评论并获取标签。
- **列出 issue**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，按需加 `--label` 和 `--state` 过滤。
- **评论 issue**：`gh issue comment <number> --body "..."`
- **添加/移除标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**：`gh issue close <number> --comment "..."`

从 `git remote -v` 推断 repo--`gh` 在 clone 内运行时自动识别。

## PR 作为分诊面

**PR 作为请求面：是。** 外部 PR 与 issue 跑相同的标签和状态，使用 `gh pr` 等价命令：

- **读取 PR**：`gh pr view <number> --comments` 和 `gh pr diff <number>` 看 diff。
- **列出待分诊的外部 PR**：`gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`，只保留 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的（丢弃 `OWNER`/`MEMBER`/`COLLABORATOR`）。
- **评论/打标签/关闭**：`gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`。

GitHub 的 issue 和 PR 共享同一编号空间，裸 `#42` 可能是任一--用 `gh pr view 42` 解析，回退到 `gh issue view 42`。

## 当技能说「发布到 issue 跟踪器」

创建一个 GitHub issue。

## 当技能说「获取相关 ticket」

运行 `gh issue view <number> --comments`。

## Wayfinding 操作

供 `/wayfinder` 使用。**map** 是单个 issue，其 **child** issue 作为 ticket。

- **Map**：单个标记 `wayfinder:map` 的 issue，承载 Notes / Decisions-so-far / Fog body。`gh issue create --label wayfinder:map`。
- **Child ticket**：作为 GitHub sub-issue 链接到 map（`gh api` 调 sub-issues 端点）。sub-issues 不可用时，把 child 加到 map body 的 task list，并在 child body 顶部写 `Part of #<map>`。标签：`wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）。认领后 ticket 指派给驱动的 dev。
- **Blocking**：GitHub **原生 issue 依赖**--UI 可见的规范表示。用 `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>` 添加边，其中 `<blocker-db-id>` 是 blocker 的数字 **database id**（`gh api repos/<owner>/<repo>/issues/<n> --jq .id`，_不是_ `#number` 或 `node_id`）。GitHub 报告 `issue_dependencies_summary.blocked_by`（仅 open blocker--实时门）。依赖不可用时，回退到 child body 顶部 `Blocked by: #<n>, #<n>`。ticket 在所有 blocker 关闭后解锁。
- **Frontier 查询**：列出 map 的 open child（`gh issue list --state open`，限定 map 的 sub-issues / task list），丢弃有 open blocker（`issue_dependencies_summary.blocked_by > 0`，或 `Blocked by` 行有 open issue）或已指派的；map 顺序首个胜出。
- **认领**：`gh issue edit <n> --add-assignee @me`--session 的首次写入。
- **解决**：`gh issue comment <n> --body "<answer>"`，然后 `gh issue close <n>`，再向 map 的 Decisions-so-far 追加上下文指针（gist + link）。
