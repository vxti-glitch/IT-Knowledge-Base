from collections import defaultdict
from .config import SITE_TITLE, SITE_SUBTITLE, BUILD_VERSION, CATEGORY_META, SEVERITY_CLASSES, CATEGORY_ORDER
from .assets import SITE_CSS, SITE_JS

def render_topbar(build_ts: str) -> str:
    return f"""
    <header class="topbar" role="banner">
      <a href="index.html" class="topbar__brand" aria-label="{SITE_TITLE} home">
        <span class="topbar__brand-title">{SITE_TITLE}</span>
        <span class="topbar__brand-subtitle">{SITE_SUBTITLE}</span>
      </a>
      <div class="topbar__search-wrapper" role="search">
        <span class="topbar__search-icon" aria-hidden="true">&#9906;</span>
        <label for="search-input" class="visually-hidden">Search articles</label>
        <input
          type="search"
          id="search-input"
          placeholder="Search articles... (press / to focus)"
          autocomplete="off"
          spellcheck="false"
          aria-label="Search knowledge base articles"
        />
        <button id="search-clear" class="topbar__search-clear" aria-label="Clear search">&times;</button>
      </div>
      <span id="search-results-count" aria-live="polite" aria-atomic="true"></span>
      <div class="topbar__actions">
        <button id="theme-toggle" class="theme-toggle" aria-label="Toggle Theme">
          <span id="theme-icon">&#9789;</span>
        </button>
      </div>
    </header>"""

def render_sidebar(articles: list[dict]) -> str:
    """Build the sidebar navigation grouped by category and OS."""
    by_category = defaultdict(list)
    for art in articles:
        by_category[art["category"]].append(art)

    sidebar_html = '<nav class="sidebar" aria-label="Article navigation">\n'

    # Clean category mapping to remove emojis
    CATEGORY_META_NO_EMOJI = {
        "FAQ": {"icon": "", "color_class": "cat-faq", "slug": "faq", "desc": "Quick answers to common tech support questions."},
        "How-To Guides": {"icon": "", "color_class": "cat-how-to", "slug": "how-to", "desc": "Step-by-step instructions for IT procedures."},
    }

    for cat in CATEGORY_ORDER:
        if cat not in by_category:
            continue
        meta = CATEGORY_META_NO_EMOJI.get(cat, {"icon": "", "color_class": "", "slug": cat.lower()})
        cat_articles = by_category[cat]
        count = len(cat_articles)
        color_cls = meta["color_class"]

        sidebar_html += f"""
  <div class="sidebar__category {color_cls}">
    <div class="sidebar__category-header" role="button" aria-expanded="true">
      <span>{cat}</span>
      <span class="sidebar__category-count">{count}</span>
    </div>
    <div class="sidebar__os-groups">
"""
        # Group by OS
        os_groups = defaultdict(list)
        for art in cat_articles:
            tags_lower = [t.lower() for t in art["tags"]]
            if "windows" in tags_lower: os_name = "Windows"
            elif "macos" in tags_lower: os_name = "macOS"
            elif "linux" in tags_lower: os_name = "Linux"
            elif "chromeos" in tags_lower: os_name = "ChromeOS"
            else: os_name = "General/Network"
            os_groups[os_name].append(art)

        # Iterate over sorted OS groups (ChromeOS, General/Network, Linux, Windows, macOS)
        for os_name in sorted(os_groups.keys()):
            os_articles = os_groups[os_name]
            sidebar_html += f"""
      <div class="sidebar__os-group is-collapsed">
        <div class="sidebar__os-header" role="button" aria-expanded="false">
          <span>{os_name}</span>
          <span class="sidebar__category-count">{len(os_articles)}</span>
        </div>
        <ul class="sidebar__articles" role="list">
"""
            for art in sorted(os_articles, key=lambda x: x.get("short_title", x["title"])):
                sidebar_title = art.get("short_title", art["title"])
                sidebar_html += f"""
          <li role="listitem">
            <a href="{art['slug']}.html" class="sidebar__article-link" title="{art['title']}">
              {sidebar_title}
            </a>
          </li>"""
            sidebar_html += "\n        </ul>\n      </div>\n"

        sidebar_html += "    </div>\n  </div>\n"

    sidebar_html += "</nav>\n"
    return sidebar_html

