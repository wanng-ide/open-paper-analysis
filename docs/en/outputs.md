# Output Backends

[English](../en/outputs.md) | [简体中文](../zh-CN/outputs.md)

## One manuscript

The agent makes research decisions once. Canonical metadata, sources, chapters
`0` through `8`, evidence anchors, equations, tables, limitations, and
research judgment form one semantic manuscript. Backend rendering may change
only platform structure and media transport.

All targets preserve paper identity, chapter meaning, metrics, uncertainty,
Figure/Table labels, and the distinction between reported evidence and personal
judgment.

## Markdown

Markdown is the default and universal fallback. It uses:

- YAML metadata with official institutions, not an author list.
- Separate formal publication and first-public preprint dates when both exist.
- One to four compact contribution tags. Chinese tags use at most four Han
  characters and space-delimited tags use at most four words; detailed claims
  remain in the body.
- A visible paper title and linked contents.
- `Sources`, then numbered chapters `0` through `8`.
- Standard equations, tables, links, and stable relative image paths.
- No Notion tags or Lark XML.

[Markdown example](../../examples/deepseekmoe/markdown.md) |
[body screenshot](../../examples/deepseekmoe/screenshots/markdown.png)

## Notion

Notion uses official enhanced Markdown plus structured property calls:

1. Database properties contain canonical metadata through the live schema map,
   including the same compact contribution tags used by Markdown.
2. The body begins with `# 目录` and a native table-of-contents block.
3. `# 参考` precedes chapters `0` through `8`.
4. The page title is not repeated in the body.
5. Figures remain adjacent to their numbered analysis.

The default style is a restrained native academic note: continuous paragraphs,
dynamic headings, tables only for real tabular evidence, and no automatic
callouts, columns, cover, or decorative color.

[Sanitized enhanced-Markdown example](../../examples/deepseekmoe/notion.md) |
[logical property fixture](../../examples/deepseekmoe/notion-properties.json) |
[body screenshot](../../examples/deepseekmoe/screenshots/notion.png)

The property fixture describes canonical values, not a Notion API payload. It
contains no database ID, page ID, workspace schema, or account data.

## Feishu/Lark

Feishu/Lark is a full publishing backend, not only an export file:

1. The document title is set with the native title field.
2. A compact two-column table presents institutions, formal publication,
   first-public preprint date when distinct, venue, type, topics, compact
   contributions, and canonical links.
3. Native headings provide the document outline; no fabricated contents
   section is added.
4. Equations, tables, links, and images use native XML/block types.
5. Long documents are created as a skeleton and filled serially by the same
   agent, then read back.

[Lark XML example](../../examples/deepseekmoe/lark.xml) |
[body screenshot](../../examples/deepseekmoe/screenshots/lark.png)

## Capability and fallback order

For each remote backend:

1. Use an available connected platform tool, app, or MCP.
2. Otherwise use an authenticated local CLI: `ntn` or `lark-cli`.
3. Otherwise preserve an offline platform fixture when useful and return
   Markdown as the portable fallback.

The completion report records `success`, `partial`, or `blocked` for each
target independently. It never invents a remote URL.

## Safe updates

Duplicate matching uses DOI, arXiv ID, canonical URL, then exact normalized
title. Update one unique match, create when none exists, and stop the affected
target on ambiguity.

Before an update, the agent reads the existing artifact and preserves useful
custom sections, annotations, images, attachments, embeds, child pages,
whiteboards, and other user material. Full-body replacement is allowed only
after inspection proves it will not delete content that must remain.
