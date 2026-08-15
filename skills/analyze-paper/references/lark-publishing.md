# Lark Publishing

## Contents

- Activation and fallback
- Configuration and capability selection
- Document style
- Duplicate and update safety
- Create and render
- Media
- Read-back verification

## Activation and fallback

Use Lark when the user requests a Feishu or Lark document, or when `lark`
appears in configured outputs.

Always complete the shared manuscript first. If no usable Lark capability is
available, preserve the Markdown artifact and render a `.lark.xml` offline
artifact when file writing is possible. Return the Lark target as `partial`;
do not invent a document URL.

## Configuration and capability selection

Read `[lark]` according to the
[configuration reference](configuration.md). A parent folder token, Wiki node,
or supported parent position is optional unless the selected capability
requires one.

Choose the first usable capability:

1. A connected Feishu or Lark document tool, app, or MCP server with create,
   read, and update access.
2. `lark-cli` with authenticated document and drive capabilities.
3. Offline Lark XML plus Markdown fallback.

Authentication belongs to the connected tool or host credential store. Never
place access tokens, user IDs, tenant IDs, or private document tokens in the
Skill, note body, or public fixtures.

Inspect live tool help or schemas before assuming command flags.

## Document style

Use native XML or structured block calls rather than importing raw portable
Markdown when the capability supports them.

- Set the document title separately. Do not repeat the exact title as the first
  body heading.
- Begin with a compact two-column metadata table for institution, date, venue,
  paper type, and canonical links. Omit empty rows.
- Use the native heading outline instead of a fabricated table-of-contents
  section.
- Follow with `参考` and chapters `0` through `8`.
- Keep continuous academic paragraphs. Use lists only for genuinely parallel
  items and tables only for real row-and-column data.
- Use restrained styling. Do not add decorative callouts, grids, colors, or
  whiteboards by default.
- Preserve inline links, bold text, code, equations, and real data tables with
  native blocks when supported.

Illustrative XML skeleton:

```xml
<title>Exact paper title</title>
<table>
  <tbody>
    <tr><td><b>机构</b></td><td>Primary institution</td></tr>
    <tr><td><b>论文</b></td><td><a href="https://paper.example">Canonical source</a></td></tr>
  </tbody>
</table>
<h1>参考</h1>
<p><a href="https://paper.example">论文</a></p>
<h1>0 省流</h1>
<p>Deep analysis...</p>
```

Escape XML text and attributes correctly. Use only tags supported by the live
capability.

## Duplicate and update safety

Search within the configured folder or Wiki scope before creating. Start with
the exact or shortened title, then confirm a unique candidate through DOI,
arXiv URL, or canonical paper URL in its body or metadata table.

- Update one unique match.
- Create when none exists.
- Stop on multiple plausible matches.

Before updating, fetch the document with block identifiers when available.
Preserve user-added images, files, embeds, whiteboards, annotations, and custom
sections. Prefer targeted block updates. Replace the entire body only after
inspection proves that no content requiring preservation will be deleted.

## Create and render

For a short document, create the complete body in one operation. For a deep
paper note, create the title and heading skeleton, then write one chapter at a
time in order using the same agent and manuscript. Re-fetch block identifiers
after operations that invalidate them.

Do not split chapters across independent workers. A fresh isolated paper worker
may own the complete analysis and publishing workflow, but the body must remain
one coherent manuscript.

## Media

Follow the media policy.

- In `markers` mode, write the formal label as a restrained bold paragraph or
  quote immediately before its analysis.
- In `extract` mode, upload the stable local asset, insert it immediately before
  the formal label and analysis, and verify the returned media block.
- In `off` mode, do not leave empty image blocks or authoring reminders.

## Read-back verification

Fetch the final document and confirm:

- Title and configured parent are correct.
- The metadata table contains the intended canonical values.
- `参考` and chapters `0` through `8` are present in order.
- Chapters `3` and `4` and their subsections are paper-specific.
- The heading outline is coherent and does not duplicate the document title.
- Links, equations, tables, and media survived rendering.
- Existing user media and custom content remain after an update.
- No Notion tags, YAML frontmatter, scratch text, credentials, tokens, or local
  paths remain.

Return the verified document URL and per-target completion record.
