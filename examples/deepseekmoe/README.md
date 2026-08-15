# DeepSeekMoE Golden Example

This directory renders one evidence-grounded manuscript to three targets:

| Target | Fixture | Sanitized body screenshot |
| --- | --- | --- |
| Portable Markdown | [markdown.md](markdown.md) | [markdown.png](screenshots/markdown.png) |
| Notion enhanced Markdown | [notion.md](notion.md) and [logical properties](notion-properties.json) | [notion.png](screenshots/notion.png) |
| Feishu/Lark native XML | [lark.xml](lark.xml) | [lark.png](screenshots/lark.png) |

The [media manifest](media.yaml) records six extracted visuals and two marker
fallbacks. The extracted files are cropped from the official ACL 2024 PDF,
which is distributed under CC BY 4.0; source, page, purpose, license, and
attribution remain in the manifest.

The Notion fixture contains enhanced page-body Markdown only. Its companion
JSON contains canonical logical metadata, not a real API payload. The Lark
fixture uses only documented native XML tags. No fixture contains a page ID,
document token, workspace schema, signed URL, account identity, credential, or
local path.

Canonical `contributions` are deliberately rendered as four short property
tags: `细粒专家`, `共享专家`, `消融验证`, and `规模扩展`. Their full claims and
evidence remain in chapters 1 and 6 rather than being compressed into metadata.

## 中文

本目录把同一份有证据支撑的 DeepSeekMoE 主稿渲染为可移植 Markdown、
Notion enhanced Markdown 和飞书原生 XML。六张开放许可图表用于展示
`extract` 的最佳效果，Figure 4 和 Figure 5 则保留 marker，用来展示
混合回退。

Notion 的 JSON 只表示脱敏后的逻辑属性，不是实际 API payload；飞书 XML
只使用公开支持的标签。截图只保留文档正文，不包含账号、工作区、页面 ID、
私有属性值或本地路径。

`contributions` 固定为 `细粒专家`、`共享专家`、`消融验证`、`规模扩展`
四个短标签；完整贡献和证据仍在第 1、6 章展开，不塞进属性值。
