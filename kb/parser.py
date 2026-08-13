import re
import sys
from datetime import datetime
from pathlib import Path
import frontmatter
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension

def parse_markdown_file(filepath: Path) -> dict | None:
    """
    Parse a single Markdown file, extracting YAML frontmatter and
    converting the body to HTML.

    Returns a dict containing all metadata and the rendered HTML body,
    or None if the file cannot be parsed.
    """
    try:
        post = frontmatter.load(filepath)
    except Exception as exc:
        print(f"  [WARN] Could not parse {filepath.name}: {exc}")
        return None

    meta = dict(post.metadata)

    # Validate required fields
    required = ["title", "category"]
    for field in required:
        if field not in meta:
            print(
                f"  [WARN] Skipping {filepath.name}: missing required "
                f"frontmatter field '{field}'"
            )
            return None

    # Ensure tags is a list
    if isinstance(meta.get("tags"), str):
        meta["tags"] = [t.strip() for t in meta["tags"].split(",") if t.strip()]
    elif not isinstance(meta.get("tags"), list):
        meta["tags"] = []
    meta["tags"] = [t.lstrip("#").strip() for t in meta["tags"] if t.strip()]

    # Generate a short title for the sidebar
    short_title = meta.get("title", "")
    for prefix in ["FAQ:", "FAQ -", "How-To:", "How-To Guides:", "Fix Notes:"]:
        if short_title.lower().startswith(prefix.lower()):
            short_title = short_title[len(prefix):].strip()
    meta["short_title"] = short_title

    # Normalise last_updated to a display string
    last_updated = meta.get("last_updated", "")
    if hasattr(last_updated, "strftime"):
        last_updated = last_updated.strftime("%B %d, %Y")
    elif isinstance(last_updated, str) and last_updated:
        try:
            parsed = datetime.strptime(last_updated, "%Y-%m-%d")
            last_updated = parsed.strftime("%B %d, %Y")
        except ValueError:
            pass
    meta["last_updated"] = last_updated or "Unknown"

    # Convert Markdown body → HTML
    md_extensions = [
        FencedCodeExtension(),
        CodeHiliteExtension(linenums=False, guess_lang=False),
        TableExtension(),
        TocExtension(permalink=True),
        "nl2br",
        "smarty",
        "attr_list",
    ]
    md = markdown.Markdown(extensions=md_extensions)
    body_html = md.convert(post.content)

    # Generate a URL-safe slug from the filename (without extension)
    slug = filepath.stem.lower()
    slug = re.sub(r"[^a-z0-9\-]", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")

    # Build plain-text excerpt for search index (first 300 chars of content)
    plain_text = re.sub(r"<[^>]+>", "", body_html)
    plain_text = plain_text.replace("¶", "").replace("&para;", "").strip()
    plain_text = re.sub(r"^(Summary|Overview|Question|Issue|Symptoms|Issue Description|## [^\n]+)\s*", "", plain_text, flags=re.IGNORECASE).strip()
    plain_text = re.sub(r"\s+", " ", plain_text).strip()
    excerpt = plain_text[:300] + ("..." if len(plain_text) > 300 else "")

    return {
        "slug": slug,
        "filename": filepath.name,
        "title": meta.get("title", filepath.stem),
        "short_title": meta.get("short_title", meta.get("title", filepath.stem)),
        "author": meta.get("author", "Unknown"),
        "category": meta.get("category", "Uncategorised"),
        "last_updated": meta["last_updated"],
        "target_audience": meta.get("target_audience", ""),
        "tags": meta["tags"],
        "severity": meta.get("severity", "N/A"),
        "kb_id": meta.get("kb_id", ""),
        "incident_date": str(meta.get("incident_date", "")),
        "resolution_date": str(meta.get("resolution_date", "")),
        "total_downtime": meta.get("total_downtime", ""),
        "affected_users": meta.get("affected_users", ""),
        "body_html": body_html,
        "excerpt": excerpt,
        "plain_text": plain_text,
        "toc": md.toc,
    }

def discover_articles(docs_dir: Path) -> list[dict]:
    """
    Recursively walk docs_dir, parse every .md file found, and return
    a list of article dicts sorted by category order then title.
    """
    articles = []
    md_files = sorted(docs_dir.rglob("*.md"))

    if not md_files:
        sys.exit(f"[ERROR] No .md files found in '{docs_dir}'. Aborting.")

    print(f"[INFO] Discovered {len(md_files)} Markdown file(s) in '{docs_dir}'")

    for filepath in md_files:
        print(f"  Parsing: {filepath.relative_to(docs_dir)}")
        article = parse_markdown_file(filepath)
        if article:
            articles.append(article)

    print(f"[INFO] Successfully parsed {len(articles)} article(s)")
    return articles

