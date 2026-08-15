# Getting Started

[English](../en/getting-started.md) | [简体中文](../zh-CN/getting-started.md)

## Requirements

The repository contains a canonical Agent Skill rather than a standalone
application or SDK. Use a host that supports Agent Skills, or point another
agent at `skills/analyze-paper/SKILL.md`.

Remote publishing is optional:

- Markdown needs only a writable directory.
- Notion needs a connected Notion tool/MCP or an authenticated `ntn` CLI.
- Feishu/Lark needs a connected document tool/MCP or authenticated
  `lark-cli`.

Credentials remain in the host or CLI credential store.

## Install

From the repository root:

```bash
./scripts/install.sh --target codex
./scripts/install.sh --target claude
./scripts/install.sh --target agents --dest /path/to/project/.agents/skills
```

Existing installations are protected. Inspect a destination with `--dry-run`
or explicitly replace the installed Skill with `--force`.

## First analysis

An ordinary request is enough:

```text
Use $analyze-paper to analyze https://arxiv.org/abs/2401.06066 in Chinese.
```

Markdown is the zero-configuration default. A writable run creates
`paper-notes/<paper-slug>.md`; a read-only run returns the complete Markdown
in the response.

Request several outputs in one run:

```text
Analyze this paper deeply in Chinese. Produce Markdown and publish the same
manuscript to Notion and Feishu. Keep figure markers; do not extract images.
```

The current request overrides configured outputs and media mode.

## What the agent does

1. Resolves the exact paper and checks the selected destinations for duplicates.
2. Collects primary sources and classifies the paper type.
3. Builds an evidence map and optional media manifest.
4. Drafts one deep, target-neutral manuscript.
5. Renders each selected target from that manuscript.
6. Reads every completed artifact back and reports target-specific status.

When the host supports isolated workers, the main agent delegates the complete
single-paper workflow to one fresh worker. It does not split chapters among
independent writers. Without workers, the same contract runs inline.

## Completion states

Each requested target returns one state:

- `success`: written and read back successfully.
- `partial`: analysis completed but remote publishing or some media failed;
  an offline artifact or Markdown fallback remains.
- `blocked`: that target could not be safely created or updated, for example
  because duplicate matching was ambiguous.

One failed target does not remove or roll back successful artifacts.
