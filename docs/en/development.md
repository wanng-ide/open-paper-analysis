# Development

[English](../en/development.md) | [简体中文](../zh-CN/development.md)

## Repository layout

```text
skills/analyze-paper/       Canonical cross-agent Skill
  SKILL.md                  Compact execution workflow
  references/               Content, quality, media, and backend contracts
  assets/                   Public configuration example
  scripts/                  Artifact validator
examples/deepseekmoe/       Three-target golden example and open media
evals/cases.yaml            Behavioral evaluation matrix
scripts/                    Installer and repository checks
docs/en, docs/zh-CN         Mirrored guides
```

There is one canonical Skill. The installer copies it into Codex, Claude Code,
or a generic Agent Skills directory; do not maintain separate Skill bodies.

## Local validation

```bash
npx --yes skills-ref@0.1.5 validate skills/analyze-paper
python /path/to/skill-creator/scripts/quick_validate.py skills/analyze-paper
python skills/analyze-paper/scripts/validate_note.py examples/deepseekmoe/markdown.md
python skills/analyze-paper/scripts/validate_note.py examples/deepseekmoe/notion.md
python skills/analyze-paper/scripts/validate_note.py examples/deepseekmoe/lark.xml
python scripts/validate_examples.py
python scripts/check_markdown_links.py
python scripts/check_docs_parity.py
bash scripts/test-install.sh
```

CI additionally parses configuration, compiles Python scripts, scans Git
history with Gitleaks, and runs all installer targets.

## Evaluation matrix

Behavioral cases cover model/method, benchmark, system, survey, title
resolution, safe updates, duplicate ambiguity, marker and extraction media,
multi-target partial failure, unavailable platforms, and read-only output.

Forward tests should include:

- One method paper rendered to all three targets.
- One dataset/benchmark paper whose chapters `3` and `4` remain
  benchmark-specific.
- A partial-failure run proving one unavailable backend does not roll back
  Markdown.

## Live smoke tests

Use a clearly marked temporary title and a non-production destination. For both
Notion and Lark:

1. Create properties/title, body, equations, links, and media.
2. Read the artifact back and verify chapters, metadata, and evidence labels.
3. Capture a body-only screenshot with account and workspace chrome excluded.
4. Move the temporary artifact to trash.
5. Record only redacted status and counts in the pull request.

Never commit the test URL, page/document ID, private schema, account name,
signed media URL, or local configuration. Claude runtime testing is recorded as
not run when Claude Code is unavailable; format validation still runs.

## Contributions

Keep changes aligned with the content contract and existing platform
references. Add abstractions only when they prevent real target drift or
validation duplication. A backend change should update its reference, golden
fixture, validator, evaluation cases, both language guides, and pull-request
test evidence.
