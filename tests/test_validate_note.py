from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VALIDATOR_PATH = ROOT / "skills" / "analyze-paper" / "scripts" / "validate_note.py"
SPEC = importlib.util.spec_from_file_location("validate_note", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateNoteTests(unittest.TestCase):
    def fixture(self, name: str) -> str:
        return (ROOT / "examples" / "deepseekmoe" / name).read_text(encoding="utf-8")

    def test_all_golden_targets_are_valid(self) -> None:
        for name, target in (
            ("markdown.md", "markdown"),
            ("notion.md", "notion"),
            ("lark.xml", "lark"),
        ):
            with self.subTest(target=target):
                self.assertEqual(VALIDATOR.validate(self.fixture(name), target, 5), [])

    def test_markdown_rejects_notion_markup(self) -> None:
        text = self.fixture("markdown.md") + "\n<table_of_contents/>\n"
        errors = VALIDATOR.validate(text, "markdown", 5)
        self.assertTrue(any("platform-specific" in error for error in errors))

    def test_notion_rejects_private_page_url(self) -> None:
        private_url = "https://" + "app." + "notion.com/p/private"
        text = self.fixture("notion.md") + f"\n{private_url}\n"
        errors = VALIDATOR.validate(text, "notion", 5)
        self.assertTrue(any("private Notion" in error for error in errors))

    def test_lark_rejects_malformed_xml(self) -> None:
        errors = VALIDATOR.validate("<title>broken", "lark", 0)
        self.assertTrue(any("invalid Lark XML" in error for error in errors))

    def test_lark_rejects_unknown_tags(self) -> None:
        text = self.fixture("lark.xml") + "<unsupported>value</unsupported>"
        errors = VALIDATOR.validate(text, "lark", 5)
        self.assertTrue(any("unsupported Lark XML tags" in error for error in errors))

    def test_duplicate_evidence_is_rejected(self) -> None:
        text = self.fixture("markdown.md").replace(
            "> [Figure 5]", "> [Figure 4]", 1
        )
        errors = VALIDATOR.validate(text, "markdown", 5)
        self.assertTrue(any("duplicate figure/table" in error for error in errors))

    def test_long_chinese_contribution_tag_is_rejected(self) -> None:
        text = self.fixture("markdown.md").replace(
            '  - "细粒专家"', '  - "在等计算约束下拆分专家"', 1
        )
        errors = VALIDATOR.validate(text, "markdown", 5)
        self.assertTrue(any("Han characters" in error for error in errors))

    def test_long_english_contribution_tag_is_rejected(self) -> None:
        text = self.fixture("markdown.md").replace(
            '  - "细粒专家"',
            '  - "segmentation under equal compute and parameters"',
            1,
        )
        errors = VALIDATOR.validate(text, "markdown", 5)
        self.assertTrue(any("words" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
