---
name: analyze-paper
description: Analyze a single research paper and create or update an evidence-grounded professional paper note. Use when the user asks to read, analyze, explain, summarize, interpret, or take notes on a paper, or supplies an arXiv link, PDF, DOI, title, project page, code repository, existing Markdown note, or Notion paper page. Classify the paper type, prioritize primary sources, produce verified Markdown by default, and optionally publish to Notion when configured.
---

# Analyze Paper

Analyze one research paper deeply and leave a verified, reusable note. Preserve
the paper's actual mechanism and evidence instead of producing a generic
summary.

## Required references

Read these files before drafting:

- [Source policy](references/source-policy.md) for discovery and evidence rules.
- [Quality standard](references/quality-standard.md) for the evidence map,
  chapter intent, figure/table analysis, and verification.
- [Paper types](references/paper-types.md) after classifying the paper.

Read the destination-specific reference before writing:

- [Markdown output](references/markdown-output.md) for the default output.
- [Notion publishing](references/notion-publishing.md) only when the user asks
  for Notion or a discovered configuration enables it.

## Scope and defaults

- Handle one paper per run. If the request names multiple papers, ask the user
  to choose one; do not silently turn the task into a comparison or survey.
- Follow the user's language for the note. Preserve official names, metrics,
  benchmark names, and technical terms when translation would reduce precision.
- Resolve the destination in this order: explicit user request, discovered
  configuration, Markdown.
- In a writable environment, write Markdown to
  `paper-notes/<paper-slug>.md` unless the user supplies a path. If file writing
  is unavailable, return the complete Markdown in the response.
- Treat Notion as optional. Missing Notion tools or configuration must not
  block Markdown analysis.
- Do not upload paper figures or other media unless the user explicitly asks.

## Execution mode

Use a fresh isolated worker for real single-paper analysis when the host offers
subagents, workers, or equivalent isolated execution. Otherwise run the same
workflow in the current context.

When delegating:

1. Pass only the original request, paper source, output constraints, this Skill
   path, and any explicit configuration path.
2. Require the worker to read this file and all applicable references.
3. Assign the whole analysis, duplicate check, write, and read-back verification
   to that worker. Do not draft the same note in parallel.
4. Keep Skill inspection, editing, and explanation in the current agent unless
   independent validation is explicitly useful.
5. Close or release the worker when the host requires cleanup.

## Workflow

1. Resolve the input to a paper URL, PDF, DOI, exact title, official project or
   code page, or existing note.
2. Resolve the output target and optional configuration. Never copy credentials
   or personal identifiers into the note or Skill.
3. Search the selected destination for the same arXiv ID, DOI, canonical paper
   URL, or exact title. Update one unique match, create when none exists, and
   stop on multiple plausible matches.
4. Gather primary sources first: paper abstract and PDF, official source files
   when useful, venue page, project page, official repository, dataset/model
   card, and author-provided appendices.
5. Classify the paper as model/method, dataset/benchmark, system/tool,
   survey/position, technical report, or other.
6. Build an evidence map before drafting: problem, scope, artifact, mechanism,
   implementation or construction, decisive experiments, ablations or cases,
   key numbered figures/tables, limitations, and follow-up links.
7. Draft from the evidence map using paper-specific headings. Keep confirmed
   claims separate from personal research judgment.
8. Write or update the selected artifact. Preserve user-added media, links,
   custom sections, and useful old notes unless replacement was requested.
9. Read the artifact back and verify metadata, sources, chapter structure,
   figure/table callouts, analysis depth, and absence of process text.
10. Return the artifact path or page URL plus a concise completion report.

## Completion report

Include:

- `status`: success, partial, or blocked.
- `artifact`: final file path or page URL.
- `operation`: created or updated.
- `paper_type`: selected classification.
- `sources`: primary sources used.
- `metadata`: important values written.
- `figure_table_callouts`: count and retained labels.
- `verification`: read-back and structural checks performed.
- `caveats`: unresolved ambiguity, missing official source, reproducibility
  boundary, publishing fallback, or none.

Do not claim successful publishing without reading the destination back.
