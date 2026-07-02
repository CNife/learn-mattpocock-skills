---
name: bilingual-html
description: 将 SKILL.md 转为中英对照的 HTML 参考页面，使用 Kami 设计风格。触发词：排版技能 / 生成 HTML 对照 / 做成可读页面 / turn skill into readable HTML.
disable-model-invocation: true
---

# Bilingual HTML

把一篇技能文档做成适合阅读的双栏 HTML：左栏英文原文，右栏中文翻译，段落级对齐，Kami 暖羊皮纸风格。

## 流程

### 1. 读源文件

读入待转换的 `SKILL.md`，完整读取。提取 frontmatter **所有字段**，保留原始值，不做解释或转化。

字段按以下顺序和规则排列到表格：

| 字段 | 规则 |
|---|---|
| `name` | 原文直出 |
| `description` | 原文直出 |
| — | 紧随其后加一行「触发词」列，值为 description 的中文翻译 |
| `argument-hint` | 如有则原文直出 |
| — | 紧随其后加一行「参数提示」列，值为 argument-hint 的中文翻译 |
| `disable-model-invocation` | 如有则直接输出原始值（`true` / `false`），不做任何解释 |
| 其他未知字段 | 原文直出，不翻译 |

**完成标志**：frontmatter 全部字段已提取，全文已读入。

### 2. 分段落

按 Markdown 段落拆分原文。段落定义为：**至少两个换行符隔开的文本块**（一个 `<p>`、一个 `<h3>`、或一个 `<ul>`/`<ol>` 各自为一个段落）。

每一段译成中文，保留原文的所有格式标记（`<strong>`、`<code>`、`<a>`、`<em>`）。

**完成标志**：每段原文对应一段译文，格式标记完整保留。

### 3. 拼 HTML

按以下模板生成独立 HTML 文件。文件放在 `./<skill-name>/` 下，一个 `.md` 对应一个 `.html`。

#### 3.1 结构骨架

```
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} · skill router</title>
  <!-- CDN 字体加载 -->
  <style>
    /* .back-link 导航 */
    /* @font-face + 全部样式 */
  </style>
<body>
  <div class="container">
    <!-- .back-link 导航 ← index.html 和同技能文件链接 -->
    <!-- frontmatter 表格 -->
    <!-- h1 + subtitle -->
    <!-- 逐段落 pair -->
  </div>
</body>
</html>
```

#### 3.2 Font 加载

使用两条 CDN 来源，禁止使用本地/系统字体：

```css
@font-face {
  font-family: "TsangerJinKai02";
  src: url("https://cdn.jsdelivr.net/gh/tw93/Kami@main/assets/fonts/TsangerJinKai02-W04.ttf") format("truetype");
  font-weight: 400;
}
@font-face {
  font-family: "TsangerJinKai02";
  src: url("https://cdn.jsdelivr.net/gh/tw93/Kami@main/assets/fonts/TsangerJinKai02-W05.ttf") format("truetype");
  font-weight: 500;
}
```

