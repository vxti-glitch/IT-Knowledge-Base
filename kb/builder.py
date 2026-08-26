import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from .config import BUILD_VERSION
from .parser import ArticleValidationError, discover_articles
from .renderer import render_article_page, render_index_page

STATIC_DIR = Path(__file__).with_name("static")


def _prepare_output(output_dir: Path, docs_dir: Path) -> Path:
    resolved = output_dir.resolve()
    protected = {
        Path(resolved.anchor),
        Path.home().resolve(),
        Path.cwd().resolve(),
        docs_dir.resolve(),
    }
    if resolved in protected:
        raise ArticleValidationError(
            [f"Refusing to use protected output directory '{resolved}'"]
        )
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True)
    return resolved


def build_site(docs_dir: Path, output_dir: Path) -> dict:
    docs_dir = docs_dir.resolve()
    articles = discover_articles(docs_dir)
    output_dir = _prepare_output(output_dir, docs_dir)
    build_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    shutil.copytree(STATIC_DIR, output_dir / "assets")
    (output_dir / "index.html").write_text(
        render_index_page(articles, build_ts), encoding="utf-8"
    )
    for article in articles:
        (output_dir / f"{article['slug']}.html").write_text(
            render_article_page(article, articles, build_ts), encoding="utf-8"
        )

    search_index = [
        {
            "slug": article["slug"],
            "title": article["title"],
            "category": article["category"],
            "article_type": article["article_type"],
            "platforms": article["platforms"],
            "tags": article["tags"],
            "kb_id": article["kb_id"],
            "excerpt": article["excerpt"],
            "plain_text": article["plain_text"],
            "url": f"{article['slug']}.html",
        }
        for article in articles
    ]
    (output_dir / "search-index.json").write_text(
        json.dumps(search_index, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    report = {
        "simulation": True,
        "build_version": BUILD_VERSION,
        "generated_at": build_ts,
        "article_count": len(articles),
        "category_counts": dict(Counter(article["category"] for article in articles)),
        "article_type_counts": dict(
            Counter(article["article_type"] for article in articles)
        ),
        "quality_gate": {
            "unique_kb_ids": True,
            "unique_article_bodies": True,
            "required_metadata": True,
            "required_sections": True,
            "normalized_tags": True,
        },
    }
    (output_dir / "build-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    print(f"Built {len(articles)} validated articles in '{output_dir}'.")
    return report
