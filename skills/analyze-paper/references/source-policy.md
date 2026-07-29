# Source Policy

## Contents

- Source priority
- Paper resolution
- Evidence collection
- Claim discipline
- Access failures

## Source priority

Use primary sources whenever available:

1. The paper PDF and official abstract page.
2. Official paper source files or appendix.
3. Venue or proceedings page.
4. Author-maintained project page.
5. Official code repository.
6. Official model card or dataset card.
7. Author talks, posts, or released artifacts.

Use secondary sources only to discover primary material or to identify a
specific external criticism that the note labels as external. Do not substitute
a news article, social post, generated summary, or repository README for the
paper's experimental claims.

## Paper resolution

- Prefer a canonical abstract page over a direct PDF URL in metadata.
- Record the DOI when one exists.
- For title-only requests, identify the unique paper through title, authors,
  year, and venue before drafting.
- Treat an official project page or repository as a route to the paper, not
  automatically as the paper itself.
- If two papers plausibly match the request, stop and report both candidates.
- If the user supplies an existing note, independently resolve its paper source
  before updating it.

## Evidence collection

Capture:

- Exact title, authors for identity resolution, primary institutions,
  publication or submission date, and venue status.
- Research question and explicit scope.
- Inputs, outputs, modules, data flow, objectives, and assumptions.
- Data sources, filtering, annotation, splits, scale, and licenses.
- Training, inference, implementation, deployment, and resource details.
- Evaluation tasks, metrics, baselines, human comparisons, and uncertainty.
- Ablations, robustness checks, qualitative cases, and failure examples.
- Numbered figures and tables that support central claims.
- Release status for code, data, checkpoints, prompts, and evaluation tools.

Read captions and the surrounding discussion for each retained figure or table.
Do not infer a result from a caption alone when the body qualifies it.

Resolve institutions from the paper's affiliation block, official source
package, or venue PDF. Use the official full affiliation names, retain named
laboratories or institutes when present, and deduplicate spelling variants.
Do not infer an institution from an email domain or author biography alone.

## Claim discipline

- Distinguish paper claims, directly observed results, and personal judgment.
- Preserve units, metric direction, evaluation split, and comparison setting.
- Say when a baseline uses a different model, data budget, prompt, or protocol.
- Avoid converting correlation, benchmark performance, or preference ratings
  into stronger causal or real-world claims.
- Do not invent missing hyperparameters, costs, licenses, or release plans.
- Mark an omitted detail as a reproducibility limitation.
- Keep quotations short and necessary; paraphrase by default.

## Access failures

If the PDF is inaccessible, try the official abstract page, source package,
venue page, and author artifacts. If the available evidence cannot support a
professional note, return `partial` or `blocked` and name the missing source.
Do not fill gaps from memory without clearly labeling the limitation.