def render_article_card(art: dict, color_cls: str) -> str:
    sev_cls = SEVERITY_CLASSES.get(art["severity"], "badge-na")
    sev_badge = (
        f'<span class="badge {sev_cls}" aria-label="Severity: {art["severity"]}">'
        f'{art["severity"]}</span>'
        if art["severity"] and art["severity"] != "N/A"
        else ""
    )
    kb_id_badge = (
        f'<span class="article-card__kb-id">{art["kb_id"]}</span>'
        if art["kb_id"] else ""
    )
    tags_html = "".join(
        f'<span class="tag-pill">#{t}</span>' for t in art["tags"][:5]
    )

    title_esc   = art['title'].replace('"', '&quot;')
    excerpt_esc = art['excerpt'].replace('"', '&quot;')
    tags_esc    = ",".join(art["tags"]).replace('"', '&quot;')
    author_esc  = art["author"].replace('"', '&quot;')
    audience_esc = art["target_audience"].replace('"', '&quot;')

    return f'''
<a class="article-card {color_cls}"
   href="{art['slug']}.html"
   data-slug="{art['slug']}"
   data-title="{title_esc}"
   data-tags="{tags_esc}"
   data-excerpt="{excerpt_esc}"
   data-author="{author_esc}"
   data-kbid="{art['kb_id']}"
   data-audience="{audience_esc}"
   data-category="{art['category']}"
   aria-label="Article: {title_esc}">
  <div class="article-card__header">
    {kb_id_badge}
    {sev_badge}
  </div>
  <h3 class="article-card__title" style="font-size:1.1rem;font-weight:600;margin:8px 0;color:var(--clr-text-primary);">{art['title']}</h3>
  <p class="article-card__excerpt" style="display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;color:var(--clr-text-muted);font-size:0.9rem;margin-bottom:12px;line-height:1.5;">{art['excerpt']}</p>
  <div class="article-card__meta">
    <span style="font-size:0.72rem;color:var(--clr-text-muted)">
      Updated: {art['last_updated']}
    </span>
    {'&bull; <span style="font-size:0.72rem;color:var(--clr-text-muted)">' + art['author'] + '</span>' if art['author'] else ''}
  </div>
  <div class="article-card__tags">{tags_html}</div>
</a>'''

def render_index_page(articles: list[dict], sidebar_html: str, topbar_html: str,
                      all_tags: list[str], build_ts: str) -> str:
    """Render the main index.html page."""
    by_category = defaultdict(list)
    for art in articles:
        by_category[art["category"]].append(art)

    sections_html = ""
    for cat in CATEGORY_ORDER:
        if cat not in by_category:
            continue
        meta = CATEGORY_META.get(cat, {"icon": "•", "color_class": "", "desc": ""})
        color_cls = meta["color_class"]
        cards_html = "".join(
            render_article_card(art, color_cls)
            for art in sorted(by_category[cat], key=lambda x: x["title"])
        )
        sections_html += f"""
<section class="category-section {color_cls}" aria-labelledby="cat-{meta['slug']}">
  <div class="category-section__header">
    <div class="category-section__icon" aria-hidden="true">{meta['icon']}</div>
    <div class="category-section__title-block">
      <h2 id="cat-{meta['slug']}">{cat}</h2>
      <p>{meta['desc']}</p>
    </div>
  </div>
  <div class="article-cards" role="list">
    {cards_html}
  </div>
</section>"""

    tag_bar_html = '''
    <div class="dropdown-filters" role="region" aria-label="Filters" style="display:flex;gap:12px;margin-bottom:24px;">
      <select id="filter-system" class="filter-dropdown" style="padding:8px 12px;border-radius:6px;background:var(--clr-bg-card);border:1px solid var(--clr-border);color:var(--clr-text-primary);outline:none;font-family:var(--font-sans);font-size:0.95rem;">
        <option value="">Filter by System...</option>
        <option value="printing">Printing & Scanning</option>
        <option value="email">Email & Exchange</option>
        <option value="active directory">Active Directory</option>
        <option value="networking">Networking</option>
        <option value="hardware">Hardware</option>
      </select>
      <select id="filter-os" class="filter-dropdown" style="padding:8px 12px;border-radius:6px;background:var(--clr-bg-card);border:1px solid var(--clr-border);color:var(--clr-text-primary);outline:none;font-family:var(--font-sans);font-size:0.95rem;">
        <option value="">Filter by OS...</option>
        <option value="windows">Windows</option>
        <option value="linux">Linux</option>
        <option value="macos">macOS</option>
        <option value="chromeos">ChromeOS</option>
      </select>
      <select id="filter-category" class="filter-dropdown" style="padding:8px 12px;border-radius:6px;background:var(--clr-bg-card);border:1px solid var(--clr-border);color:var(--clr-text-primary);outline:none;font-family:var(--font-sans);font-size:0.95rem;">
        <option value="">Filter by Category...</option>
        <option value="FAQ">FAQ</option>
        <option value="How-To Guides">How-To Guides</option>
      </select>
    </div>
    '''

    total = len(articles)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <script>
    const theme = localStorage.getItem('theme');
    if (theme === 'light') document.documentElement.setAttribute('data-theme', 'light');
  </script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Internal IT knowledge base covering FAQ, How-To Guides, and Fix Notes for the support team." />
  <meta name="robots" content="noindex, nofollow" />
  <title>{SITE_TITLE} — {SITE_SUBTITLE}</title>
  <script src="https://cdn.jsdelivr.net/npm/fuse.js/dist/fuse.js"></script>
  <style>{SITE_CSS}</style>
