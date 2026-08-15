#!/usr/bin/env python3
"""Validate an analyze-paper Markdown, Notion, or Lark artifact."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


REQUIRED_METADATA = (
    "title",
    "institutions",
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
    "placeholder text": r"\bplaceholder\b|占位",
    "placement instruction": r"\bput (?:this|the) (?:figure|table) here\b",
    "editing process text": r"旧页面|编辑记录|修改记录|本次修改",
    "local path": r"(?:/Users/|/home/|/data/)[^\s<]+",
    "private Notion page URL": r"https?://(?:www\.)?(?:notion\.so|app\.notion\.com)/",
    "private Lark document URL": r"https?://[^/\s]*(?:feishu|larksuite)\.(?:cn|com)/(?:docx|wiki)/",
    "signed media URL": r"(?:X-Amz-Signature|X-Goog-Signature|Signature=|Expires=\d{6,})",
    "credential-shaped assignment": (
        r"(?:api[_-]?key|access[_-]?token|oauth[_-]?token|client[_-]?secret)"
        r"\s*[:=]\s*[\"']?[A-Za-z0-9_./+\-=]{12,}"
    ),
    "opaque private page id": r"\b[0-9a-f]{32}\b",
}

LABEL = r"(?:Appendix )?(?:Figure|Table) [A-Za-z0-9][A-Za-z0-9.\-]*"
MARKDOWN_MEDIA_RE = re.compile(
    rf"^(?:!\[(?P<image>{LABEL})(?::[^\]]*)?\]\([^\n]+\)|"
    rf"> \[(?P<marker>{LABEL})\])\s*$",
    re.MULTILINE,
)
HAN_CHARACTER_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
SPACE_DELIMITED_WORD_RE = re.compile(
    r"[A-Za-z0-9]+(?:[-/][A-Za-z0-9]+)*"
)
SENTENCE_PUNCTUATION_RE = re.compile(r"[,.;:!?，。；：！？]")
LARK_ALLOWED_TAGS = {
    "document",
    "title",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    "h1",
    "h2",
    "h3",
    "p",
    "ul",
    "ol",
    "li",
    "blockquote",
    "pre",
    "code",
    "img",
    "b",
    "em",
    "u",
    "del",
    "a",
    "br",
    "span",
    "latex",
    "hr",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("note", type=Path)
    parser.add_argument(
        "--format",
        choices=("auto", "markdown", "notion", "lark"),
        default="auto",
        help="artifact format; inferred from the path by default",
    )
    parser.add_argument(
        "--min-evidence",
        "--min-callouts",
        dest="min_evidence",
        type=int,
        default=5,
        help="minimum numbered figure/table evidence anchors (default: 5)",
    )
    return parser.parse_args()


def infer_format(path: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    if path.suffix.lower() == ".xml":
        return "lark"
    if "notion" in path.name.lower():
        return "notion"
    return "markdown"


def frontmatter(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return text[4:end]


def yaml_block_list(metadata: str, key: str) -> list[str] | None:
    match = re.search(
        rf"^{re.escape(key)}:\s*\n(?P<body>(?:  - .+\n?)+)",
        metadata,
        re.MULTILINE,
    )
    if not match:
        return None
    return [
        line.removeprefix("  - ").strip().strip("\"'")
        for line in match.group("body").splitlines()
    ]


def validate_contribution_tags(metadata: str) -> list[str]:
    values = yaml_block_list(metadata, "contributions")
    if values is None:
        return ["contributions must be a YAML block list of compact tags"]

    errors: list[str] = []
    if not 1 <= len(values) <= 4:
        errors.append(
            f"contributions contains {len(values)} tags; expected 1-4"
        )

    for value in values:
        if not value:
            errors.append("contribution tags must not be empty")
            continue
        if SENTENCE_PUNCTUATION_RE.search(value):
            errors.append(
                f"contribution tag uses sentence punctuation: {value!r}"
            )
        han_count = len(HAN_CHARACTER_RE.findall(value))
        if han_count > 4:
            errors.append(
                f"Chinese contribution tag has {han_count} Han characters; "
                f"expected at most 4: {value!r}"
            )
        elif han_count == 0:
            word_count = len(SPACE_DELIMITED_WORD_RE.findall(value))
            if word_count > 4:
                errors.append(
                    f"contribution tag has {word_count} words; "
                    f"expected at most 4: {value!r}"
                )
    return errors


def validate_forbidden(text: str) -> list[str]:
    errors: list[str] = []
    for label, pattern in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            errors.append(f"forbidden public content: {label}")
    return errors


def markdown_section(text: str, level: int, number: int) -> str:
    marks = "#" * level
    match = re.search(
        rf"^{marks} {number}(?:\s[^\n]*)?\n(?P<body>.*?)(?=^{marks} {number + 1}(?:\s|$)|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group("body") if match else ""


def check_deep_markdown(text: str, chapter_level: int) -> list[str]:
    errors: list[str] = []
    chapter_zero = markdown_section(text, chapter_level, 0)
    paragraphs = [
        part
        for part in re.split(r"\n\s*\n", chapter_zero)
        if part.strip() and not part.lstrip().startswith(("#", "- ", "> ", "!["))
    ]
    if not 3 <= len(paragraphs) <= 5:
        errors.append(
            f"chapter 0 has {len(paragraphs)} prose paragraphs; expected 3-5"
        )

    subsection_level = chapter_level + 1
    subsection_marks = "#" * subsection_level
    for chapter in (3, 4):
        section = markdown_section(text, chapter_level, chapter)
        count = len(
            re.findall(rf"^{subsection_marks} \d+\.\d+\s", section, re.MULTILINE)
        )
        if not 3 <= count <= 6:
            errors.append(
                f"chapter {chapter} has {count} substantive subsections; expected 3-6"
            )

    for chapter in (5, 6, 7):
        section = markdown_section(text, chapter_level, chapter)
        prose = re.sub(r"[#>*_`\[\]()\-]", "", section).strip()
        if len(prose) < 250:
            errors.append(f"chapter {chapter} is too thin for the deep profile")
    return errors


def validate_markdown_like(
    text: str, target: str, min_evidence: int
) -> list[str]:
    errors: list[str] = []
    chapter_level = 2 if target == "markdown" else 1
    marks = "#" * chapter_level

    if target == "markdown":
        metadata = frontmatter(text)
        if metadata is None:
            errors.append("missing or unclosed YAML frontmatter")
        else:
            for key in REQUIRED_METADATA:
                if not re.search(rf"^{re.escape(key)}:", metadata, re.MULTILINE):
                    errors.append(f"missing metadata key: {key}")
            if re.search(r"^authors:", metadata, re.MULTILINE):
                errors.append("deprecated metadata key: authors; use institutions")
            errors.extend(validate_contribution_tags(metadata))
        body = text[text.find("\n---\n", 4) + 5 :] if metadata is not None else text
        if not re.search(r"^# \S", body, re.MULTILINE):
            errors.append("missing visible paper title")
        if not re.search(r"^## Contents\b", text, re.MULTILINE):
            errors.append("missing linked Contents section")
        if "<table_of_contents" in text or re.search(
            r"<(?:title|table|p|h1)>", text
        ):
            errors.append("Markdown contains platform-specific markup")
        source_pattern = r"^## (?:Sources|参考|来源)\b"
    else:
        if frontmatter(text) is not None:
            errors.append("Notion body must not contain YAML frontmatter")
        if not re.search(r"^# 目录\s*$", text, re.MULTILINE):
            errors.append("Notion body must begin with the 目录 section")
        if not re.search(
            r"^<table_of_contents(?:\s[^>]*)?/>\s*$", text, re.MULTILINE
        ):
            errors.append("missing native Notion table of contents")
        if re.search(r"<(?:title|tbody|tr|td|latex)>", text):
            errors.append("Notion body contains Lark XML")
        source_pattern = r"^# (?:参考|Sources|来源)\b"

    if not re.search(source_pattern, text, re.MULTILINE):
        errors.append("missing sources/reference heading")
    for chapter in range(9):
        if not re.search(rf"^{marks} {chapter}(?:\s|$)", text, re.MULTILINE):
            errors.append(f"missing chapter heading: {chapter}")

    matches = list(MARKDOWN_MEDIA_RE.finditer(text))
    labels = [(match.group("image") or match.group("marker")) for match in matches]
    if len(set(labels)) != len(labels):
        errors.append("duplicate figure/table evidence labels")
    if len(labels) < min_evidence:
        errors.append(
            f"found {len(labels)} figure/table evidence anchors; "
            f"expected at least {min_evidence}"
        )
    for match, label in zip(matches, labels):
        following = text[match.end() :].lstrip()
        first_block = following.split("\n\n", 1)[0].strip()
        if len(first_block) < 40 or first_block.startswith("#"):
            errors.append(f"evidence anchor lacks immediate analysis: {label}")

    errors.extend(check_deep_markdown(text, chapter_level))
    return errors


def lark_text(node: ET.Element) -> str:
    return "".join(node.itertext()).strip()


def validate_lark(text: str, min_evidence: int) -> list[str]:
    errors: list[str] = []
    try:
        root = ET.fromstring(f"<document>{text}</document>")
    except ET.ParseError as exc:
        return [f"invalid Lark XML: {exc}"]

    unknown = sorted({node.tag for node in root.iter()} - LARK_ALLOWED_TAGS)
    if unknown:
        errors.append(f"unsupported Lark XML tags: {', '.join(unknown)}")
    titles = root.findall("./title")
    if len(titles) != 1 or not lark_text(titles[0]):
        errors.append("Lark XML must contain exactly one non-empty title")
    if root.find("./table") is None:
        errors.append("Lark XML is missing the compact metadata table")

    children = list(root)
    headings = [lark_text(node) for node in children if node.tag == "h1"]
    if not any(title in headings for title in ("参考", "Sources", "来源")):
        errors.append("missing sources/reference heading")
    for chapter in range(9):
        if not any(re.match(rf"^{chapter}(?:\s|$)", title) for title in headings):
            errors.append(f"missing chapter heading: {chapter}")

    labels: list[str] = []
    evidence_indexes: list[tuple[int, str]] = []
    for index, node in enumerate(children):
        label = ""
        if node.tag == "img":
            match = re.match(rf"^({LABEL})(?::|$)", node.attrib.get("caption", ""))
            label = match.group(1) if match else ""
        elif node.tag == "blockquote":
            match = re.search(rf"\b({LABEL})\b", lark_text(node))
            label = match.group(1) if match else ""
        if label:
            labels.append(label)
            evidence_indexes.append((index, label))

    if len(set(labels)) != len(labels):
        errors.append("duplicate figure/table evidence labels")
    if len(labels) < min_evidence:
        errors.append(
            f"found {len(labels)} figure/table evidence anchors; "
            f"expected at least {min_evidence}"
        )
    for index, label in evidence_indexes:
        following = children[index + 1] if index + 1 < len(children) else None
        if (
            following is None
            or following.tag != "p"
            or len(lark_text(following)) < 40
        ):
            errors.append(f"evidence anchor lacks immediate analysis: {label}")

    for chapter in (3, 4):
        start = next(
            (
                i
                for i, node in enumerate(children)
                if node.tag == "h1" and re.match(rf"^{chapter}\s", lark_text(node))
            ),
            None,
        )
        end = next(
            (
                i
                for i, node in enumerate(children)
                if start is not None and i > start and node.tag == "h1"
            ),
            len(children),
        )
        count = (
            sum(node.tag == "h2" for node in children[start + 1 : end])
            if start is not None
            else 0
        )
        if not 3 <= count <= 6:
            errors.append(
                f"chapter {chapter} has {count} substantive subsections; expected 3-6"
            )

    zero_index = next(
        (
            i
            for i, node in enumerate(children)
            if node.tag == "h1" and re.match(r"^0\s", lark_text(node))
        ),
        None,
    )
    one_index = next(
        (
            i
            for i, node in enumerate(children)
            if node.tag == "h1" and re.match(r"^1\s", lark_text(node))
        ),
        len(children),
    )
    zero_paragraphs = (
        sum(node.tag == "p" for node in children[zero_index + 1 : one_index])
        if zero_index is not None
        else 0
    )
    if not 3 <= zero_paragraphs <= 5:
        errors.append(
            f"chapter 0 has {zero_paragraphs} prose paragraphs; expected 3-5"
        )

    if "<table_of_contents" in text or text.startswith("---\n"):
        errors.append("Lark XML contains another platform's markup")
    return errors


def validate(text: str, target: str, min_evidence: int) -> list[str]:
    errors = validate_forbidden(text)
    if target in {"markdown", "notion"}:
        errors.extend(validate_markdown_like(text, target, min_evidence))
    else:
        errors.extend(validate_lark(text, min_evidence))
    return errors


def main() -> int:
    args = parse_args()
    if args.min_evidence < 0:
        print("--min-evidence must be non-negative", file=sys.stderr)
        return 2
    target = infer_format(args.note, args.format)
    try:
        text = args.note.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"cannot read {args.note}: {exc}", file=sys.stderr)
        return 2

    errors = validate(text, target, args.min_evidence)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if target == "lark":
        root = ET.fromstring(f"<document>{text}</document>")
        count = sum(
            node.tag in {"img", "blockquote"}
            and bool(
                re.search(LABEL, node.attrib.get("caption", "") + lark_text(node))
            )
            for node in list(root)
        )
    else:
        count = len(MARKDOWN_MEDIA_RE.findall(text))
    print(
        f"Valid {target} paper note: {args.note} "
        f"({count} evidence anchors)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
