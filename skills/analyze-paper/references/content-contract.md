# Content Contract

## Contents

- One manuscript, many targets
- Canonical metadata
- Deep manuscript
- Evidence anchors
- Rendering invariants
- Multi-target completion

## One manuscript, many targets

Create one target-neutral manuscript after resolving the paper, classifying its
type, and building the evidence map. Render every requested target from this
same manuscript. Do not independently rewrite the analysis for Markdown,
Notion, or Lark.

The manuscript consists of:

1. Canonical metadata.
2. Primary and supporting source records.
3. Chapters `0` through `8` with paper-specific chapters `3` and `4`.
4. Visual evidence records for selected figures and tables.
5. Optional equations, compact data tables, and code excerpts.
6. A media manifest when extracted assets are available.

Keep target markup out of the manuscript. Apply heading levels, table-of-
contents blocks, property mappings, media uploads, and XML escaping only while
rendering a target.

## Canonical metadata

Use these keys across targets:

- `title`
- `institutions`
- `paper_url`
- `pdf_url` when known
- `arxiv_url` when known
- `doi` when known
- `published`
- `venue`
- `paper_type`
- `topics`, with at most four values
- `contributions`, with at most four values
- `project_url` when known
- `code_url` when known
- `status`
- `rating` only when evidence supports a useful judgment
- `sources`

Authors may be collected for identity resolution and citations, but they are
not a substitute for `institutions` in portable note metadata.

## Deep manuscript

Use the deep profile for every completed analysis. Depth means exhausting the
useful evidence, not padding a short paper.

- `0`: normally three to five dense paragraphs covering thesis, value,
  mechanism, strongest evidence, and the most important boundary.
- `1`: explain the problem, artifact, contribution, method or construction,
  main evidence, and larger significance.
- `2`: reconstruct the prior line, direct alternatives, contribution type, and
  precise positioning.
- `3`: normally three to six substantive subsections. Explain inputs, outputs,
  assumptions, components, stages, implementation, and design rationale.
- `4`: normally three to six substantive subsections. Explain protocols,
  metrics, comparisons, ablations or cases, decisive results, and what those
  results do not establish.
- `5`: separate author-acknowledged limitations from additional analysis and
  cover the concrete boundaries that materially affect interpretation.
- `6`: distinguish confirmed contributions from unresolved questions.
- `7`: provide a developed first-person research judgment, connections to
  neighboring routes, and what should be tested or tracked next.
- `8`: annotate later versions, official releases, replications, and follow-up
  work instead of listing bare links.

A core subsection should usually contain at least two paper-specific
paragraphs: one for mechanism or setup and one for interpretation, evidence,
or boundary. Use fewer subsections when the paper lacks evidence; never invent
content to meet a count.

## Evidence anchors

Represent every retained visual with:

- Exact label, such as `Figure 2`, `Table 4`, or `Appendix Figure A.1`.
- Official caption or a faithful concise description.
- Source page or source URL when available.
- The claim it supports.
- Immediate analysis of the result and its boundary.
- Optional stable media asset and license record.

Use five to eight anchors for a substantial paper when that many materially
useful numbered items exist. Follow the media policy for marker, extraction,
and upload behavior.

## Rendering invariants

All targets must preserve:

- The same paper identity and canonical links.
- The same chapter order and paper-specific chapter meaning.
- The same confirmed claims, metrics, settings, and uncertainty.
- The same visual labels and associated analysis.
- The same distinction between paper claims and research judgment.

Targets may differ only where the platform requires it: visible title,
frontmatter or database properties, heading level, table of contents, native
tables, media references, and block markup.

## Multi-target completion

Resolve every requested target before writing. Draft once, then render and
verify each target independently. A failed target must not roll back a
successful target.

Always preserve or return the Markdown artifact when possible. Report each
target with:

- `target`: markdown, notion, or lark.
- `status`: success, partial, or blocked.
- `artifact`: path or verified page URL.
- `operation`: created, updated, rendered-only, or none.
- `media`: markers, extracted count, uploaded count, or off.
- `verification`: checks performed.
- `caveat`: target-specific failure or none.