</head>
<body>
<div class="layout">
  {topbar_html}
  {sidebar_html}

  <main class="main" id="main-content" tabindex="-1">
    <div class="index-header">
      <h1>{SITE_TITLE}</h1>
      <p>{total} articles across {len(CATEGORY_ORDER)} categories &mdash; {SITE_SUBTITLE}</p>
    </div>

    {tag_bar_html}

    {sections_html}

    <div class="no-results" id="no-results" role="alert" aria-live="assertive">
      <div class="no-results__icon" aria-hidden="true">&#9906;</div>
      <h3>No articles match your search.</h3>
      <p>Try different keywords or clear the tag filter.</p>
    </div>
  </main>
</div>

<footer class="footer" role="contentinfo">
  <span>{SITE_TITLE} &mdash; Internal Use Only</span>
  <span>Generated by kb_builder.py v{BUILD_VERSION} &middot; {build_ts}</span>
</footer>

<script>{SITE_JS}</script>
</body>
</html>"""

def render_article_page(art: dict, sidebar_html: str, topbar_html: str,
                        build_ts: str) -> str:
    """Render an individual article HTML page."""
    sev_cls = SEVERITY_CLASSES.get(art["severity"], "badge-na")

    incident_box = ""
    if art["category"] == "Fix Notes" and any([
        art["incident_date"], art["total_downtime"], art["affected_users"]
    ]):
        stats = ""
        if art["incident_date"]:
            stats += f'<div><div class="incident-stat__label">Incident Date</div><div class="incident-stat__value">{art["incident_date"]}</div></div>'
        if art["resolution_date"]:
            stats += f'<div><div class="incident-stat__label">Resolved</div><div class="incident-stat__value">{art["resolution_date"]}</div></div>'
        if art["total_downtime"]:
            stats += f'<div><div class="incident-stat__label">Downtime</div><div class="incident-stat__value">{art["total_downtime"]}</div></div>'
        if art["affected_users"]:
            stats += f'<div><div class="incident-stat__label">Users Affected</div><div class="incident-stat__value">{art["affected_users"]}</div></div>'

        incident_box = f"""
<div class="article-page__incident-box" role="region" aria-label="Incident summary data">
  <h3>Incident Summary Data</h3>
  <div class="incident-stats">
    {stats}
  </div>
</div>"""

    # Tags
    tags_html = "".join(
        f'<span class="tag-pill">#{t}</span>' for t in art["tags"]
    )

    # Meta bar items
    meta_items = [
        ("KB ID", f'<code style="font-family:var(--font-mono);font-size:0.85rem">{art["kb_id"]}</code>' if art["kb_id"] else "N/A"),
        ("Author", art["author"] or "Unknown"),
        ("Last Updated", art["last_updated"]),
        ("Audience", art["target_audience"] or "All Staff"),
    ]
    if art["severity"] and art["severity"] != "N/A":
        meta_items.append(("Severity", f'<span class="badge {sev_cls}">{art["severity"]}</span>'))

    meta_html = "".join(
        f'<div class="article-page__meta-item"><div class="article-page__meta-label">{label}</div>'
        f'<div class="article-page__meta-value">{value}</div></div>'
        for label, value in meta_items
    )

    cat_meta = CATEGORY_META.get(art["category"], {"slug": "index", "color_class": ""})
    color_cls = cat_meta["color_class"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{art['excerpt'][:155]}" />
  <meta name="robots" content="noindex, nofollow" />
  <title>{art['title']} &mdash; {SITE_TITLE}</title>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
  <style>{SITE_CSS}</style>
  <script>
    const theme = localStorage.getItem('theme');
    if (theme === 'light') document.documentElement.setAttribute('data-theme', 'light');
  </script>
</head>
<body>
<div class="layout">
  {topbar_html}
  {sidebar_html}

  <main class="main" id="main-content" tabindex="-1">
    <article class="article-page {color_cls}" aria-label="{art['title']}">

      <nav class="article-page__breadcrumb" aria-label="Breadcrumb">
        <a href="index.html">{SITE_TITLE}</a>
        <span aria-hidden="true">/</span>
        <span>{art['category']}</span>
        <span aria-hidden="true">/</span>
        <span aria-current="page">{art['kb_id'] or art['slug']}</span>
      </nav>

      <h1 class="article-page__title">{art['title']}</h1>

      <div class="article-page__meta-bar" role="region" aria-label="Article metadata">
        {meta_html}
      </div>

      {incident_box}

      <div class="article-body-col">
        <div class="article-body">
          {art['body_html']}
        </div>

        <div class="article-page__tags" role="region" aria-label="Article tags">
          <div class="article-page__tags-label">Tags</div>
          {tags_html}
        </div>
      </div>
      <aside class="article-toc">
        <div class="article-page__tags-label" style="margin-bottom:8px">On This Page</div>
        {art.get('toc', '')}
      </aside>

    </article>
  </main>
</div>

<footer class="footer" role="contentinfo">
  <span>{SITE_TITLE} &mdash; Internal Use Only</span>
  <span>Generated by kb_builder.py v{BUILD_VERSION} &middot; {build_ts}</span>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-powershell.min.js"></script>
<script>{SITE_JS}</script>
</body>
</html>"""

