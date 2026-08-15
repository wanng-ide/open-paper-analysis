# 输出后端

[English](../en/outputs.md) | [简体中文](../zh-CN/outputs.md)

## 一份主稿

Agent 只做一次研究判断。Canonical metadata、来源、章节 `0-8`、证据
锚点、公式、表格、局限和研究判断共同形成一份语义主稿。后端渲染只改变
平台结构与媒体传输方式。

所有目标必须保持相同的论文身份、章节含义、指标、实验设置、不确定性、
Figure/Table 编号，以及“论文报告”与“个人判断”的边界。

## Markdown

Markdown 是默认输出，也是通用保底：

- YAML 元数据记录正式单位，而不是以作者列表代替。
- 同时存在正式版本和预印本时，分别记录正式发表与首次公开日期。
- `contributions` 使用 1-4 个短标签，中文标签通常不超过 4 个汉字，
  空格分词语言不超过 4 个词；完整贡献及证据留在正文中说明。
- 显示论文标题和可点击目录。
- `Sources` 之后依次为 `0-8`。
- 使用标准公式、表格、链接和稳定相对图片路径。
- 不混入 Notion 标签或飞书 XML。

[Canonical Markdown 示例](../../examples/deepseekmoe/markdown.md) |
[完整案例说明](../../examples/deepseekmoe/README.md)

## Notion

Notion 使用官方 enhanced Markdown，并通过结构化调用写入属性：

1. 数据库属性按照实时 schema 映射 canonical metadata，并与 Markdown
   使用相同的短贡献标签。
2. 正文以 `# 目录` 和原生目录块开始。
3. `# 参考` 后依次为 `0-8`。
4. 数据库标题不在正文重复。
5. 图表始终紧邻其编号与分析。

默认风格是克制的原生学术笔记：连续段落、动态标题，只有真实行列数据才
用表格；不自动添加 callout、分栏、封面或装饰色。

[脱敏 enhanced-Markdown 示例](../../examples/deepseekmoe/notion.md) |
[逻辑属性 fixture](../../examples/deepseekmoe/notion-properties.json) |
[完整案例说明](../../examples/deepseekmoe/README.md)

属性 fixture 表示 canonical 值，不是 Notion API payload；其中没有
database ID、page ID、工作区 schema 或账号信息。

## 飞书

飞书是一等发布后端，不只是 XML 导出：

1. 使用原生文档标题。
2. 顶部两列表紧凑展示单位、正式发表、首次公开（若不同）、venue、论文
   类型、主题、短贡献和 canonical links。
3. 用原生标题大纲导航，不伪造目录。
4. 公式、表格、链接、图片使用原生 XML/block。
5. 长文先建骨架，再由同一 Agent 串行写入并读回。

[Canonical 飞书 XML 示例](../../examples/deepseekmoe/lark.xml) |
[完整案例说明](../../examples/deepseekmoe/README.md)

## 能力与回退顺序

每个远程后端都按相同顺序选择能力：

1. 已连接的平台工具、App 或 MCP。
2. 已认证的本地 CLI：`ntn` 或 `lark-cli`。
3. 必要时保留脱敏离线平台工件，并以 Markdown 作为可移植保底。

完成报告对每个目标独立记录 `success`、`partial` 或 `blocked`，
绝不编造远程 URL。

## 安全更新

查重依次使用 DOI、arXiv ID、canonical URL、规范化精确标题。唯一命中
则更新，无命中则创建；存在歧义时只阻塞受影响目标。

更新前完整读取已有工件，保留有价值的自定义章节、批注、图片、附件、
embed、子页面和画板。只有确认不会删除应保留内容时，才允许全量替换。
