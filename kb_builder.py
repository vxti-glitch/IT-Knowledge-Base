#!/usr/bin/env python3
"""
kb_builder.py — Automated IT Knowledge Base Static Site Generator
=================================================================
Ingests a directory of Markdown files with YAML frontmatter and compiles
them into a complete, self-contained static HTML website with sidebar
navigation, client-side full-text search, and a tag-based filter system.

Requirements:
    pip install markdown python-frontmatter

Usage:
    python kb_builder.py --docs ./docs --output ./output

Author:   IT Support Portfolio Project
Version:  1.0.0
"""

import argparse
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

try:
    import frontmatter
except ImportError:
    sys.exit(
        "[ERROR] Required package 'python-frontmatter' not found.\n"
        "Install it with: pip install python-frontmatter"
    )

try:
    import markdown
    from markdown.extensions.codehilite import CodeHiliteExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.toc import TocExtension
except ImportError:
    sys.exit(
        "[ERROR] Required package 'markdown' not found.\n"
        "Install it with: pip install markdown"
    )


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SITE_TITLE = "IT Knowledge Base"
SITE_SUBTITLE = "Internal Documentation Portal"
BUILD_VERSION = "1.0.0"

CATEGORY_ORDER = ["FAQ", "How-To Guides"]

CATEGORY_META = {
    "FAQ": {
        "icon": "?",
        "desc": "Quick answers to common tech support questions.",
        "slug": "faq",
        "color_class": "cat-faq",
    },
    "How-To Guides": {
        "icon": "&#9654;",
        "desc": "Step-by-step operational and configuration guides.",
        "slug": "how-to",
        "color_class": "cat-howto",
    },
}

SEVERITY_CLASSES = {
    "Critical": "badge-critical",
    "High": "badge-high",
    "Medium": "badge-medium",
    "Low": "badge-low",
    "N/A": "badge-na",
}


# ---------------------------------------------------------------------------
# Markdown Parser
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# File Discovery
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# CSS — Inline professional theme
# ---------------------------------------------------------------------------

