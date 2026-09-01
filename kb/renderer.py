from collections import Counter
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import (
    BUILD_VERSION,
    CATEGORY_META,
    CATEGORY_ORDER,
    SITE_SUBTITLE,
    SITE_TITLE,
)

TEMPLATE_DIR = Path(__file__).with_name("templates")


def _environment() -> Environment:
    return Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(("html", "xml")),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def _groups(articles: list[dict]) -> list[dict]:
    groups: list[dict] = []
    for category in CATEGORY_ORDER:
        category_articles = [
            article for article in articles if article["category"] == category
        ]
        if category_articles:
            groups.append(
                {
                    "name": category,
                    "meta": CATEGORY_META[category],
                    "articles": category_articles,
                }
            )
    return groups


def _base_context(articles: list[dict], build_ts: str) -> dict:
    return {
        "site_title": SITE_TITLE,
        "site_subtitle": SITE_SUBTITLE,
        "build_version": BUILD_VERSION,
        "build_ts": build_ts,
        "article_count": len(articles),
        "groups": _groups(articles),
    }


def render_index_page(articles: list[dict], build_ts: str) -> str:
    context = _base_context(articles, build_ts)
    context.update(
        {
            "page_kind": "index",
            "page_title": SITE_TITLE,
            "page_description": "Browse simulated Tier 1 help-desk troubleshooting articles, runbooks, validation steps, ticket notes, and escalation criteria.",
            "article_types": sorted({article["article_type"] for article in articles}),
            "platforms": sorted(
                {platform for article in articles for platform in article["platforms"]},
                key=str.casefold,
            ),
            "category_counts": Counter(article["category"] for article in articles),
            "evidence_statuses": sorted(
                {
                    (article["evidence_status"], article["evidence_status_label"])
                    for article in articles
                },
                key=lambda item: item[1].casefold(),
            ),
        }
    )
    return _environment().get_template("index.html").render(**context)


def render_article_page(article: dict, articles: list[dict], build_ts: str) -> str:
    def relevance(candidate: dict) -> tuple[int, str]:
        score = 0
        if candidate["category"] == article["category"]:
            score += 6
        score += 2 * len(set(candidate["platforms"]) & set(article["platforms"]))
        score += len(set(candidate["tags"]) & set(article["tags"]))
        return score, candidate["title"].casefold()

    related = [
        candidate for candidate in articles if candidate["slug"] != article["slug"]
    ]
    related.sort(
        key=lambda candidate: (-relevance(candidate)[0], relevance(candidate)[1])
    )
    context = _base_context(articles, build_ts)
    context.update(
        {
            "page_kind": "article",
            "page_title": f"{article['title']} — {SITE_TITLE}",
            "page_description": article["excerpt"][:155],
            "article": article,
            "related_articles": related[:3],
        }
    )
    return _environment().get_template("article.html").render(**context)
