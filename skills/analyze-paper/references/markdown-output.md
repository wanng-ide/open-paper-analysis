# Markdown Output

## Contents

- Destination and naming
- Metadata contract
- Visible document structure
- Body contract
- Media rendering
- Duplicate handling
- Safe updates
- Read-back verification

## Destination and naming

Use an explicit user path when provided. Otherwise use `[markdown].notes_directory`;
default to `paper-notes`.

Choose `<paper-slug>` in this order:

1. A stable, recognizable short paper or project name.
2. The arXiv identifier prefixed with `arxiv-`.
3. A lowercase hyphenated English title shortened to 80 characters.
4. `paper-<publication-year>-<first-author>` when no better stable slug exists.

Avoid filesystem-sensitive characters. Do not silently overwrite an unrelated
file with the same slug.

## Metadata contract

Begin the note with YAML frontmatter:

```yaml
---
title: "Exact paper title"
institutions:
  - "Primary institution"
paper_url: "https://canonical-paper-page"
pdf_url: "https://optional-direct-pdf"
doi: "optional DOI"
published: "YYYY-MM-DD"
venue: "venue, arXiv, or unknown"
paper_type: "model/method"
topics:
  - "precise topic"
contributions:
  - "expert segmentation"
project_url: "optional official project page"
code_url: "optional official repository"
status: "analyzed"
rating: 4
sources:
  - "https://primary-source"
---
```

Use `institutions` for the official affiliations that materially represent the
paper. Prefer the full names printed in the paper or official source, preserve
distinct laboratories or institutes when they are part of the affiliation, and
deduplicate aliases. Do not use an author list as a substitute for
institutions.

Keep `topics` and `contributions` to at most four values each. Contribution
values are compact property tags, not mini-abstracts: use no more than four Han
characters for a Chinese tag or four words for a space-delimited tag. Keep
metrics, settings, and complete contribution claims in the body. Omit optional
keys whose values are unknown rather than inventing them. Omit `rating` when
there is not enough evidence for a useful personal judgment.

Use canonical URLs. Keep credentials, local tool configuration, private
database IDs, and scratch paths out of metadata.

## Visible document structure

After frontmatter, render a visible document title and a linked contents list.
Use standard portable Markdown rather than Notion or Lark tags:

```markdown
# Exact paper title

## Contents

- [Sources](#sources)
- [0 Short take](#0-short-take)
- [1 Summary](#1-summary)
...

## Sources
```

Keep the title at level 1, chapters at level 2, and chapter subsections at
level 3. Link labels and anchors may follow the user's language.

## Body contract

Use headings in the user's language while preserving numeric anchors:

```markdown
## Sources

## 0 Short take

## 1 Summary

## 2 Background and positioning

## 3 <Paper-specific mechanism, construction, system, or argument>

## 4 <Paper-specific evidence>

## 5 Limitations and boundaries

## 6 Conclusion

## 7 Research judgment

## 8 Follow-up references
```

Put only source links and short source labels under `Sources`. Use the quality
standard for chapter depth and figure/table callouts.

## Media rendering

Follow the shared media policy.

In marker mode:

```markdown
> [Figure 1]

Figure 1 shows ... It supports ... It does not establish ...
```

In extract mode:

```markdown
![Figure 1: concise official caption](assets/paper-slug/figure-1.png)

**Figure 1.** Figure 1 shows ... It supports ... It does not establish ...
```

Use relative paths under the configured assets directory. Include provenance
and license information in a nearby source note or media manifest. Never place
an expiring platform URL in Markdown.

## Duplicate handling

Before creating a note, inspect Markdown files in the destination directory.
Match in this order:

1. Same DOI.
2. Same arXiv identifier or canonical `paper_url`.
3. Exact normalized title.

Update one unique match. Create when no match exists. Stop and report ambiguity
when multiple files plausibly match.

## Safe updates

Read the complete existing file before editing.

- Preserve local images, attachments, custom top-level sections, annotations,
  and links not superseded by corrected paper evidence.
- Update canonical metadata and structured chapters in place.
- Do not explain migration mechanics inside the final note.
- Do not replace the complete file unless the user requested replacement or the
  existing note contains no material that needs preservation.
- If an existing claim conflicts with the paper, correct it and preserve the
  user's separate annotation only when clearly labeled as personal.

## Read-back verification

Read the written file from disk, not the in-memory draft. Confirm:

- The path and slug are correct.
- YAML frontmatter is closed and contains required metadata, including official
  institutions rather than an author list.
- A visible title, linked contents, `Sources`, and chapters `0` through `8` are
  present.
- Chapters `3` and `4` are paper-specific.
- Figure/table markers or extracted media are real, numbered, and analyzed.
- No Notion enhanced-Markdown tags or Lark XML tags remain.
- No existing user media or custom content was accidentally lost.
- No authoring instructions or scratch text remain.

Run the bundled validator from the Skill directory when executable tools are
available:

```bash
python scripts/validate_note.py /absolute/path/to/note.md
```
