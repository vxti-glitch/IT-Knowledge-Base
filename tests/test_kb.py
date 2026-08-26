import json
import tempfile
import unittest
from pathlib import Path

from kb.builder import build_site
from kb.parser import discover_articles, parse_markdown_file


ARTICLE = """---
title: "Reset a test password"
author: "Tier 1 Support"
category: "How-To Guides"
last_updated: "2026-08-25"
kb_id: "HOW-TEST-001"
tags: "Windows, #Identity"
---

## Summary

Use this fictional article to verify the knowledge-base build.
"""


class ParserTests(unittest.TestCase):
    def test_article_metadata_is_normalized(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            article_path = Path(temp_dir) / "reset-test-password.md"
            article_path.write_text(ARTICLE, encoding="utf-8")

            article = parse_markdown_file(article_path)

            self.assertIsNotNone(article)
            self.assertEqual(article["slug"], "reset-test-password")
            self.assertEqual(article["tags"], ["Windows", "Identity"])
            self.assertEqual(article["last_updated"], "August 25, 2026")
            self.assertIn("fictional article", article["plain_text"])

    def test_missing_required_category_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            article_path = Path(temp_dir) / "invalid.md"
            article_path.write_text(
                "---\ntitle: Invalid article\n---\n\nNo category.\n",
                encoding="utf-8",
            )

            self.assertIsNone(parse_markdown_file(article_path))


class BuildTests(unittest.TestCase):
    def test_build_creates_searchable_static_site(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            docs_dir = root / "docs"
            output_dir = root / "output"
            docs_dir.mkdir()
            (docs_dir / "reset-test-password.md").write_text(
                ARTICLE, encoding="utf-8"
            )

            build_site(docs_dir, output_dir)

            self.assertTrue((output_dir / "index.html").is_file())
            self.assertTrue((output_dir / "reset-test-password.html").is_file())
            search_index = json.loads(
                (output_dir / "search-index.json").read_text(encoding="utf-8")
            )
            self.assertEqual(len(search_index), 1)
            self.assertEqual(search_index[0]["kb_id"], "HOW-TEST-001")
            self.assertEqual(search_index[0]["url"], "reset-test-password.html")

    def test_discovery_sorts_articles_by_title(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_dir = Path(temp_dir)
            for name, title in (("z.md", "Zulu"), ("a.md", "Alpha")):
                (docs_dir / name).write_text(
                    ARTICLE.replace("Reset a test password", title),
                    encoding="utf-8",
                )

            articles = discover_articles(docs_dir)

            self.assertEqual([article["title"] for article in articles], ["Alpha", "Zulu"])

    def test_duplicate_filenames_receive_unique_category_slugs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_dir = Path(temp_dir)
            faq_dir = docs_dir / "faq"
            how_to_dir = docs_dir / "how-to"
            faq_dir.mkdir()
            how_to_dir.mkdir()
            (faq_dir / "account-help.md").write_text(
                ARTICLE.replace("How-To Guides", "FAQ"), encoding="utf-8"
            )
            (how_to_dir / "account-help.md").write_text(ARTICLE, encoding="utf-8")

            articles = discover_articles(docs_dir)

            self.assertEqual(
                {article["slug"] for article in articles},
                {"faq-account-help", "how-to-account-help"},
            )


if __name__ == "__main__":
    unittest.main()