SITE_CSS = r"""
/* ============================================================
   IT Knowledge Base — Enterprise Documentation Theme
   Inspired by: Vercel Docs, GitHub Primer
   Typeface: Inter (UI), JetBrains Mono (code)
   Palette:  Cold corporate — near-black canvas, sharp borders
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Custom Properties ─────────────────────────────── */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  /* ---- Canvas ---- */
  --clr-bg-page:        #0a0a0a;
  --clr-bg-sidebar:     #111111;
  --clr-bg-content:     #0a0a0a;
  --clr-bg-card:        #111111;
  --clr-bg-card-hover:  #161616;
  --clr-bg-code:        #141414;
  --clr-bg-inline-code: #1a1a1a;

  /* ---- Borders ---- */
  --clr-border:         #1f1f1f;
  --clr-border-strong:  #2e2e2e;
  --clr-border-subtle:  #181818;

  /* ---- Text ---- */
  --clr-text-primary:   #ededed;
  --clr-text-secondary: #a1a1a1;
  --clr-text-muted:     #555555;
  --clr-text-dimmed:    #3a3a3a;
  --clr-btn-icon:       #ededed;
}

[data-theme="light"] {
  --clr-bg-page:        #fcfcfc;
  --clr-bg-sidebar:     #f5f5f5;
  --clr-bg-content:     #ffffff;
  --clr-bg-card:        #ffffff;
  --clr-bg-card-hover:  #f9f9f9;
  --clr-bg-code:        #f5f5f5;
  --clr-bg-inline-code: #f0f0f0;
  --clr-border:         #eaeaea;
  --clr-border-strong:  #dcdcdc;
  --clr-border-subtle:  #f0f0f0;
  --clr-text-primary:   #111111;
  --clr-text-secondary: #444444;
  --clr-text-muted:     #888888;
  --clr-text-dimmed:    #aaaaaa;
  --clr-btn-icon:       #111111;
}

:root {
  /* ---- Accent (Vercel blue) ---- */
  --clr-accent:         #0070f3;
  --clr-accent-hover:   #338ef7;
  --clr-accent-subtle:  rgba(0, 112, 243, 0.06);
  --clr-accent-border:  rgba(0, 112, 243, 0.25);

  /* ---- Category chromes (desaturated, corporate) ---- */
  --clr-cat-faq:        #3b82f6;
  --clr-cat-howto:      #8b5cf6;
  --clr-cat-fixnotes:   #ef4444;

  /* ---- Severity ---- */
  --clr-sev-critical-bg:  rgba(239, 68, 68, 0.08);
  --clr-sev-critical-fg:  #f87171;
  --clr-sev-critical-bd:  rgba(239, 68, 68, 0.2);
  --clr-sev-high-bg:      rgba(249, 115, 22, 0.08);
  --clr-sev-high-fg:      #fb923c;
  --clr-sev-high-bd:      rgba(249, 115, 22, 0.2);
  --clr-sev-medium-bg:    rgba(234, 179, 8, 0.08);
  --clr-sev-medium-fg:    #facc15;
  --clr-sev-medium-bd:    rgba(234, 179, 8, 0.2);
  --clr-sev-low-bg:       rgba(34, 197, 94, 0.08);
  --clr-sev-low-fg:       #4ade80;
  --clr-sev-low-bd:       rgba(34, 197, 94, 0.2);
  --clr-sev-na-bg:        rgba(113, 113, 113, 0.08);
  --clr-sev-na-fg:        #737373;
  --clr-sev-na-bd:        rgba(113, 113, 113, 0.2);

  /* ---- Typography ---- */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
               Helvetica, Arial, sans-serif;
  --font-mono: 'JetBrains Mono', 'Cascadia Code', 'Fira Code',
               'Consolas', 'Courier New', monospace;

  /* ---- Layout ---- */
  --sidebar-width:  260px;
  --topbar-height:  48px;
  --content-max:    820px;

  /* ---- Transitions ---- */
  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --t-fast: 0.12s;
  --t-mid:  0.2s;
}

html {
  scroll-behavior: smooth;
  font-size: 14px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

body {
  font-family: var(--font-sans);
  background: var(--clr-bg-page);
  color: var(--clr-text-primary);
  line-height: 1.6;
  min-height: 100vh;
  letter-spacing: -0.005em;
}

/* ── Selection ──────────────────────────────────────────────── */
::selection {
  background: rgba(0, 112, 243, 0.2);
  color: var(--clr-text-primary);
}

.headerlink { display: none; }

/* ── Layout Shell ───────────────────────────────────────────── */
.layout {
  display: grid;
  grid-template-columns: var(--sidebar-width) 1fr;
  grid-template-rows: var(--topbar-height) 1fr auto;
  min-height: 100vh;
}

/* ── Top Bar ────────────────────────────────────────────────── */
.topbar {
  grid-column: 1 / -1;
  grid-row: 1;
  background: var(--clr-bg-page);
  border-bottom: 1px solid var(--clr-border);
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 20px;
  position: sticky;
  top: 0;
  z-index: 200;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.topbar__brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex-shrink: 0;
}

.topbar__brand-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--clr-text-primary);
  letter-spacing: -0.01em;
}

.topbar__brand-divider {
  width: 1px;
  height: 18px;
  background: var(--clr-border-strong);
  flex-shrink: 0;
}

.topbar__brand-subtitle {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  font-weight: 400;
}

.topbar__search-wrapper {
  flex: 1;
  max-width: 480px;
  position: relative;
}

#search-input {
  width: 100%;
  background: var(--clr-bg-card);
  border: 1px solid var(--clr-border-strong);
  border-radius: 6px;
  padding: 7px 14px 7px 36px;
  font-family: var(--font-sans);
  font-size: 0.8125rem;
  color: var(--clr-text-primary);
  outline: none;
  transition: border-color var(--t-fast), box-shadow var(--t-fast);
}

#search-input::placeholder {
  color: var(--clr-text-muted);
  font-size: 0.8rem;
}

#search-input:focus {
  border-color: var(--clr-accent);
  box-shadow: 0 0 0 2px var(--clr-accent-subtle);
  background: #0d0d0d;
}

.topbar__search-icon {
  position: absolute;
  left: 11px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--clr-text-muted);
  font-size: 0.8rem;
  pointer-events: none;
}

.topbar__search-clear {
  position: absolute;
  right: 9px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--clr-text-muted);
  cursor: pointer;
  font-size: 0.875rem;
  line-height: 1;
  display: none;
  padding: 2px 4px;
  border-radius: 3px;
  transition: color var(--t-fast);
}

.topbar__search-clear:hover { color: var(--clr-text-primary); }

#search-results-count {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  margin-left: auto;
  flex-shrink: 0;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.topbar__build-info {
  font-size: 0.7rem;
  color: var(--clr-text-dimmed);
  white-space: nowrap;
  flex-shrink: 0;
  font-family: var(--font-mono);
}

/* ── Sidebar ────────────────────────────────────────────────── */
.sidebar {
  grid-column: 1;
  grid-row: 2;
  background: var(--clr-bg-sidebar);
  border-right: 1px solid var(--clr-border);
  overflow-y: auto;
  padding: 16px 0 48px;
  position: sticky;
  top: var(--topbar-height);
  height: calc(100vh - var(--topbar-height));
}

.sidebar::-webkit-scrollbar { width: 3px; }
.sidebar::-webkit-scrollbar-track { background: transparent; }
.sidebar::-webkit-scrollbar-thumb {
  background: var(--clr-border-strong);
  border-radius: 0;
}

/* Category group */
.sidebar__category { margin-bottom: 4px; }

.sidebar__category-header {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--clr-text-muted);
  cursor: pointer;
  user-select: none;
  transition: background var(--t-fast);
}

.sidebar__category-header:hover {
  background: rgba(255,255,255,0.03);
}

.sidebar__category-header::after {
  content: '▼';
  font-size: 0.6rem;
  margin-left: 8px;
  transition: transform 0.2s ease;
}

.sidebar__category.is-collapsed .sidebar__category-header::after {
  transform: rotate(-90deg);
}

.sidebar__category.is-collapsed .sidebar__articles,
.sidebar__category.is-collapsed .sidebar__os-groups {
  display: none;
}

.sidebar__os-group { margin: 2px 0 2px 16px; }

.sidebar__os-header {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--clr-text-secondary);
  cursor: pointer;
  user-select: none;
  transition: background var(--t-fast);
}

.sidebar__os-header:hover {
  background: rgba(255,255,255,0.03);
}

.sidebar__os-header::after {
  content: '▼';
  font-size: 0.55rem;
  margin-left: 6px;
  transition: transform 0.2s ease;
}

.sidebar__os-group.is-collapsed .sidebar__os-header::after {
  transform: rotate(-90deg);
}

.sidebar__os-group.is-collapsed .sidebar__articles {
  display: none;
}

.sidebar__category-count {
  margin-left: auto;
  font-size: 0.6875rem;
  font-weight: 500;
  color: var(--clr-text-dimmed);
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}

.sidebar__articles { list-style: none; }

.sidebar__article-link {
  display: block;
  padding: 6px 16px 6px 36px;
  color: var(--clr-text-secondary);
  text-decoration: none;
  font-size: 0.8125rem;
  transition: background var(--t-fast), color var(--t-fast);
  border-left: 2px solid transparent;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar__article-link:hover {
  color: var(--clr-text-primary);
  background: rgba(255,255,255,0.03);
  border-left-color: var(--clr-border-strong);
}

.sidebar__article-link.is-active {
  color: var(--clr-text-primary);
  border-left-color: var(--clr-accent);
  background: rgba(0, 112, 243, 0.04);
  font-weight: 500;
}

.sidebar__article-kb-id {
  display: block;
  font-size: 0.6875rem;
  color: var(--clr-text-dimmed);
  margin-top: 1px;
  font-family: var(--font-mono);
}

/* ── Main Content ───────────────────────────────────────────── */
.main {
  grid-column: 2;
  grid-row: 2;
  padding: 40px 48px;
  overflow-y: auto;
  min-width: 0;
}

/* ── Index / Home Page ──────────────────────────────────────── */
.index-header {
  margin-bottom: 36px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--clr-border);
}

.index-header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: -0.025em;
  color: var(--clr-text-primary);
  line-height: 1.2;
}

.index-header p {
  margin-top: 6px;
  font-size: 0.875rem;
  color: var(--clr-text-secondary);
  line-height: 1.5;
}

/* ── Tag Filter Bar ─────────────────────────────────────────── */
.tag-filter-section {
  margin-bottom: 32px;
}

.tag-filter-section h2 {
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--clr-text-muted);
  margin-bottom: 10px;
}

.tag-filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag-btn {
  background: transparent;
  border: 1px solid var(--clr-border-strong);
  border-radius: 4px;
  padding: 4px 10px;
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--clr-text-secondary);
  cursor: pointer;
  font-family: var(--font-sans);
  letter-spacing: -0.005em;
  transition: background var(--t-fast), border-color var(--t-fast),
              color var(--t-fast);
}

.tag-btn:hover {
  background: rgba(255,255,255,0.04);
  border-color: var(--clr-text-muted);
  color: var(--clr-text-primary);
}

.tag-btn.is-active {
  background: var(--clr-accent);
  border-color: var(--clr-accent);
  color: #fff;
  font-weight: 600;
}

.tag-btn--reset {
  color: var(--clr-text-muted);
  border-color: var(--clr-border);
}

/* ── Article Cards (Index) ──────────────────────────────────── */
.category-section {
  margin-bottom: 48px;
}

.category-section__header {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--clr-border);
}

.category-section__icon {
  font-size: 0.875rem;
  flex-shrink: 0;
  opacity: 0.6;
}

.cat-faq    .category-section__icon { color: var(--clr-cat-faq); }
.cat-howto  .category-section__icon { color: var(--clr-cat-howto); }
.cat-fixnotes .category-section__icon { color: var(--clr-cat-fixnotes); }

.category-section__title-block h2 {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--clr-text-primary);
  line-height: 1.2;
  letter-spacing: -0.01em;
}

.category-section__title-block p {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  margin-top: 2px;
}

/* Card grid — table-style rows */
.article-cards {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--clr-border);
  border-radius: 6px;
  overflow: hidden;
}

.article-card {
  background: var(--clr-bg-card);
  border-bottom: 1px solid var(--clr-border);
  padding: 16px 20px;
  text-decoration: none;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8px 16px;
  align-items: start;
  transition: background var(--t-fast);
  position: relative;
}

.article-card:last-child { border-bottom: none; }

.article-card::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 2px;
  opacity: 0;
  transition: opacity var(--t-fast);
}

.cat-faq    .article-card::before { background: var(--clr-cat-faq); }
.cat-howto  .article-card::before { background: var(--clr-cat-howto); }
.cat-fixnotes .article-card::before { background: var(--clr-cat-fixnotes); }

.article-card:hover {
  background: var(--clr-bg-card-hover);
}

.article-card:hover::before { opacity: 1; }

.article-card__left {
  min-width: 0;
  grid-column: 1;
}

.article-card__right {
  grid-column: 2;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
  flex-shrink: 0;
}

.article-card__header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.article-card__kb-id {
  font-size: 0.6875rem;
  font-family: var(--font-mono);
  color: var(--clr-text-muted);
  background: var(--clr-bg-code);
  padding: 1px 6px;
  border-radius: 3px;
  border: 1px solid var(--clr-border-strong);
  white-space: nowrap;
  flex-shrink: 0;
}

.article-card__title {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--clr-text-primary);
  line-height: 1.45;
  margin-bottom: 4px;
  letter-spacing: -0.005em;
}

.article-card__excerpt {
  font-size: 0.7812rem;
  color: var(--clr-text-secondary);
  line-height: 1.55;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-card__meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 6px;
}

.article-card__date {
  font-size: 0.6875rem;
  color: var(--clr-text-muted);
  font-variant-numeric: tabular-nums;
}

.article-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-pill {
  font-size: 0.6875rem;
  font-weight: 400;
  padding: 1px 7px;
  border-radius: 3px;
  background: transparent;
  border: 1px solid var(--clr-border-strong);
  color: var(--clr-text-muted);
  letter-spacing: 0.01em;
}

/* ── Badges ─────────────────────────────────────────────────── */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 7px;
  border-radius: 3px;
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.02em;
  border: 1px solid transparent;
  white-space: nowrap;
}

.badge-critical { background: var(--clr-sev-critical-bg); color: var(--clr-sev-critical-fg); border-color: var(--clr-sev-critical-bd); }
.badge-high     { background: var(--clr-sev-high-bg);     color: var(--clr-sev-high-fg);     border-color: var(--clr-sev-high-bd); }
.badge-medium   { background: var(--clr-sev-medium-bg);   color: var(--clr-sev-medium-fg);   border-color: var(--clr-sev-medium-bd); }
.badge-low      { background: var(--clr-sev-low-bg);      color: var(--clr-sev-low-fg);      border-color: var(--clr-sev-low-bd); }
.badge-na       { background: var(--clr-sev-na-bg);       color: var(--clr-sev-na-fg);       border-color: var(--clr-sev-na-bd); }

/* ── Article Page ───────────────────────────────────────────── */
.article-page {
  max-width: var(--content-max);
}

.article-page__breadcrumb {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.article-page__breadcrumb a {
  color: var(--clr-text-secondary);
  text-decoration: none;
  transition: color var(--t-fast);
}

.article-page__breadcrumb a:hover { color: var(--clr-text-primary); }

.article-page__title {
  font-size: 1.4375rem;
  font-weight: 600;
  letter-spacing: -0.025em;
  line-height: 1.3;
  color: var(--clr-text-primary);
  margin-bottom: 20px;
}

.article-page__meta-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 14px 20px;
  background: var(--clr-bg-card);
  border: 1px solid var(--clr-border);
  border-radius: 4px;
  margin-bottom: 28px;
  font-size: 0.8rem;
}

.article-page__meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.article-page__meta-label {
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--clr-text-muted);
}

.article-page__meta-value {
  color: var(--clr-text-secondary);
  font-size: 0.8125rem;
}

.article-page__incident-box {
  background: rgba(239, 68, 68, 0.05);
  border: 1px solid rgba(239, 68, 68, 0.15);
  border-left: 3px solid var(--clr-cat-fixnotes);
  border-radius: 0 4px 4px 0;
  padding: 14px 18px;
  margin-bottom: 24px;
}

.article-page__incident-box h3 {
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: #f87171;
  margin-bottom: 12px;
}

.incident-stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
}

.incident-stat__label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--clr-text-muted);
  margin-bottom: 2px;
}

.incident-stat__value {
  font-size: 0.8125rem;
  color: var(--clr-text-secondary);
  font-weight: 400;
}

/* ── Article Body Typography ────────────────────────────────── */
.article-body {
  font-size: 0.9rem;
  line-height: 1.75;
  color: var(--clr-text-primary);
}

.article-body h2 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--clr-text-primary);
  margin: 2.25em 0 0.6em;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--clr-border);
  letter-spacing: -0.015em;
}

.article-body h3 {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--clr-text-primary);
  margin: 1.75em 0 0.5em;
  letter-spacing: -0.01em;
}

.article-body h4 {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--clr-text-secondary);
  margin: 1.5em 0 0.4em;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.article-body p { margin-bottom: 1em; }
.article-body ul, .article-body ol {
  margin: 0 0 1em 1.25em;
  color: var(--clr-text-primary);
}
.article-body li { margin-bottom: 0.3em; line-height: 1.65; }

.article-body a {
  color: var(--clr-accent);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 2px;
  transition: color var(--t-fast);
}

.article-body a:hover { color: var(--clr-accent-hover); }

.article-body strong {
  font-weight: 600;
  color: var(--clr-text-primary);
}
.article-body em { font-style: italic; }

/* Inline code */
.article-body code {
  font-family: var(--font-mono);
  font-size: 0.8125em;
  background: var(--clr-bg-inline-code);
  border: 1px solid var(--clr-border-strong);
  border-radius: 3px;
  padding: 1px 5px;
  color: #a5b4fc;
}

/* Code blocks */
.article-body pre {
  background: var(--clr-bg-code);
  border: 1px solid var(--clr-border-strong);
  border-radius: 4px;
  padding: 18px 20px;
  overflow-x: auto;
  margin: 1.25em 0;
  position: relative;
}

.article-body pre code {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.8125rem;
  color: #cbd5e1;
  line-height: 1.65;
}

/* Tables */
.article-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.25em 0;
  font-size: 0.85rem;
}

.article-body th {
  background: var(--clr-bg-code);
  padding: 9px 14px;
  text-align: left;
  font-weight: 600;
  font-size: 0.75rem;
  letter-spacing: 0.045em;
  text-transform: uppercase;
  color: var(--clr-text-secondary);
  border: 1px solid var(--clr-border-strong);
}

.article-body td {
  padding: 8px 14px;
  border: 1px solid var(--clr-border);
  color: var(--clr-text-secondary);
  vertical-align: top;
  line-height: 1.5;
}

.article-body tr:nth-child(even) td {
  background: rgba(255,255,255,0.015);
}

/* Blockquotes */
.article-body blockquote {
  border-left: 2px solid var(--clr-border-strong);
  padding: 10px 18px;
  margin: 1.25em 0;
  color: var(--clr-text-secondary);
}

.article-body blockquote strong {
  color: var(--clr-text-secondary);
}

/* Checkboxes */
.article-body li input[type="checkbox"] {
  margin-right: 7px;
  accent-color: var(--clr-accent);
}

/* Article tags at the bottom */
.article-page__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid var(--clr-border);
}

.article-page__tags-label {
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--clr-text-muted);
  width: 100%;
  margin-bottom: 2px;
}

/* ── No Results Banner ──────────────────────────────────────── */
.no-results {
  display: none;
  text-align: center;
  padding: 64px 20px;
  color: var(--clr-text-muted);
}

.no-results__icon {
  font-size: 1.5rem;
  margin-bottom: 12px;
  opacity: 0.4;
}

.no-results h3 {
  font-size: 0.9375rem;
  color: var(--clr-text-secondary);
  margin-bottom: 6px;
  font-weight: 500;
}

/* ── Footer ─────────────────────────────────────────────────── */
.footer {
  grid-column: 1 / -1;
  grid-row: 3;
  padding: 14px 48px;
  border-top: 1px solid var(--clr-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.6875rem;
  color: var(--clr-text-dimmed);
  background: var(--clr-bg-page);
  font-family: var(--font-mono);
}

/* ── Utilities ───────────────────────────────────────────────── */
.hidden { display: none !important; }
.visually-hidden {
  position: absolute;
  width: 1px; height: 1px;
  clip: rect(0,0,0,0);
  overflow: hidden;
}

/* ── Responsive ─────────────────────────────────────────────── */
@media (max-width: 960px) {
  :root {
    --sidebar-width: 220px;
  }

  .main {
    padding: 28px 28px;
  }
}

@media (max-width: 740px) {
  .layout {
    grid-template-columns: 1fr;
    grid-template-rows: var(--topbar-height) auto 1fr auto;
  }

  .sidebar {
    grid-column: 1;
    grid-row: 2;
    position: static;
    height: auto;
    border-right: none;
    border-bottom: 1px solid var(--clr-border);
    padding: 10px 0;
    max-height: 220px;
    overflow-y: auto;
  }

  .main {
    grid-column: 1;
    grid-row: 3;
    padding: 20px 16px;
  }

  .footer {
    grid-column: 1;
    grid-row: 4;
    flex-direction: column;
    gap: 4px;
    text-align: center;
    padding: 14px 20px;
  }

  .topbar__build-info { display: none; }
  .topbar__brand-subtitle { display: none; }
  .topbar__brand-divider { display: none; }

  .article-cards {
    border-radius: 4px;
  }

  .article-card {
    grid-template-columns: 1fr;
    padding: 14px 16px;
  }

  .article-card__right {
    flex-direction: row;
    align-items: center;
  }
}

/* ── Dynamic ToC ────────────────────────────────────────────── */
.article-toc {
  display: none;
}
@media (min-width: 1200px) {
  .article-page {
    display: grid;
    grid-template-columns: 1fr 220px;
    gap: 40px;
    max-width: 1100px;
  }
  .article-body-col { grid-column: 1; min-width: 0; }
  .article-toc {
    display: block;
    grid-column: 2;
    position: sticky;
    top: calc(var(--topbar-height) + 40px);
    height: fit-content;
    max-height: calc(100vh - 100px);
    overflow-y: auto;
    font-size: 0.8125rem;
    padding-left: 10px;
    border-left: 1px solid var(--clr-border);
  }
  .article-toc .toc ul { list-style: none; padding-left: 10px; }
  .article-toc .toc > ul { padding-left: 0; }
  .article-toc a {
    color: var(--clr-text-secondary);
    text-decoration: none;
    display: block;
    padding: 3px 0;
    transition: color var(--t-fast);
  }
  .article-toc a:hover { color: var(--clr-text-primary); }
  .article-toc a.is-active {
    color: var(--clr-accent);
    font-weight: 600;
  }
}

/* ── Copy Buttons ───────────────────────────────────────────── */
.copy-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: var(--clr-bg-card);
  border: 1px solid var(--clr-border-strong);
  color: var(--clr-text-muted);
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 0.7rem;
  font-family: var(--font-sans);
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s, background 0.2s, color 0.2s;
}
.article-body pre:hover .copy-btn { opacity: 1; }
.copy-btn:hover {
  background: var(--clr-border-strong);
  color: var(--clr-text-primary);
}
.copy-btn.copied {
  background: var(--clr-accent);
  color: #fff;
  border-color: var(--clr-accent);
}

/* ── Theme Toggle ───────────────────────────────────────────── */
.theme-toggle {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--clr-btn-icon);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
  border-radius: 4px;
  font-size: 1.1rem;
}
.theme-toggle:hover { background: rgba(128,128,128,0.1); }
"""


