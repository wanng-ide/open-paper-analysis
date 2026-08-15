#!/usr/bin/env python3
"""Reject private identifiers and secret-shaped values in public text files."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEXT_SUFFIXES = {
    "",
    ".md",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".xml",
    ".py",
    ".sh",
}
PATTERN_DEFINITION_FILES = {
    Path("scripts/check_public_artifacts.py"),
    Path("skills/analyze-paper/scripts/validate_note.py"),
}
PATTERNS = {
    "email address": r"(?i)\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b",
    "private local path": r"(?:/Users|/home|/data)/[^/\s]+/(?:[^\s<]+)",
    "private Notion page URL": r"https?://(?:www\.)?(?:notion\.so|app\.notion\.com)/",
    "private Lark document URL": r"https?://[^/\s]*(?:feishu|larksuite)\.(?:cn|com)/(?:docx|wiki)/",
    "signed media URL": r"(?:X-Amz-Signature|X-Goog-Signature|Signature=|Expires=\d{6,})",
    "opaque private page id": r"\b[0-9a-f]{32}\b",
    "credential-shaped assignment": (
        r"(?i)(?:api[_-]?key|access[_-]?token|oauth[_-]?token|client[_-]?secret|"
        r"app[_-]?secret|password)\s*[:=]\s*[\"']?[A-Za-z0-9_./+\-=]{12,}"
    ),
}


def public_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.relative_to(ROOT) in PATTERN_DEFINITION_FILES:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return files


def main() -> int:
    findings: list[str] = []
    for path in public_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in PATTERNS.items():
            if re.search(pattern, text):
                findings.append(f"{path.relative_to(ROOT)}: {label}")

    if findings:
        for finding in findings:
            print(f"ERROR: {finding}", file=sys.stderr)
        return 1
    print(f"Public artifact scan passed ({len(public_text_files())} text files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
