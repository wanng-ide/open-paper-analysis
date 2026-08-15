# Configuration

## Contents

- Discovery
- Version 2
- Run-time overrides
- Version 1 compatibility
- Privacy boundary

## Discovery

Load the first existing configuration in this order:

1. A path explicitly supplied by the user.
2. `.open-paper-analysis.toml` in the working project.
3. `~/.config/open-paper-analysis/config.toml`.

No configuration is required. Without one, use deep analysis, marker media, and
Markdown under `paper-notes`.

## Version 2

Version 2 separates shared defaults, media policy, and target destinations:

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

`defaults.outputs` accepts one or more unique values from `markdown`,
`notion`, and `lark`. Preserve Markdown as the fallback even when it is not
an explicitly requested publishing target. `language = "auto"` follows the
user. The only completed-analysis depth profile is `deep`.

`media.mode` accepts `markers`, `extract`, or `off`. Enforce
`max_items` only for extraction. Treat
`license_policy = "open-or-approved"` as a hard permission boundary.

Notion property names live under `[notion.properties]`; fixed select values
may live under `[notion.values]`. Read the live schema before mapping either.

`lark.parent_token` and `lark.parent_position` are mutually exclusive when
the selected capability enforces that constraint. An empty target means the
host or user must supply a destination before remote publishing.

## Run-time overrides

The current user request overrides configuration. Resolve:

1. Explicit outputs, paths, parent locations, language, and media mode.
2. Discovered version 2 or version 1 configuration.
3. Built-in defaults.

Do not rewrite a user's configuration as a side effect of paper analysis.

## Version 1 compatibility

Accept the original version 1 keys without requiring migration:

- `[defaults].output` becomes a one-item output list.
- `[defaults].notes_directory` becomes `[markdown].notes_directory`.
- `[notion].enabled = true` adds `notion` when the current request does not
  specify outputs.
- Existing Notion destination and property mapping keys keep their meaning.

If both version 1 and version 2 forms appear, prefer the version 2 form and
report the ignored legacy key as a non-blocking configuration warning.

## Privacy boundary

Configuration may contain destination IDs and property mappings on the user's
machine. It must never contain API keys, OAuth tokens, client secrets, session
cookies, upload tokens, signed media URLs, user identities, or credentials.
Authentication belongs to the connected tool, MCP server, CLI credential
store, or host environment.

Never copy local configuration into a paper note, fixture, log excerpt, pull
request, or public repository. Redact destination identifiers in test reports.
