# Notion Publishing

## Contents

- Activation and fallback
- Configuration
- Tool selection
- Native paper-note style
- Duplicate and media safety
- Metadata mapping
- Publish and verify

## Activation and fallback

Use this integration only when the user explicitly requests Notion or
configured outputs include Notion.

Always finish the shared deep manuscript first. If Notion is unavailable or
misconfigured, preserve the Markdown artifact, return `partial`, and explain
the publishing issue. Do not downgrade the analysis or invent a page URL.

## Configuration

Discover configuration in this order:

1. A path explicitly supplied by the user.
2. `.open-paper-analysis.toml` in the working project.
3. `~/.config/open-paper-analysis/config.toml`.

Use [the configuration reference](configuration.md) and
[example configuration](../assets/config.example.toml) as the schema.
Configuration contains destinations and property mappings, never API tokens.
Authentication belongs to the connected Notion tool, MCP server, CLI, or host
credential store.

Require a database or data-source target before creating a database entry. A
template is optional. Treat a template as a lightweight skeleton; the shared
content contract, paper-type structure, and quality standard remain
authoritative.

## Tool selection

Choose the first usable capability:

1. A connected native Notion tool, app, or MCP server with page/database read
   and write access.
2. The `ntn` CLI when it is installed and authenticated.
3. A sanitized enhanced-Markdown artifact plus the portable Markdown fallback.

Use the selected tool's structured API for properties and blocks. Do not build
JSON by unsafe string interpolation.

For `ntn`, inspect live help before assuming command flags:

```bash
ntn --help
ntn pages --help
ntn api --help
```

Prefer the platform's enhanced Markdown page-content API when available. Use
structured block calls for properties, unsupported blocks, and media when
needed. Probe live capability rather than hardcoding a CLI version.

## Native paper-note style

Render the page body in this order:

```markdown
# 目录
<table_of_contents color="gray"/>

# 参考

论文：[canonical paper](https://paper.example)
项目主页：[official project](https://project.example)
GitHub：[official code](https://code.example)

# 0 省流

# 1 摘要

# 2 背景与定位

# 3 <paper-specific mechanism title>

# 4 <paper-specific evidence title>

# 5 局限与讨论

# 6 总结

# 7 个人研究判断

# 8 后续参考
```

Use the user's language for headings. Keep continuous academic paragraphs and
place selected media directly before its formal label and analysis. Do not add
callouts, columns, page covers, decorative colors, or dashboard-like cards by
default. Use native tables only for real row-and-column evidence and native
equations where the manuscript requires them.

Render inline equations as `$...$` and block equations as `$$...$$` in
enhanced Markdown. Do not carry portable `\\(...\\)` or `\\[...\\]` delimiters
into the Notion body.

The page title lives in the database title property. Do not repeat it as the
first body heading. Do not include portable YAML frontmatter in the page body.

## Duplicate and media safety

Query the target before writing. Match same DOI, arXiv ID, canonical paper URL,
or exact normalized title.

- Update one unique match.
- Create when none exists.
- Stop on multiple plausible matches.

Before updating, inspect the existing page and child blocks. Preserve
user-added images, files, embeds, bookmarks, annotations, and useful old notes.
Prefer precise enhanced-Markdown updates or block-aware edits. Use a destructive
full-body replacement only when the user requested it or inspection proves that
no material needs preservation.

## Metadata mapping

Read the live database schema before setting properties. Map canonical Markdown
metadata through `[notion.properties]` in the configuration.

- Reuse existing select and multi-select options when accurate.
- Map canonical `institutions` to the configured institution property. Preserve
  official affiliation names, deduplicate aliases, and do not populate it with
  author names.
- Keep topics and contributions to at most four options each.
- Create a new option only when no existing option fits.
- Do not assume English, Chinese, or any user's private property names.
- Skip an unmapped optional property rather than failing the entire publish.
- Never write configuration values or credentials into the page body.

Follow the media policy. In marker mode, use a restrained formal label followed
by analysis. In extract mode, upload or import the asset and place it directly
before the same label. Never persist signed Notion download URLs in local files
or public examples.

## Publish and verify

Create or update properties using structured calls, then write the enhanced
Markdown body using the safest block-aware operation available. For a long
page, write the heading skeleton and append chapters serially from the same
manuscript when the capability cannot accept the complete body reliably.

Read the page back and verify:

- The returned page belongs to the configured target.
- Canonical title and paper URL match.
- Mapped properties contain the intended values.
- The body begins with `目录`, contains the native table of contents and
  `参考`, and includes chapters `0` through `8`.
- Existing media remains present after an update.
- Figure/table callouts and their analysis remain adjacent.
- Media blocks, formal labels, and analysis remain adjacent and match the media
  manifest.
- No YAML frontmatter, Lark XML, signed media URL, or private target ID remains
  in the body.
- No scratch, migration, or authoring text remains.

Return the verified page URL. When Markdown was also written, report both
artifacts.
