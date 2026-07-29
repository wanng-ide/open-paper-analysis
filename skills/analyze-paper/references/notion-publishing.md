# Notion Publishing

## Contents

- Activation and fallback
- Configuration
- Tool selection
- Duplicate and media safety
- Metadata mapping
- Publish and verify

## Activation and fallback

Use this integration only when the user explicitly requests Notion or a
discovered configuration sets Notion as the default output.

Always finish the Markdown-quality analysis first. If Notion is unavailable or
misconfigured, preserve the Markdown artifact, return `partial`, and explain
the publishing issue. Do not downgrade the analysis or invent a page URL.

## Configuration

Discover configuration in this order:

1. A path explicitly supplied by the user.
2. `.open-paper-analysis.toml` in the working project.
3. `~/.config/open-paper-analysis/config.toml`.

Use [the example configuration](../assets/config.example.toml) as the schema.
Configuration contains destinations and property mappings, never API tokens.
Authentication belongs to the connected Notion tool, MCP server, CLI, or host
credential store.

Require a database or data-source target before creating a page. A template is
optional. Treat a template as a lightweight skeleton; the paper-type structure
and quality standard remain authoritative.

## Tool selection

Choose the first usable capability:

1. A connected native Notion tool, app, or MCP server with page/database read
   and write access.
2. The `ntn` CLI when it is installed and authenticated.
3. Markdown fallback.

Use the selected tool's structured API for properties and blocks. Do not build
JSON by unsafe string interpolation.

For `ntn`, inspect live help before assuming command flags:

```bash
ntn --help
ntn pages --help
ntn api --help
```

## Duplicate and media safety

Query the target before writing. Match same DOI, arXiv ID, canonical paper URL,
or exact normalized title.

- Update one unique match.
- Create when none exists.
- Stop on multiple plausible matches.

Before updating, inspect the existing page and child blocks. Preserve
user-added images, files, embeds, bookmarks, annotations, and useful old notes.
Use a destructive full-body replacement only when the user requested it or
inspection proves that no material needs preservation.

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

## Publish and verify

Create or update properties using structured calls, then write the Markdown
body using the safest block-aware operation available.

Read the page back and verify:

- The returned page belongs to the configured target.
- Canonical title and paper URL match.
- Mapped properties contain the intended values.
- The body includes `Sources` and chapters `0` through `8`.
- Existing media remains present after an update.
- Figure/table callouts and their analysis remain adjacent.
- No scratch, migration, or authoring text remains.

Return the verified page URL. When Markdown was also written, report both
artifacts.