Google Fonts 预连接 + 加载 Source Serif 4：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap" rel="stylesheet">
```

Font stack（serif 一文一中的搭配）：

```css
--serif: "Source Serif 4", "TsangerJinKai02", "Noto Serif SC", "Source Han Serif SC", serif;
```

#### 3.3 CSS 变量

```css
:root {
  --parchment: #f5f4ed;
  --ink-blue: #1B365D;
  --text: #2c2418;
  --text-soft: #5a4f40;
  --warm-gray: #e1ddcf;
  --warm-mid: #cdc6b4;
}
```

Typography 基础：

```css
body {
  background: var(--parchment);
  color: var(--text);
  font-family: var(--serif);
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

全局导航样式：

```css
.back-link {
  display: inline-block;
  margin-bottom: 1rem;
  font-size: 0.85rem;
}
```

#### 3.4 Frontmatter 表格

frontmatter 放在页面最顶部，用 `<table>` 展示，墨蓝左边框。所有字段按原始值输出，不做解释：

```html
<table class="fm-table">
  <tr><td>name</td><td>{name}</td></tr>
  <tr><td>description</td><td>{description}</td></tr>
  <tr><td>触发词</td><td>{description 的中文翻译}</td></tr>
  <!-- 以下两行仅在 frontmatter 含 argument-hint 时出现 -->
  <tr><td>argument-hint</td><td>{argument-hint 原文}</td></tr>
  <tr><td>参数提示</td><td>{argument-hint 的中文翻译}</td></tr>
  <tr><td>disable-model-invocation</td><td>{原始值，如 true}</td></tr>
</table>
```

注意：
- 不要在表格中对任何字段值做额外解释（如 `true` → `user-invoked only`）
- frontmatter 中不存在的字段不要出现在表格中
- 对于未知/非标准的 frontmatter 字段，原文直出，不翻译

```css
.fm-table {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0 0;
  font-size: 0.8rem;
  background: #ece9e0;
  border-left: 3px solid var(--ink-blue);
}
.fm-table td {
  padding: 0.3rem 0.6rem;
  vertical-align: top;
  color: var(--text-soft);
}
.fm-table td:first-child {
  font-weight: 600;
  color: var(--ink-blue);
  white-space: nowrap;
  width: 1%;
  padding-right: 1.2rem;
}
```

#### 3.5 段落级双栏对齐

每个段落独立成 `.pair`，内含 `.col-en`（英文）和 `.col-zh`（中文）：

```html
<div class="pair">
  <div class="col-en" lang="en"><p>原文段落...</p></div>
  <div class="col-zh" lang="zh-CN"><p>译文段落...</p></div>
</div>
```

```css
.pair {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  margin: 0.45rem 0;
}
.col-en {
  padding-right: 1.8rem;
  border-right: 1px solid var(--warm-gray);
}
.col-zh {
  padding-left: 1.8rem;
  line-height: 1.85;
}
```

#### 3.6 响应式

≤800px 时堆叠为单栏：

```css
@media (max-width: 800px) {
  .pair { grid-template-columns: 1fr; }
  .col-en {
    border-right: none;
    border-bottom: 1px solid var(--warm-gray);
    padding: 0.3rem 0;
    margin-bottom: 0.3rem;
  }
  .col-zh { padding: 0.3rem 0; }
}
```

#### 3.7 禁止事项

- 不要调整原文的内容结构（不要合并/拆分段落、不要改写句式）
- 不要添加自己的创意装饰（无阴影、无渐变、无圆角卡片、无固定/粘性定位）
- 不要使用本地/系统字体回退
- 不要使用 `Inter`、`system-ui` 等无衬线字体作为正文字体
- 中文行高 ≥ 1.8

#### 3.8 导航链接

生成 HTML 后必须添加导航链接，规则如下：

**主文档（`SKILL.html`）：**
- 在 `<div class="container">` 之后、frontmatter 表格之前插入 `.back-link` 导航行
- 首个链接为 `← <a href="../index.html">技能图谱</a>`
- 如果该技能有附属 `.md` 文件生成了独立 HTML（如 `LOGIC.html`、`ADR-FORMAT.html`），在 index 链接后追加 ` · <a href="...">标签</a>`，每个附属文件对应一个链接

**附属文档（如 `LOGIC.html`、`ADR-FORMAT.html`）：**
- 在 `<div class="container">` 之后插入 `.back-link` 导航行
- 首个链接为 `← <a href="SKILL.html">技能名</a>`（返回主文档）
- 追加 ` · <a href="../index.html">技能图谱</a>`

**单文件技能（无附属文档）：**
- 只加 `← <a href="../index.html">技能图谱</a>`

所有导航链接使用 `.back-link` 样式（display: inline-block、margin-bottom: 1rem、font-size: 0.85rem）。

### 4. 验证

- 用浏览器打开生成的 HTML，检查双栏在段落级是否对齐
- 缩小到 375px 宽度，检查移动端堆叠效果
- 确认 frontmatter 表格在最顶部
- 确认字体已从 CDN 正确加载（无 fallback 到系统字体）

**完成标志**：四项验证全部通过。

## 参考

### Kami 设计语言

| Token | 值 | 用途 |
|---|---|---|
| `--parchment` | `#f5f4ed` | 页面背景，暖羊皮纸色 |
| `--ink-blue` | `#1B365D` | 强调色：h1、h2、strong、链接、frontmatter 标签 |
| `--text` | `#2c2418` | 正文，暖深棕 |
| `--text-soft` | `#5a4f40` | 辅助文字 |
| `--warm-gray` | `#e1ddcf` | 分栏分隔线 |
| `--warm-mid` | `#cdc6b4` | h2 下边框 |

### 文件命名

- 源文件 `skills/<category>/<skill>/SKILL.md` → 输出 `./<skill>/SKILL.html`
- 例：`skills/engineering/ask-matt/SKILL.md` → `./ask-matt/SKILL.html`
- 文件名与源文件对应，便于对照阅读
