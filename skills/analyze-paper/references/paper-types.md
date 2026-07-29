# Paper Type Structures

## Contents

- Selection rule
- Model or method
- Dataset or benchmark
- System or tool
- Survey or position
- Technical report
- Other and hybrid papers

## Selection rule

Classify by the paper's primary contribution, not by the presence of a model,
dataset, or code artifact. Use one main structure. For a hybrid paper, retain
the dominant structure and add only the secondary subsections supported by
substantial evidence.

## Model or method

Use when the main contribution is an architecture, algorithm, training recipe,
inference method, objective, or adaptation technique.

Suggested mechanism chapter:

```markdown
# 3 <Method name and central mechanism>
## 3.1 <Problem definition, input, and output>
## 3.2 <Core components or algorithm>
## 3.3 <Training data, objective, and implementation>
## 3.4 <Inference, adaptation, or decisive design choice>
```

Suggested evidence chapter:

```markdown
# 4 <Main experimental evidence>
## 4.1 <Primary tasks, metrics, and comparisons>
## 4.2 <Ablations, generalization, or robustness>
## 4.3 <Cases, human evaluation, or failure modes>
```

Record parameter counts, training stages, inference settings, and resource
requirements when they affect interpretation or reproducibility.

## Dataset or benchmark

Use when the main contribution is a dataset, benchmark, evaluation suite,
leaderboard, annotation protocol, task collection, or measurement study.

Suggested construction chapter:

```markdown
# 3 <Dataset or benchmark design>
## 3.1 <Capability, task, or construct being measured>
## 3.2 <Sources, collection, filtering, scale, and splits>
## 3.3 <Annotation, quality control, and governance>
## 3.4 <Evaluation protocol, metrics, and submission rules>
```

Suggested evidence chapter:

```markdown
# 4 <Baseline and diagnostic evidence>
## 4.1 <Composition, statistics, and coverage>
## 4.2 <Baselines, human performance, and main results>
## 4.3 <Robustness, bias, contamination, and interpretation limits>
```

Do not use model-report headings unless the paper also contributes a substantive
model or training pipeline.

## System or tool

Use when the main contribution is a platform, application, agent framework,
serving design, toolkit, or operational system.

Suggested design chapter:

```markdown
# 3 <System design and workflow>
## 3.1 <Scenario, interface, and user workflow>
## 3.2 <Architecture and components>
## 3.3 <Data flow, calls, and engineering tradeoffs>
## 3.4 <Deployment, cost, reliability, and constraints>
```

Suggested evidence chapter:

```markdown
# 4 <System evaluation and cases>
## 4.1 <Primary quality and system metrics>
## 4.2 <User study or representative cases>
## 4.3 <Ablations, load tests, and failure cases>
```

Separate demonstrated system behavior from proposed architecture.

## Survey or position

Use when the contribution is a taxonomy, synthesis, conceptual framework,
position, agenda, or set of open problems.

Suggested argument chapter:

```markdown
# 3 <Taxonomy or central position>
## 3.1 <Objects, definitions, and classification>
## 3.2 <Method families or representative routes>
## 3.3 <Comparison dimensions and judgment criteria>
## 3.4 <Disagreements, gaps, and open questions>
```

Suggested evidence chapter:

```markdown
# 4 <Coverage and supporting cases>
## 4.1 <Corpus, statistics, or evidence base>
## 4.2 <Representative cases>
## 4.3 <Counterexamples and applicability limits>
```

Do not present the paper's taxonomy as an empirical law. Check corpus selection
and omitted neighboring work.

## Technical report

Use when the paper documents a model family, product release, large engineering
program, or broad capability suite without one narrow methodological novelty.

Organize chapter `3` as a narrative from design hypothesis through architecture,
data, training, post-training, and deployment. Organize chapter `4` around
concrete evidence groups such as base-model results, post-training behavior,
long-context or efficiency, code or agent tasks, multilingual coverage, and
safety evidence.

Do not create an empty safety section. Include safety or governance only when
the report provides concrete methods, evaluations, incidents, or release rules.

## Other and hybrid papers

For theory, empirical science, replication, critique, or other papers, preserve
the common chapter intent while naming chapters `3` and `4` after the actual
argument and evidence. Explain the classification in the completion report.

For a true hybrid:

- Pick the structure matching the headline contribution.
- Add a secondary subsection only when necessary to understand the claim.
- Avoid duplicating the same result across chapters.
