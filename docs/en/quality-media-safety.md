# Quality, Media, and Safety

[English](../en/quality-media-safety.md) | [简体中文](../zh-CN/quality-media-safety.md)

## Deep means evidence-complete

Every completed note uses the deep profile. This does not impose a word count:
it asks the agent to exhaust useful primary evidence without padding a short
paper or inventing missing detail.

- Chapter `0` normally contains three to five dense paragraphs.
- Chapters `1` and `2` explain the problem, artifact, evidence, prior line,
  direct alternatives, and precise positioning.
- Paper-specific chapters `3` and `4` normally contain three to six
  substantive subsections when evidence supports them.
- Core subsections usually explain both mechanism/setup and
  interpretation/boundary.
- Chapters `5`, `6`, and `7` must not collapse into generic conclusions.
- Chapter `8` annotates versions, releases, replications, and follow-up work.

Paper type still controls the content. A benchmark note emphasizes
construction, contamination, protocols, baselines, and validity rather than
imitating a model architecture report.

## Evidence anchors

For each useful numbered Figure or Table, record:

- Exact formal label and a faithful caption.
- Source page or stable source URL.
- The claim it supports.
- Immediate interpretation and the boundary of that interpretation.
- Optional stable media plus license or approval basis.

A substantial paper normally retains five to eight useful anchors. Fewer are
correct when the paper contains fewer meaningful visuals.

## Media modes

`markers` is the default. It gives accurate evidence navigation without
copying media.

`extract` selects three to six central visuals by default, such as the core
architecture, decisive result, key ablation, representative case, or important
efficiency result. Every crop is checked against its formal number, caption,
and surrounding text.

`off` removes standalone visual blocks, not the obligation to explain
important evidence.

## Permission and provenance

Access to a PDF is not reuse permission. Automatic extraction requires an open
license, user-provided material, or explicit approval. Otherwise the run falls
back to markers.

Never remove attribution or watermarks. Never commit the full paper merely to
support an example. Repository assets use stable filenames and a media manifest
with source, page, purpose, and license.

## Privacy and secrets

Public artifacts must not contain:

- API keys, OAuth tokens, cookies, client secrets, or credential files.
- Private database, page, document, user, tenant, or upload identifiers.
- Signed or short-lived media URLs.
- Local absolute paths, private property schemas, or personal defaults.

CI runs Gitleaks over Git history, configuration checks, fixture-specific
secret patterns, XML parsing, and link validation. Real-platform smoke-test
reports redact URLs and identifiers, and temporary documents are removed after
read-back and screenshot capture.
