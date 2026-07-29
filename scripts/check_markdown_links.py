#!/usr/bin/env python3
"""Check local Markdown links in the repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    missing: list[str] = []
    for markdown in ROOT.rglob("*.md"):
        if ".git" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or "://" in target or target.startswith(("mailto:", "#")):
                continue
            path = (markdown.parent / unquote(target)).resolve()
            if not path.exists():
                missing.append(f"{markdown.relative_to(ROOT)} -> {raw_target}")

    if missing:
        for item in missing:
            print(f"Missing link target: {item}", file=sys.stderr)
        return 1

    print("All local Markdown links resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
