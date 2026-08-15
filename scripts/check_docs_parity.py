#!/usr/bin/env python3
"""Check bilingual documentation parity and language navigation."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
LANGUAGES = ("en", "zh-CN")


def markdown_files(language: str) -> set[Path]:
    base = DOCS / language
    return {path.relative_to(base) for path in base.rglob("*.md")}


def main() -> int:
    errors: list[str] = []
    collections = {language: markdown_files(language) for language in LANGUAGES}
    if collections["en"] != collections["zh-CN"]:
        only_en = sorted(collections["en"] - collections["zh-CN"])
        only_zh = sorted(collections["zh-CN"] - collections["en"])
        if only_en:
            errors.append(f"English-only docs: {', '.join(map(str, only_en))}")
        if only_zh:
            errors.append(f"Chinese-only docs: {', '.join(map(str, only_zh))}")

    for relative in sorted(collections["en"] & collections["zh-CN"]):
        for language in LANGUAGES:
            path = DOCS / language / relative
            text = path.read_text(encoding="utf-8")
            if not re.search(r"^# \S", text, re.MULTILINE):
                errors.append(f"{path.relative_to(ROOT)} has no H1")
            en_target = f"../en/{relative.as_posix()}"
            zh_target = f"../zh-CN/{relative.as_posix()}"
            if f"[English]({en_target})" not in text:
                errors.append(f"{path.relative_to(ROOT)} lacks English navigation")
            if f"[简体中文]({zh_target})" not in text:
                errors.append(f"{path.relative_to(ROOT)} lacks Chinese navigation")

    root_readmes = {
        "en": ROOT / "README.md",
        "zh-CN": ROOT / "README.zh-CN.md",
    }
    for language, path in root_readmes.items():
        if not path.exists():
            errors.append(f"missing root {language} README: {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        if not re.search(r"^# Open Paper Analysis$", text, re.MULTILINE):
            errors.append(f"{path.name} has no project H1")
        for target in ("README.md", "README.zh-CN.md"):
            if f"]({target})" not in text:
                errors.append(f"{path.name} does not link {target}")
        docs_target = f"docs/{language}/README.md"
        if docs_target not in text:
            errors.append(f"{path.name} does not link {docs_target}")

    if all(path.exists() for path in root_readmes.values()):
        heading_counts = {
            language: len(
                re.findall(
                    r"^## [^#].*$",
                    path.read_text(encoding="utf-8"),
                    re.MULTILINE,
                )
            )
            for language, path in root_readmes.items()
        }
        if heading_counts["en"] != heading_counts["zh-CN"]:
            errors.append(
                "root README section counts differ: "
                f"English={heading_counts['en']}, "
                f"Chinese={heading_counts['zh-CN']}"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "Bilingual docs are mirrored: "
        f"{len(collections['en'])} files per language"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
