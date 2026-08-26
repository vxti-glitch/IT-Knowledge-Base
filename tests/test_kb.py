import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from kb.builder import build_site
from kb.parser import ArticleValidationError, discover_articles, parse_markdown_file


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_BODY = """
## Summary

This fictional test article validates the published content workflow and contains enough specific detail to pass the minimum quality gate without representing a production environment.

## Scope and safety

Use only the fictional lab target and preserve the starting state before any approved change. Do not record credentials or secrets.

## Symptoms or trigger

- A fictional user reports a repeatable test condition.

## Information to collect

- Test username, device, exact error, timestamp, and business impact.

## Diagnostic steps

Capture the current state, reproduce the condition once, and record the result before making a change.

## Resolution or next action

Apply one reversible fictional correction and record the expected outcome.

## Validation

Repeat the original task and confirm the documented result with the fictional user.

## Ticket note example

> Simulated ticket note: Reproduced the lab condition, applied one approved test correction, and verified the expected result.

## Escalation criteria

Escalate when the condition affects multiple fictional users, requires privileged access, or remains after the Tier 1 boundary.

## References

- [Microsoft Learn](https://learn.microsoft.com/)
"""


def article_text(
    kb_id="KB-WINDOWS-999", category="Windows Endpoint", title="Test article"
):
    return f"""---
title: "{title}"
author: "Tier 1 Support Lab"
category: "{category}"
article_type: "How-To"
last_updated: "2026-08-26"
kb_id: "{kb_id}"
tags: ["Windows 11", "Troubleshooting"]
platforms: ["Windows 11"]
support_tier: "Tier 1"
risk: "Low"
---
{REQUIRED_BODY}
"""


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and attributes.get("href"):
            self.targets.append(attributes["href"])
        if tag in {"link", "script"}:
            target = attributes.get("href") or attributes.get("src")
            if target:
                self.targets.append(target)


class ParserTests(unittest.TestCase):
    def test_article_metadata_and_tags_are_normalized(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs = Path(temp_dir)
            folder = docs / "windows-endpoint"
            folder.mkdir()
            path = folder / "test.md"
            path.write_text(
                article_text().replace(
                    'tags: ["Windows 11", "Troubleshooting"]',
                    'tags: ["Windows 11", "WiFi", "wi-fi", "Troubleshooting"]',
                ),
                encoding="utf-8",
            )

            article = parse_markdown_file(path, docs)

            self.assertEqual(article["slug"], "test")
            self.assertEqual(
                article["tags"], ["Windows 11", "Wi-Fi", "Troubleshooting"]
            )
            self.assertEqual(article["last_updated_display"], "August 26, 2026")
            self.assertIn("fictional test article", article["plain_text"].lower())

    def test_missing_required_metadata_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs = Path(temp_dir)
            folder = docs / "windows-endpoint"
            folder.mkdir()
            path = folder / "test.md"
            path.write_text(
                article_text().replace('risk: "Low"\n', ""), encoding="utf-8"
            )

            with self.assertRaisesRegex(
                ArticleValidationError, "missing required field 'risk'"
            ):
                parse_markdown_file(path, docs)

    def test_folder_must_match_category(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs = Path(temp_dir)
            folder = docs / "printing"
            folder.mkdir()
            path = folder / "test.md"
            path.write_text(article_text(), encoding="utf-8")

            with self.assertRaisesRegex(
                ArticleValidationError, "folder does not match category"
            ):
                parse_markdown_file(path, docs)

    def test_placeholder_content_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs = Path(temp_dir)
            folder = docs / "windows-endpoint"
            folder.mkdir()
            path = folder / "test.md"
            path.write_text(
                article_text().replace(
                    "Capture the current state",
                    "A General Issue issue occurred. Capture the current state",
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ArticleValidationError, "banned placeholder phrase"
            ):
                parse_markdown_file(path, docs)

    def test_duplicate_kb_ids_and_bodies_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs = Path(temp_dir)
            folder = docs / "windows-endpoint"
            folder.mkdir()
            (folder / "one.md").write_text(article_text(title="One"), encoding="utf-8")
            (folder / "two.md").write_text(article_text(title="Two"), encoding="utf-8")

            with self.assertRaises(ArticleValidationError) as context:
                discover_articles(docs)

            message = str(context.exception)
            self.assertIn("Duplicate KB ID", message)
            self.assertIn("Duplicate article body", message)


class RepositoryQualityTests(unittest.TestCase):
    def test_complete_published_library_passes_quality_gate(self):
        articles = discover_articles(REPO_ROOT / "docs")

        self.assertEqual(len(articles), 20)
        self.assertEqual(len({article["kb_id"] for article in articles}), 20)
        self.assertEqual(len({article["content_hash"] for article in articles}), 20)
        self.assertTrue(
            all(article["author"] == "Tier 1 Support Lab" for article in articles)
        )

    def test_build_creates_searchable_self_contained_site(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "site"
            report = build_site(REPO_ROOT / "docs", output)

            self.assertEqual(report["article_count"], 20)
            self.assertTrue((output / "index.html").is_file())
            self.assertTrue((output / "assets" / "site.css").is_file())
            self.assertTrue((output / "assets" / "site.js").is_file())
            self.assertEqual(len(list(output.glob("*.html"))), 21)

            search_index = json.loads(
                (output / "search-index.json").read_text(encoding="utf-8")
            )
            self.assertEqual(len(search_index), 20)
            self.assertTrue(all(record["plain_text"] for record in search_index))

            html = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn("SIMULATED PORTFOLIO LAB", html)
            self.assertIn('content="index, follow"', html)
            self.assertIn('class="nav-group-button"', html)
            self.assertNotIn("Internal Use Only", html)
            self.assertNotIn("cdn.jsdelivr.net", html)
            self.assertNotIn("cdnjs.cloudflare.com", html)

    def test_every_generated_local_link_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "site"
            build_site(REPO_ROOT / "docs", output)
            missing = []

            for html_path in output.glob("*.html"):
                collector = LinkCollector()
                collector.feed(html_path.read_text(encoding="utf-8"))
                for target in collector.targets:
                    parts = urlsplit(target)
                    if parts.scheme or target.startswith(
                        ("#", "mailto:", "javascript:")
                    ):
                        continue
                    local_target = unquote(parts.path)
                    if not local_target:
                        continue
                    candidate = (html_path.parent / local_target).resolve()
                    if not candidate.exists():
                        missing.append(f"{html_path.name} -> {target}")

            self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
