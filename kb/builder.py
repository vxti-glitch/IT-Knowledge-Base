import shutil
import sys
import json
from datetime import datetime
from collections import defaultdict
from pathlib import Path
from .config import BUILD_VERSION
from .parser import discover_articles
from .renderer import render_index_page, render_article_page, render_topbar, render_sidebar

def build_site(docs_dir: Path, output_dir: Path) -> None:
    build_ts = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    print(f"\n[INFO] IT Knowledge Base Builder v{BUILD_VERSION}")
    print(f"[INFO] Source:  {docs_dir.resolve()}")
    print(f"[INFO] Output:  {output_dir.resolve()}")
    print(f"[INFO] Build:   {build_ts}\n")

    # Clean and recreate output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    print(f"[INFO] Output directory prepared: {output_dir}\n")

    # Discover and parse all articles
    articles = discover_articles(docs_dir)
    if not articles:
        sys.exit("[ERROR] No valid articles parsed. Aborting build.")

    # Collect all unique tags
    all_tags: list[str] = sorted(
        set(tag for art in articles for tag in art["tags"])
    )

    print(f"\n[INFO] Unique tags collected: {all_tags}")

    # Build shared layout components
    topbar_html  = render_topbar(build_ts)
    sidebar_html = render_sidebar(articles)

    # Generate index.html
    print("\n[INFO] Generating index.html ...")
    index_html = render_index_page(
        articles, sidebar_html, topbar_html, all_tags, build_ts
    )
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")
    print("  [OK] index.html")

    # Generate one HTML page per article
    print("[INFO] Generating article pages ...")
    for art in articles:
        page_html = render_article_page(art, sidebar_html, topbar_html, build_ts)
        out_path  = output_dir / f"{art['slug']}.html"
        out_path.write_text(page_html, encoding="utf-8")
        print(f"  [OK] {art['slug']}.html  ({art['category']} / {art['kb_id'] or art['title'][:40]})")

    # Generate search index JSON
    print("[INFO] Generating search-index.json ...")
    search_index = [
        {
            "slug":     art["slug"],
            "title":    art["title"],
            "category": art["category"],
            "author":   art["author"],
            "kb_id":    art["kb_id"],
            "tags":     art["tags"],
            "excerpt":  art["excerpt"],
            "url":      f"{art['slug']}.html",
        }
        for art in articles
    ]
    (output_dir / "search-index.json").write_text(
        json.dumps(search_index, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print("  [OK] search-index.json")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"[DONE] Build complete.")
    print(f"       Articles generated : {len(articles)}")
    print(f"       Unique tags        : {len(all_tags)}")
    print(f"       Output directory   : {output_dir.resolve()}")
    print(f"       Entry point        : {(output_dir / 'index.html').resolve()}")
    print(f"{'=' * 60}\n")
    print(f"Open the knowledge base:")
    print(f"  {(output_dir / 'index.html').resolve()}")
    print()

