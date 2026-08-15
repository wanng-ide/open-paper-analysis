# Configuration

[English](../en/configuration.md) | [简体中文](../zh-CN/configuration.md)

## Discovery order

Configuration is optional. The Skill loads the first existing file:

1. A path explicitly supplied in the request.
2. `.open-paper-analysis.toml` in the current project.
3. `~/.config/open-paper-analysis/config.toml`.

Copy `skills/analyze-paper/assets/config.example.toml` as a starting point.
Do not commit a populated local configuration.

## Configuration schema

```toml
version = 2

[defaults]
outputs = ["markdown"]
language = "auto"
depth = "deep"

[media]
mode = "markers"
max_items = 6
license_policy = "open-or-approved"

[markdown]
notes_directory = "paper-notes"
assets_directory = "assets"

[notion]
database_id = ""
data_source_id = ""
template_page_id = ""

[lark]
parent_token = ""
parent_position = ""
doc_format = "xml"
```

### Defaults

`outputs` accepts unique values from `markdown`, `notion`, and `lark`.
It may contain one or several values. `language = "auto"` follows the user.
`depth = "deep"` is the sole completed-analysis profile; depth remains bounded
by available evidence.

### Media

`mode` accepts:

- `markers`: exact numbered Figure/Table anchors with analysis, no upload.
- `extract`: select and publish eligible media up to `max_items`.
- `off`: omit standalone media while retaining important prose evidence.

`open-or-approved` permits automatic extraction only for open-license
material, user-provided material, or explicitly approved reuse.

### Markdown

`notes_directory` controls the default note directory. `assets_directory`
controls stable relative media paths for extracted assets.

### Notion

Set a database or data-source destination only in local configuration. A
template is optional. `[notion.properties]` maps canonical metadata to the
live database schema; `[notion.values]` may contain fixed select values.
Empty optional mappings are skipped.

Map `published` to the formal publication property and `preprint_date` to a
distinct first-public preprint property when both exist in the live schema.

The publisher reads the live schema before writing. It never assumes private
property names from another workspace.

### Feishu/Lark

`parent_token` and `parent_position` identify the configured folder, Wiki
node, or library position. Leave both empty when the destination will be
provided in the request. They are mutually exclusive when the selected tool
requires it. XML is the default document format.

## Schema validation

The Skill supports only configuration files with `version = 2`. A file with a
missing or different version is not migrated or reinterpreted. The agent
reports the configuration problem and, when safe, continues from explicit
request values plus the built-in Markdown defaults. Paper analysis never
rewrites the user's configuration file.

## Credential boundary

Configuration may name destinations and property mappings. It must not contain
API keys, OAuth tokens, cookies, client secrets, upload tokens, signed media
URLs, user identities, or other credentials. Authentication belongs to the
connected tool, MCP, CLI credential store, or host environment.

Never include a populated local configuration in an issue, pull request,
fixture, note body, or test log.
