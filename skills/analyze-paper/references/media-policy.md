# Media Policy

## Contents

- Modes
- Selection
- Licensing and provenance
- Extraction
- Target behavior
- Verification

## Modes

Use the explicit request first, then `[media].mode` from configuration.

- `markers` is the default. Keep the exact figure or table label followed by
  finished analysis, but do not extract or upload media.
- `extract` selects, extracts, and publishes eligible key visuals.
- `off` omits standalone visual blocks. Important visual evidence may still be
  analyzed in prose.

Do not ask for confirmation when the mode is already explicit. When markers
would materially limit the requested deliverable, mention that `extract` is
available in the completion report rather than interrupting the analysis.

## Selection

For `extract`, choose three to six visuals by default and never exceed the
configured `max_items`.

Prefer:

1. The central architecture, pipeline, construction, or taxonomy figure.
2. The decisive main-results table or plot.
3. A key ablation, robustness, or intervention result.
4. A representative qualitative case or dataset example.
5. A scale, efficiency, release, or system result when central to the claim.

Do not extract decorative figures, redundant leaderboard tables, or visuals
that cannot be read at note width.

## Licensing and provenance

Automatic extraction is allowed only when the paper or asset has an open
license, the user supplied the material, or the user explicitly approved its
reuse. Otherwise fall back to markers.

Record for each extracted asset:

- Stable local filename.
- Formal figure or table label.
- Paper title and canonical source.
- Page number when known.
- License or approval basis.
- A concise caption.

For committed public golden fixtures, also record a SHA-256 digest so CI can
detect accidental replacement or corruption. A normal user note does not need
to expose a digest unless reproducible asset tracking is useful.

Never treat access to a PDF as proof of reuse permission. Do not remove
watermarks or attribution.

## Extraction

Prefer author-provided source assets when they correspond unambiguously to the
formal label. For PDF-only papers, crop from a rendered page at readable
resolution and verify the crop against the caption and surrounding text.

Use stable lowercase filenames such as `figure-1.png` or `table-a-2.png`. Keep
example assets reasonably compressed and avoid committing a full paper PDF.

If extraction is ambiguous, mislabeled, unreadable, or technically
unavailable, retain the marker and report the fallback. Never guess the
figure-to-file mapping.

## Target behavior

- Markdown uses stable relative asset paths and visible captions.
- Notion uploads or imports media, inserts it immediately before its label and
  analysis, and does not retain expiring signed URLs in local artifacts.
- Lark uploads media through the available document capability, inserts it at
  the same evidence location, and preserves the formal label in the following
  analysis.

When a shared fixture references a repository asset, use a stable public URL
or a documented media placeholder that must be resolved before publishing.

## Verification

Read the final target back and confirm:

- Extracted and uploaded counts match the manifest.
- Every media block is adjacent to the correct label and analysis.
- Labels match the paper and are not duplicated.
- Captions and attribution remain present.
- No expiring signed URL, upload token, local absolute path, or private target
  ID appears in a public artifact.
