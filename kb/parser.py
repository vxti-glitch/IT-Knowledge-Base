import hashlib
import html
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path

import bleach
import frontmatter
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension

from .config import (
    ARTICLE_TYPES,
    CATEGORY_META,
    CATEGORY_ORDER,
    REQUIRED_FIELDS,
    REQUIRED_SECTIONS,
    RISK_LEVELS,
    TAG_ALIASES,
)

KB_ID_PATTERN = re.compile(r"^KB-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$")
BANNED_PLACEHOLDERS = (
    "general issue issue",
    "get-service -name *general*",
    "get-service -name *how*",
    "failed or unresponsive status does not guarantee",
)
ALLOWED_TAGS = {
    "a",
    "blockquote",
    "br",
    "code",
    "div",
    "em",
    "h2",
    "h3",
    "h4",
    "hr",
    "li",
    "ol",
    "p",
    "pre",
    "span",
    "strong",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "ul",
}
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "code": ["class"],
    "div": ["class"],
    "h2": ["id"],
    "h3": ["id"],
    "h4": ["id"],
    "span": ["class"],
    "td": ["align"],
    "th": ["align"],
}


class ArticleValidationError(ValueError):
    """Raised when one or more published articles fail the content quality gate."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        lines = "\n".join(f"  - {error}" for error in errors)
        super().__init__(
            f"Content validation failed with {len(errors)} error(s):\n{lines}"
        )


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "article"


def _string_list(value: object) -> list[str]:
    if isinstance(value, str):
        values = value.split(",")
    elif isinstance(value, list):
        values = value
    else:
        return []
    return [str(item).lstrip("#").strip() for item in values if str(item).strip()]


def _normalize_tags(value: object) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for tag in _string_list(value):
        canonical = TAG_ALIASES.get(tag.casefold(), tag)
        key = canonical.casefold()
        if key not in seen:
            normalized.append(canonical)
            seen.add(key)
    return normalized


def _iso_date(value: object) -> str | None:
    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return None
    return None


def _section_names(content: str) -> set[str]:
    return {
        match.group(1).strip().casefold()
        for match in re.finditer(r"^##\s+(.+?)\s*$", content, flags=re.MULTILINE)
    }


def _validate_article(
    filepath: Path, docs_dir: Path, metadata: dict, content: str
) -> list[str]:
    relative = filepath.relative_to(docs_dir).as_posix()
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in metadata or metadata[field] in (None, "", []):
            errors.append(f"{relative}: missing required field '{field}'")

    category = str(metadata.get("category", "")).strip()
    if category not in CATEGORY_ORDER:
        errors.append(f"{relative}: unsupported category '{category}'")
    elif relative.split("/", 1)[0] != CATEGORY_META[category]["slug"]:
        errors.append(f"{relative}: folder does not match category '{category}'")

    article_type = str(metadata.get("article_type", "")).strip()
    if article_type not in ARTICLE_TYPES:
        errors.append(f"{relative}: unsupported article_type '{article_type}'")

    risk = str(metadata.get("risk", "")).strip()
    if risk not in RISK_LEVELS:
        errors.append(f"{relative}: unsupported risk '{risk}'")

    kb_id = str(metadata.get("kb_id", "")).strip()
    if kb_id and not KB_ID_PATTERN.fullmatch(kb_id):
        errors.append(f"{relative}: invalid kb_id '{kb_id}'")

    if metadata.get("last_updated") and not _iso_date(metadata["last_updated"]):
        errors.append(f"{relative}: last_updated must use YYYY-MM-DD")

    if len(_normalize_tags(metadata.get("tags"))) < 2:
        errors.append(f"{relative}: include at least two normalized tags")
    if not _string_list(metadata.get("platforms")):
        errors.append(f"{relative}: include at least one platform")

    headings = _section_names(content)
    for section in REQUIRED_SECTIONS:
        if section.casefold() not in headings:
            errors.append(f"{relative}: missing section '## {section}'")

    lowered = content.casefold()
    if "[¶](" in content or "&para;" in lowered:
        errors.append(f"{relative}: contains copied permalink markup")
    for phrase in BANNED_PLACEHOLDERS:
        if phrase in lowered:
            errors.append(f"{relative}: contains banned placeholder phrase '{phrase}'")
    if len(re.sub(r"\s+", " ", content).strip()) < 800:
        errors.append(
            f"{relative}: article is too short for the published quality gate"
        )
    return errors


def parse_markdown_file(filepath: Path, docs_dir: Path | None = None) -> dict:
    docs_root = docs_dir or filepath.parent
    try:
        post = frontmatter.load(filepath)
    except Exception as exc:
        raise ArticleValidationError(
            [f"{filepath.name}: invalid frontmatter: {exc}"]
        ) from exc

    metadata = dict(post.metadata)
    errors = _validate_article(filepath, docs_root, metadata, post.content)
    if errors:
        raise ArticleValidationError(errors)

    tags = _normalize_tags(metadata["tags"])
    platforms = _string_list(metadata["platforms"])
    updated_iso = _iso_date(metadata["last_updated"])
    updated_display = datetime.strptime(updated_iso, "%Y-%m-%d").strftime("%B %d, %Y")

    md = markdown.Markdown(
        extensions=[
            FencedCodeExtension(),
            CodeHiliteExtension(linenums=False, guess_lang=False),
            TableExtension(),
            TocExtension(permalink=False),
            "smarty",
            "attr_list",
        ]
    )
    rendered = md.convert(post.content)
    body_html = bleach.clean(
        rendered,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols={"http", "https", "mailto"},
        strip=True,
    )
    toc_html = bleach.clean(
        md.toc,
        tags={"a", "li", "ul"},
        attributes={"a": ["href"]},
        protocols={"http", "https"},
        strip=True,
    )
    plain_text = html.unescape(re.sub(r"<[^>]+>", " ", body_html))
    plain_text = re.sub(r"\s+", " ", plain_text).replace("¶", "").strip()
    summary_match = re.search(
        r"^## Summary\s*(.+?)(?=^##\s+)",
        post.content,
        flags=re.MULTILINE | re.DOTALL,
    )
    summary_text = summary_match.group(1).strip() if summary_match else plain_text
    summary_text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", summary_text)
    summary_text = re.sub(r"[`*_>#-]+", " ", summary_text)
    summary_text = re.sub(r"\s+", " ", summary_text).strip()
    excerpt = summary_text[:220] + ("..." if len(summary_text) > 220 else "")
    relative = filepath.relative_to(docs_root).as_posix()
    slug = slugify(filepath.stem)

    return {
        "slug": slug,
        "source_path": relative,
        "title": str(metadata["title"]).strip(),
        "author": str(metadata["author"]).strip(),
        "category": str(metadata["category"]).strip(),
        "category_slug": CATEGORY_META[str(metadata["category"]).strip()]["slug"],
        "article_type": str(metadata["article_type"]).strip(),
        "last_updated": updated_iso,
        "last_updated_display": updated_display,
        "kb_id": str(metadata["kb_id"]).strip(),
        "tags": tags,
        "platforms": platforms,
        "support_tier": str(metadata["support_tier"]).strip(),
        "risk": str(metadata["risk"]).strip(),
        "body_html": body_html,
        "toc": toc_html,
        "plain_text": plain_text,
        "excerpt": excerpt,
        "content_hash": hashlib.sha256(
            re.sub(r"\s+", " ", post.content).strip().encode("utf-8")
        ).hexdigest(),
    }


def discover_articles(docs_dir: Path) -> list[dict]:
    docs_dir = docs_dir.resolve()
    files = sorted(docs_dir.rglob("*.md")) if docs_dir.is_dir() else []
    if not files:
        raise ArticleValidationError([f"No Markdown articles found in '{docs_dir}'"])

    articles: list[dict] = []
    errors: list[str] = []
    for filepath in files:
        try:
            articles.append(parse_markdown_file(filepath, docs_dir))
        except ArticleValidationError as exc:
            errors.extend(exc.errors)

    for field, label in (
        ("kb_id", "KB ID"),
        ("slug", "slug"),
        ("content_hash", "article body"),
    ):
        counts = Counter(article[field] for article in articles)
        for value, count in sorted(counts.items()):
            if count > 1:
                sources = ", ".join(
                    article["source_path"]
                    for article in articles
                    if article[field] == value
                )
                errors.append(f"Duplicate {label} across {count} articles: {sources}")

    if errors:
        raise ArticleValidationError(errors)

    rank = {category: index for index, category in enumerate(CATEGORY_ORDER)}
    articles.sort(
        key=lambda article: (rank[article["category"]], article["title"].casefold())
    )
    return articles
