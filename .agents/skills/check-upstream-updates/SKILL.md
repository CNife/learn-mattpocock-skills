---
name: check-upstream-updates
description: 检查 mattpocock/skills 上游更新，找出需要重译的技能与新增可翻译技能。
disable-model-invocation: true
---

# Check Upstream Updates

对比 `mattpocock-skills` submodule 锁定的上游版本与每个已翻译技能的翻译基准，找出哪些技能需要重译、哪些新技能可翻译。脚本只读，推进 submodule 指针与更新清单都需人工确认。

## 背景：两个版本锚

这个技能依赖两个**版本锚**的区分：

- **submodule 指针**：父仓库记录的 `mattpocock-skills` 检出 commit。代表"上游代码的物理副本当前停在哪个版本"。AI 翻译时读的就是这个副本。
- **清单 `source_commit`**：`docs/translated-skills.json` 里每个技能记录的 commit。代表"这个技能的 HTML **实际翻译时**所基于的上游版本"。

两者不同步是常态：推进 submodule 指针拿到最新代码后，清单 `source_commit` 仍指向旧版本，直到该技能被重译。

### 为何用 submodule + per-skill 清单

- **submodule** 提供上游代码的可读副本，且父仓库记录确切 commit，版本确定。
- **per-skill 清单**提供每个技能独立的翻译基准，使检查粒度细化到单个技能——上游改了 10 个技能，只关心已翻译的那 3 个。若只用 submodule 单一指针，要么漏报（不细化），要么误报（整体推进就标记全部需重译）。
- 代价是维护一份清单。

### 为何钉 `main` HEAD 而非 release tag

上游用 changesets 发版，但发版不频繁——`v1.0.1` 之后 `main` 已合并十几个 wayfinder 系列 PR（含 grilling 确认门）未发版。钉 tag 会长期落后于已合并的改进。这是学习/翻译站，及时性优先；每次推进显式确认，可回退。

### 为何不自动重新生成 HTML

翻译是创造性工作，自动生成会产出未校对的中文，污染站点。本技能的边界止于"报告 + 经确认推进指针"，重新生成 HTML 是 `bilingual-html` 技能 + 人工翻译的职责。

## 流程

### 1. 跑检查脚本

```bash
uv run --script scripts/check-updates.py           # 人类可读
uv run --script scripts/check-updates.py --json    # 机器可读（给下游处理）
uv run --script scripts/check-updates.py --ref origin/v1.0.1  # 对比特定 ref
```

脚本只做计算：`fetch origin` → 取 `origin/main` HEAD → 对每个已翻译技能对比 `source_commit..origin/main` 该技能当前上游目录 → 报告变更文件 + commit range；另扫描 `engineering` + `productivity` 桶找出清单里没有的新技能。

**完成标志**：脚本退出码 0 或 2，报告已完整输出到 stdout（退出码 2 表示有 `source_commit` 不在上游历史，见步骤 2 的 Unknown baseline）。

### 2. 解读输出

- **Changed skills**：上游该技能目录在 `source_commit..origin/main` 之间有文件变化 → 需要重新翻译并重新生成 HTML。
  - 列出的变更文件（`M`/`A`/`D` 前缀）指明上游改了什么，重译时重点对照。
- **Unchanged**：该技能无变化，跳过。
- **Moved skills**：上游把该技能换了桶（清单 `source_path` 与当前不符）。即使内容未变也需刷新清单的 `source_path`，并视情况重译。
- **Missing upstream**：技能在清单里但上游已删除（目录不存在）。罕见，需人工判断是否移除翻译。
- **Unknown baseline**：`source_commit` 不在上游 git 历史中（可能被 force-push 抹掉）。脚本对此退出码 2。需人工重新校准该技能的 `source_commit`。
- **New translatable skills**：`engineering`/`productivity` 桶里有清单未收录的新技能 → 可选择翻译。
- **首次运行全部 Unchanged**：清单初始化时 `source_commit` 统一填 `main` HEAD，故首次检查无差异。这是已知行为——若怀疑 HTML 实际基于更早版本，可手动校准该技能的 `source_commit` 到更早的 commit 后重跑。

**完成标志**：每个 Changed/Moved 技能已明确是否重译，每个 Missing 已明确处置，每个 Unknown-baseline 已明确如何重新校准，每个 New 技能已明确是否翻译。

### 3. 经确认推进 submodule 指针

若决定跟进上游更新，**先征得用户明确确认**，再推进：

```bash
git -C mattpocock-skills fetch origin
git -C mattpocock-skills checkout main
git -C mattpocock-skills merge --ff-only origin/main
git add mattpocock-skills          # 父仓库记录新指针
```

推进后 submodule 副本停在最新 `main` HEAD，AI 可读最新 `SKILL.md` 做翻译。但清单 `source_commit` 此刻尚未更新（更新规则见参考）。

**完成标志**：`git submodule status` 显示新 commit，父仓库 `git diff --cached` 含 `mattpocock-skills` 指针变更。

### 4. 重译后更新清单

重新翻译某技能并用 `bilingual-html` 重新生成 HTML 后，更新 `docs/translated-skills.json` 里**仅该技能**的条目：

```json
"<skill-name>": {
  "source_commit": "<当前 submodule HEAD，git -C mattpocock-skills rev-parse HEAD>",
  "translated_at": "<今天日期 YYYY-MM-DD>",
  "source_path": "<skills/<bucket>/<name>，若上游改了桶则刷新>"
}
```

- `source_commit` = 当前 submodule HEAD。
- `translated_at` = 重译日期。
- `source_path` 是**派生元数据**，脚本会验证；若上游把技能换了桶，此处同步刷新。

**完成标志**：清单里被重译技能的三字段已更新，其它技能条目不动。

## 参考

### 脚本接口

`scripts/check-updates.py`（PEP723，`uv run --script` 运行，仅依赖 stdlib）：

| 参数 | 作用 |
|---|---|
| （无） | 人类可读报告输出到 stdout，进度信息到 stderr |
| `--json` | 输出结构化 JSON |
| `--ref <ref>` | 对比指定 ref（默认 `origin/<manifest ref>`，通常 `origin/main`） |

退出码：0 = 干净；1 = submodule 或 manifest 缺失（环境错误）；2 = 有 `source_commit` 不在上游历史（数据错误，报告仍完整输出）。

### 清单结构 `docs/translated-skills.json`

```json
{
  "upstream": {"url": "https://github.com/mattpocock/skills.git", "ref": "main"},
  "skills": {
    "<name>": {
      "source_commit": "<40 字符 commit hash>",
      "translated_at": "YYYY-MM-DD",
      "source_path": "skills/<bucket>/<name>"
    }
  }
}
```

- `source_commit`：该技能 HTML 实际翻译时所基于的上游 commit。**唯一更新时机**：重新翻译并重新生成 HTML 后，设为当前 submodule HEAD（见步骤 4）。推进 submodule 指针不更新它。
- `source_path`：派生字段，脚本搜索 `mattpocock-skills/skills/*/<name>` 验证；非真值源。上游换桶时脚本标记 Moved。

### 关注范围

新增可翻译技能只扫描 `engineering` + `productivity` 两个桶（已翻译范围的桶）。`in-progress`（wayfinder 等）、`misc`、`personal`、`deprecated` 不主动报告——技能进入 `engineering`/`productivity` 后自然被检测到。

### 外部 clone 清理

本项目曾用 `/home/cnife/github/mattpocock-skills` 作为独立 clone，改用 submodule 后已冗余。确认无其他项目引用后可删除：

```bash
rm -rf /home/cnife/github/mattpocock-skills
```
