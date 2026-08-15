# Paper Analysis Quality Standard

## Contents

- Evidence map
- Required chapter intent
- Depth and style
- Figure and table callouts
- Limitations and judgment
- Rating
- Verification

## Evidence map

Build this compact map before drafting:

1. **Problem and scope**: the gap addressed and what remains outside scope.
2. **Core artifact**: model, method, dataset, benchmark, system, taxonomy, or
   report.
3. **Mechanism**: inputs, outputs, components, data flow, objectives, stages,
   design choices, and implementation details.
4. **Evidence**: datasets, benchmarks, metrics, baselines, main comparisons,
   ablations, qualitative cases, human studies, efficiency, and governance.
5. **Visual anchors**: five to eight real numbered figures or tables for a
   substantial paper, or every materially useful item when fewer exist. Record
   label, caption, source location, supported claim, and interpretation.
6. **Boundaries**: access, reproducibility, cost, coverage, validity, release,
   safety, language, modality, domain, and overclaim risk.

Draft from this map. Do not fill a template from top to bottom before the
paper's argument is understood.

## Required chapter intent

Use the user's language while retaining these numeric anchors:

- `Sources`: canonical paper and supporting first-party links.
- `0`: dense short take with thesis, value, strongest evidence, and boundary.
- `1`: problem, artifact, contribution, method or construction, and main result.
- `2`: prior line of work, direct alternatives, and the paper's positioning.
- `3`: paper-specific mechanism, construction process, system, or taxonomy.
- `4`: paper-specific experimental or analytical evidence.
- `5`: concrete limitations and distribution boundaries.
- `6`: confirmed contribution and unresolved questions.
- `7`: first-person research judgment and what to watch next.
- `8`: later versions, replications, related releases, and follow-up work.

Rename chapters `3` and `4`, and every subsection beneath them, to describe the
paper. Do not retain headings such as "Method/Architecture/Data" when only one
part applies.

## Depth and style

- Write a finished professional note, not a blog recap or section outline.
- Use the deep profile for completed analysis. Chapter `0` normally has three
  to five dense paragraphs; chapters `3` and `4` normally have three to six
  substantive subsections when the evidence supports them.
- Keep mechanism and evidence sections grounded in the paper.
- Explain inputs, outputs, assumptions, design rationale, and why each retained
  detail matters.
- State what a result proves and what it does not prove.
- Use at least two paper-specific paragraphs for a core subsection when the
  evidence warrants that subsection.
- Integrate implementation details that make later reuse possible.
- Put personal interpretation in chapters `0` and `7`; do not blur it into the
  paper's claims.
- Center the note on the paper. Put later product or model-family updates in
  chapter `8`.
- Match length to evidence. Do not pad a short position paper to imitate a long
  technical report.
- Do not compress chapters `5`, `6`, or `7` into a generic closing paragraph.
  Cover concrete boundaries, confirmed versus unresolved claims, and developed
  research judgment separately.

For a technical report, capture model sizes, architecture, context limits, data
and training stages, objectives, sampling or decoding, post-training,
efficiency, release status, and deployment constraints when reported.

## Figure and table callouts

Use five to eight anchors for a substantial paper when that many useful
numbered items exist. In marker mode use the paper's exact numbering:

```markdown
> [Figure 1]

Figure 1 shows ... The result supports ... It does not establish ...

> [Table 2]

Table 2 compares ... The decisive result is ... The comparison is limited by ...
```

Use forms such as `Appendix Figure 2`, `Figure A.1`, or `Table S3` when those
are the paper's labels. Do not invent numbers or write generic `Figure X`.

Every callout must be followed immediately by analysis. Do not leave placement
instructions, image-upload reminders, or a list of visuals without
interpretation. Do not add a callout merely to reach a count.

In extract mode, insert the media immediately before the same formal label and
analysis. The presence of an image does not replace analytical prose.

## Limitations and judgment

Discuss limitations concretely:

- Data availability, contamination, licenses, privacy, or annotation quality.
- Missing implementation detail, code, prompts, checkpoints, or compute budget.
- Metric validity, baseline comparability, uncertainty, and test-set access.
- Language, modality, domain, demographic, geographic, or temporal coverage.
- Deployment cost, latency, reliability, safety, and governance when relevant.
- Whether the evidence supports the headline claim outside the tested setting.

Separate limitations acknowledged by the authors from additional analysis.
Avoid generic paragraphs that could apply to any paper.

## Rating

Treat rating as optional metadata. Set it only when evidence supports a
meaningful judgment. Consider novelty, reproducibility, likely influence,
intellectual interest, and importance. Never include rating deliberation or a
scoring rubric in the note body.

## Verification

Read the final artifact back and check:

- Metadata identifies the correct paper and primary sources.
- Every requested target reflects the same manuscript, visual labels, and
  research judgment.
- Topics and contributions each contain no more than four precise values.
- `Sources` and chapters `0` through `8` exist.
- Chapters `3` and `4` have paper-specific titles.
- Core subsections contain analysis rather than one-line prompts.
- Figure/table callouts use real numbering and immediate analysis.
- Claims preserve metrics, settings, and uncertainty.
- Personal judgment is distinguishable from reported evidence.
- No scratch work, scoring deliberation, migration notes, or authoring
  instructions remain.
- No unresolved `TODO`, generic `Figure X`, generic `Table X`, "placeholder",
  "put this figure here", `占位`, `旧页面`, `编辑记录`, `本次修改`, or similar
  process text remains.

When the Markdown validator is available, run:

```bash
python scripts/validate_note.py <note-path>
```

Use `--min-evidence 0` only when the paper genuinely has no useful numbered
figures or tables, and explain that caveat in the completion report.