# ---------------------------------------------------------------------------
# JavaScript — Search and tag filter engine
# ---------------------------------------------------------------------------

SITE_JS = r"""
'use strict';

(function () {
  const state = { query: '', activeTag: null, searchData: [], totalCount: 0 };
  const searchInput = document.getElementById('search-input');
  const searchClear = document.getElementById('search-clear');
  const resultsCount = document.getElementById('search-results-count');
  const noResults = document.getElementById('no-results');
  const articleCards = document.querySelectorAll('.article-card[data-slug]');
  const catSections = document.querySelectorAll('.category-section');

  let fuse = null;

  async function init() {
    state.totalCount = articleCards.length;

    // Theme toggle
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const isLight = document.documentElement.getAttribute('data-theme') === 'light';
        document.documentElement.setAttribute('data-theme', isLight ? 'dark' : 'light');
        localStorage.setItem('theme', isLight ? 'dark' : 'light');
        updateThemeIcon();
      });
      updateThemeIcon();
    }

    // Fuse.js
    if (window.Fuse && searchInput) {
      try {
        const res = await fetch('search-index.json');
        const data = await res.json();
        fuse = new window.Fuse(data, {
          keys: ['title', 'tags', 'plain_text'],
          threshold: 0.3,
          ignoreLocation: true
        });
      } catch (e) {
        console.error("Search index failed to load", e);
      }
    }

    if (searchInput) {
      searchInput.addEventListener('input', onSearchInput);
      searchInput.addEventListener('keydown', (e) => { if (e.key === 'Escape') clearSearch(); });
    }
    if (searchClear) searchClear.addEventListener('click', clearSearch);

    const filterSystem = document.getElementById('filter-system');
    const filterOs = document.getElementById('filter-os');
    const filterCategory = document.getElementById('filter-category');
    if (filterSystem) filterSystem.addEventListener('change', e => { state.filterSystem = e.target.value; updateDisplay(); });
    if (filterOs) filterOs.addEventListener('change', e => { state.filterOs = e.target.value; updateDisplay(); });
    if (filterCategory) filterCategory.addEventListener('change', e => { state.filterCategory = e.target.value; updateDisplay(); });

    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== searchInput) {
        e.preventDefault();
        searchInput && searchInput.focus();
      }
    });

    markActiveSidebarLink();
    initCopyButtons();
    initTocObserver();
    initSidebarAccordion();
    updateDisplay();
  }

  function updateThemeIcon() {
    const icon = document.getElementById('theme-icon');
    if (!icon) return;
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    icon.innerHTML = isLight ? '&#9728;' : '&#9789;';
  }

  function onSearchInput(e) {
    state.query = e.target.value.trim().toLowerCase();
    if (searchClear) searchClear.style.display = state.query ? 'block' : 'none';
    updateDisplay();
  }

  function clearSearch() {
    if (searchInput) searchInput.value = '';
    state.query = '';
    if (searchClear) searchClear.style.display = 'none';
    searchInput && searchInput.focus();
    updateDisplay();
  }

  function updateDisplay() {
    let visibleSlugs = new Set();
    
    if (state.query && fuse) {
      const results = fuse.search(state.query);
      results.forEach(r => visibleSlugs.add(r.item.slug));
    } else {
      articleCards.forEach(c => visibleSlugs.add(c.dataset.slug));
    }

    let visibleCount = 0;
    articleCards.forEach(card => {
      let show = visibleSlugs.has(card.dataset.slug);
      
      const tags = (card.dataset.tags || '').toLowerCase();
      const cardCategory = card.dataset.category || '';
      
      if (state.filterSystem && !tags.includes(state.filterSystem)) show = false;
      if (state.filterOs && !tags.includes(state.filterOs)) show = false;
      if (state.filterCategory && cardCategory !== state.filterCategory) show = false;

      if (show) {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    catSections.forEach(section => {
      if (state.query) {
        // When searching, hide category headers to just show flat results
        section.classList.remove('hidden');
        const header = section.querySelector('.category-section__header');
        if (header) header.style.display = 'none';
      } else {
        const header = section.querySelector('.category-section__header');
        if (header) header.style.display = 'flex';

        const cards = section.querySelectorAll('.article-card[data-slug]');
        const anyVisible = Array.from(cards).some(c => !c.classList.contains('hidden'));
        section.classList.toggle('hidden', !anyVisible);
      }
    });

    if (noResults) noResults.style.display = visibleCount === 0 ? 'block' : 'none';
    if (resultsCount) {
      if (!state.query && !state.activeTag) resultsCount.textContent = `${state.totalCount} articles`;
      else resultsCount.textContent = `${visibleCount} of ${state.totalCount} articles`;
    }
  }

  function markActiveSidebarLink() {
    const currentPage = window.location.pathname.split('/').pop();
    document.querySelectorAll('.sidebar__article-link').forEach(link => {
      const href = link.getAttribute('href').split('/').pop();
      if (href === currentPage && currentPage !== '' && currentPage !== 'index.html') {
        link.classList.add('is-active');
        link.scrollIntoView({ block: 'nearest' });
        
        // Ensure parent category and OS group are expanded
        const cat = link.closest('.sidebar__category');
        if (cat) cat.classList.remove('is-collapsed');
        const osGroup = link.closest('.sidebar__os-group');
        if (osGroup) osGroup.classList.remove('is-collapsed');
      }
    });
  }

  function initSidebarAccordion() {
    document.querySelectorAll('.sidebar__category-header, .sidebar__os-header').forEach(header => {
      header.addEventListener('click', () => {
        const cat = header.closest('.sidebar__category');
        const osGroup = header.closest('.sidebar__os-group');
        if (header.classList.contains('sidebar__category-header') && cat) {
          cat.classList.toggle('is-collapsed');
        } else if (header.classList.contains('sidebar__os-header') && osGroup) {
          osGroup.classList.toggle('is-collapsed');
        }
      });
    });
  }

  function initCopyButtons() {
    document.querySelectorAll('.article-body pre').forEach(pre => {
      const btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.textContent = 'Copy';
      btn.addEventListener('click', () => {
        const code = pre.querySelector('code');
        if (code) {
          navigator.clipboard.writeText(code.innerText).then(() => {
            btn.textContent = 'Copied!';
            btn.classList.add('copied');
            setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
          });
        }
      });
      pre.appendChild(btn);
    });
  }

  function initTocObserver() {
    const headers = document.querySelectorAll('.article-body h2, .article-body h3');
    const links = document.querySelectorAll('.article-toc a');
    if (!headers.length || !links.length) return;

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          links.forEach(l => l.classList.remove('is-active'));
          const id = entry.target.getAttribute('id');
          const activeLink = document.querySelector(`.article-toc a[href="#${id}"]`);
          if (activeLink) activeLink.classList.add('is-active');
        }
      });
    }, { rootMargin: '0px 0px -80% 0px' });

    headers.forEach(h => observer.observe(h));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
"""


# ---------------------------------------------------------------------------
# HTML Template Renderer
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Build Orchestrator
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="kb_builder.py",
        description=(
            "Automated IT Knowledge Base Static Site Generator.\n"
            "Converts Markdown files with YAML frontmatter into a "
            "complete, searchable HTML website."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python kb_builder.py
  python kb_builder.py --docs ./docs --output ./output
  python kb_builder.py --docs /path/to/docs --output /path/to/site
        """,
    )
    parser.add_argument(
        "--docs",
        type=Path,
        default=Path("./docs"),
        metavar="DIR",
        help="Path to the directory containing Markdown source files (default: ./docs)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("./output"),
        metavar="DIR",
        help="Path to the output directory for generated HTML files (default: ./output)",
    )

    args = parser.parse_args()

    if not args.docs.exists():
        sys.exit(
            f"[ERROR] Docs directory not found: '{args.docs}'\n"
            f"Create the directory and add .md files, or specify a valid path with --docs"
        )

    if not args.docs.is_dir():
        sys.exit(f"[ERROR] --docs must be a directory, not a file: '{args.docs}'")

    build_site(docs_dir=args.docs, output_dir=args.output)


if __name__ == "__main__":
    main()
