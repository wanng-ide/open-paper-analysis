#!/usr/bin/env python3
"""Validate the shared DeepSeekMoE manuscript across all golden targets."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "deepseekmoe"
MARKDOWN = EXAMPLE / "markdown.md"
NOTION = EXAMPLE / "notion.md"
NOTION_PROPERTIES = EXAMPLE / "notion-properties.json"
LARK = EXAMPLE / "lark.xml"
MEDIA = EXAMPLE / "media.yaml"
LABEL = r"(?:Appendix )?(?:Figure|Table) [A-Za-z0-9][A-Za-z0-9.\-]*"
HAN_CHARACTER_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
SPACE_DELIMITED_WORD_RE = re.compile(
    r"[A-Za-z0-9]+(?:[-/][A-Za-z0-9]+)*"
)
SENTENCE_PUNCTUATION_RE = re.compile(r"[,.;:!?，。；：！？]")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def frontmatter(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("Markdown fixture has no frontmatter")
    return match.group(1)


def yaml_scalar(source: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*[\"']?(.+?)[\"']?\s*$", source, re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip("\"'")


def yaml_list(source: str, key: str) -> list[str]:
    match = re.search(
        rf"^{re.escape(key)}:\s*\n(?P<body>(?:  - .+\n?)+)",
        source,
        re.MULTILINE,
    )
    if not match:
        return []
    return [
        line.removeprefix("  - ").strip().strip("\"'")
        for line in match.group("body").splitlines()
    ]


def markdown_headings(text: str, level: int, numbered_only: bool = False) -> list[str]:
    marks = "#" * level
    headings = re.findall(rf"^{marks} (.+)$", text, re.MULTILINE)
    if numbered_only:
        headings = [heading for heading in headings if re.match(r"^\d+(?:\.\d+)?\s", heading)]
    return headings


def markdown_sources(text: str, heading: str, level: int) -> list[str]:
    marks = "#" * level
    match = re.search(
        rf"^{marks} {heading}\s*\n(?P<body>.*?)(?=^{marks} 0\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return []
    return re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", match.group("body"))


def markdown_evidence(text: str) -> list[str]:
    pattern = re.compile(
        rf"^(?:!\[(?P<image>{LABEL})(?::[^\]]*)?\]\([^\n]+\)|"
        rf"> \[(?P<marker>{LABEL})\])\s*$",
        re.MULTILINE,
    )
    return [match.group("image") or match.group("marker") for match in pattern.finditer(text)]


def lark_document(text: str) -> ET.Element:
    return ET.fromstring(f"<document>{text}</document>")


def node_text(node: ET.Element) -> str:
    return "".join(node.itertext()).strip()


def lark_sources(root: ET.Element) -> list[str]:
    collecting = False
    urls: list[str] = []
    for node in list(root):
        if node.tag == "h1":
            if node_text(node) == "参考":
                collecting = True
                continue
            if collecting:
                break
        if collecting:
            urls.extend(link.attrib["href"] for link in node.iter("a") if "href" in link.attrib)
    return urls


def lark_evidence(root: ET.Element) -> list[str]:
    labels: list[str] = []
    for node in list(root):
        value = node.attrib.get("caption", "") if node.tag == "img" else node_text(node)
        if node.tag not in {"img", "blockquote"}:
            continue
        match = re.search(rf"\b({LABEL})\b", value)
        if match:
            labels.append(match.group(1))
    return labels


def lark_metadata(root: ET.Element) -> dict[str, str]:
    values: dict[str, str] = {}
    table = root.find("./table")
    if table is None:
        return values
    for row in table.iter("tr"):
        cells = list(row)
        if len(cells) == 2:
            values[node_text(cells[0])] = node_text(cells[1])
    return values


def main() -> int:
    errors: list[str] = []
    markdown = MARKDOWN.read_text(encoding="utf-8")
    notion = NOTION.read_text(encoding="utf-8")
    lark = LARK.read_text(encoding="utf-8")
    properties = json.loads(NOTION_PROPERTIES.read_text(encoding="utf-8"))
    metadata = frontmatter(markdown)
    lark_root = lark_document(lark)

    scalar_keys = (
        "title",
        "paper_url",
        "pdf_url",
        "arxiv_url",
        "doi",
        "published",
        "preprint_date",
        "venue",
        "paper_type",
        "code_url",
        "status",
    )
    for key in scalar_keys:
        actual = yaml_scalar(metadata, key)
        if properties.get(key) != actual:
            fail(errors, f"Notion property mismatch for {key}")
    for key in ("institutions", "topics", "contributions"):
        if properties.get(key) != yaml_list(metadata, key):
            fail(errors, f"Notion property mismatch for {key}")

    contribution_tags = yaml_list(metadata, "contributions")
    if not 1 <= len(contribution_tags) <= 4:
        fail(errors, "golden example must contain 1-4 contribution tags")
    for tag in contribution_tags:
        han_count = len(HAN_CHARACTER_RE.findall(tag))
        word_count = len(SPACE_DELIMITED_WORD_RE.findall(tag))
        if SENTENCE_PUNCTUATION_RE.search(tag):
            fail(errors, f"contribution tag contains sentence punctuation: {tag}")
        if han_count > 4 or (han_count == 0 and word_count > 4):
            fail(errors, f"contribution tag is not compact: {tag}")

    lark_title = node_text(lark_root.find("./title"))  # type: ignore[arg-type]
    if lark_title != properties["title"]:
        fail(errors, "Lark title does not match canonical title")
    lark_meta = lark_metadata(lark_root)
    expected_lark = {
        "机构": "；".join(properties["institutions"]),
        "正式发表": f'{properties["published"]}（ACL 2024）',
        "首次公开": f'{properties["preprint_date"]}（arXiv v1）',
        "Venue": properties["venue"],
        "论文类型": properties["paper_type"],
        "主题": "；".join(properties["topics"]),
        "贡献": "；".join(properties["contributions"]),
    }
    for key, value in expected_lark.items():
        if lark_meta.get(key) != value:
            fail(errors, f"Lark metadata mismatch for {key}")

    lark_metadata_links = {
        link.attrib["href"]
        for link in lark_root.findall("./table//a")
        if "href" in link.attrib
    }
    expected_metadata_links = {
        properties["paper_url"],
        properties["pdf_url"],
        properties["arxiv_url"],
        f'https://doi.org/{properties["doi"]}',
        properties["code_url"],
    }
    if lark_metadata_links != expected_metadata_links:
        fail(errors, "Lark metadata links do not match canonical links")

    markdown_chapters = markdown_headings(markdown, 2, numbered_only=True)
    notion_chapters = markdown_headings(notion, 1, numbered_only=True)
    lark_chapters = [
        node_text(node)
        for node in lark_root.findall("./h1")
        if re.match(r"^\d+\s", node_text(node))
    ]
    if not (markdown_chapters == notion_chapters == lark_chapters):
        fail(errors, "chapter headings differ across targets")

    markdown_subsections = markdown_headings(markdown, 3, numbered_only=True)
    notion_subsections = markdown_headings(notion, 2, numbered_only=True)
    lark_subsections = [
        node_text(node)
        for node in lark_root.findall("./h2")
        if re.match(r"^\d+\.\d+\s", node_text(node))
    ]
    if not (markdown_subsections == notion_subsections == lark_subsections):
        fail(errors, "subsection headings differ across targets")

    markdown_urls = markdown_sources(markdown, "Sources", 2)
    notion_urls = markdown_sources(notion, "参考", 1)
    lark_urls = lark_sources(lark_root)
    if not (markdown_urls == notion_urls == lark_urls):
        fail(errors, "reference URLs differ across targets")

    markdown_labels = markdown_evidence(markdown)
    notion_labels = markdown_evidence(notion)
    lark_labels = lark_evidence(lark_root)
    if not (markdown_labels == notion_labels == lark_labels):
        fail(errors, "figure/table labels differ across targets")

    if "$$" not in notion or "\\(" in notion or "\\[" in notion:
        fail(errors, "Notion fixture does not use native enhanced-Markdown math")
    if "<latex>" not in lark:
        fail(errors, "Lark fixture does not use native latex blocks")
    if "\\[" not in markdown:
        fail(errors, "portable Markdown fixture is missing block math")

    manifest = MEDIA.read_text(encoding="utf-8")
    manifest_files = re.findall(
        r"^[ \t]+file: (assets/[^\s]+)$", manifest, re.MULTILINE
    )
    manifest_labels = re.findall(
        r"^[ \t]+(?:- )?label: ((?:Figure|Table) [^\n]+)$",
        manifest,
        re.MULTILINE,
    )
    manifest_hashes = re.findall(
        r"^[ \t]+sha256: ([0-9a-f]{64})$", manifest, re.MULTILINE
    )
    if len(manifest_hashes) != len(manifest_files):
        fail(errors, "every extracted media file must have one SHA-256 digest")
    for index, relative in enumerate(manifest_files):
        asset = EXAMPLE / relative
        if not asset.is_file():
            fail(errors, f"media manifest references missing file: {relative}")
        elif index < len(manifest_hashes):
            actual_hash = hashlib.sha256(asset.read_bytes()).hexdigest()
            if actual_hash != manifest_hashes[index]:
                fail(errors, f"media digest mismatch: {relative}")
        raw_url = (
            "https://raw.githubusercontent.com/wanng-ide/open-paper-analysis/"
            f"main/examples/deepseekmoe/{relative}"
        )
        if raw_url not in notion or raw_url not in lark:
            fail(errors, f"extracted media is not rendered in both platform fixtures: {relative}")
    if len(manifest_labels) != len(set(manifest_labels)):
        fail(errors, "media manifest contains duplicate labels")
    if set(manifest_labels) != set(markdown_labels):
        fail(errors, "media manifest labels do not match rendered evidence")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "Golden examples agree: "
        f"{len(markdown_chapters)} chapters, "
        f"{len(markdown_urls)} sources, "
        f"{len(markdown_labels)} evidence anchors"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
