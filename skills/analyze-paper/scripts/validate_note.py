#!/usr/bin/env python3
"""Validate the portable structure of an analyze-paper Markdown note."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_METADATA = (
    "title",
    "authors",
    "paper_url",
    "published",
    "venue",
    "paper_type",
    "topics",
    "contributions",
    "status",
    "sources",
)

FORBIDDEN_PATTERNS = {
    "generic figure label": r"\bFigure X\b",
    "generic table label": r"\bTable X\b",
    "TODO marker": r"\bTODO\b",
    "placeholder text": r"\bplaceholder\b",
    "placement instruction": r"\bput (?:this|the) (?:figure|table) here\b",
    "Chinese placeholder text": r"占位",
    "legacy-page process text": r"旧页面",
    "editing record": r"编辑记录|修改记录|本次修改",
}

CALLOUT_RE = re.compile(
    r"^> \[((?:Appendix )?(?:Figure|Table) [A-Za-z0-9][A-Za-z0-9.\-]*)\]\s*$",
    re.MULTILINE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("note", type=Path)
    parser.add_argument(
        "--min-callouts",
        type=int,
        default=5,
        help="minimum numbered figure/table callouts (default: 5)",
    )
    return parser.parse_args()


def frontmatter(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return text[4:end]


def validate(text: str, min_callouts: int) -> list[str]:
    errors: list[str] = []
    metadata = frontmatter(text)
    if metadata is None:
        errors.append("missing or unclosed YAML frontmatter")
    else:
        for key in REQUIRED_METADATA:
            if not re.search(rf"^{re.escape(key)}:", metadata, re.MULTILINE):
                errors.append(f"missing metadata key: {key}")

    if not re.search(r"^# (?:Sources|参考|来源)\b", text, re.MULTILINE):
        errors.append("missing Sources heading")

    for chapter in range(9):
        if not re.search(rf"^# {chapter}(?:\s|$)", text, re.MULTILINE):
            errors.append(f"missing chapter heading: {chapter}")

    callouts = list(CALLOUT_RE.finditer(text))
    labels = [match.group(1) for match in callouts]
    if len(set(labels)) != len(labels):
        errors.append("duplicate figure/table callout labels")
    if len(callouts) < min_callouts:
        errors.append(
            f"found {len(callouts)} figure/table callouts; expected at least "
            f"{min_callouts}"
        )

    for index, match in enumerate(callouts):
        next_start = callouts[index + 1].start() if index + 1 < len(callouts) else len(text)
        following = text[match.end():next_start].strip()
        first_block = following.split("\n\n", 1)[0].strip()
        if len(first_block) < 40 or first_block.startswith("#"):
            errors.append(f"callout lacks immediate analysis: {match.group(1)}")

    for label, pattern in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            errors.append(f"forbidden process text: {label}")

    return errors


def main() -> int:
    args = parse_args()
    if args.min_callouts < 0:
        print("--min-callouts must be non-negative", file=sys.stderr)
        return 2
    try:
        text = args.note.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"cannot read {args.note}: {exc}", file=sys.stderr)
        return 2

    errors = validate(text, args.min_callouts)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    callout_count = len(CALLOUT_RE.findall(text))
    print(f"Valid paper note: {args.note} ({callout_count} callouts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
