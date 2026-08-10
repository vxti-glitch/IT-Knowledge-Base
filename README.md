# Enterprise IT Knowledge Base Generator

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=flat-square) ![Build](https://img.shields.io/badge/Build-GitHub%20Actions-2088FF.svg?style=flat-square) ![Output](https://img.shields.io/badge/Output-Static%20HTML%2FCSS%2FJS-success.svg?style=flat-square) ![Hosting](https://img.shields.io/badge/Hosting-GitHub%20Pages-brightgreen.svg?style=flat-square) ![License](https://img.shields.io/badge/License-MIT-lightgrey.svg?style=flat-square)

A high-performance, automated static site generator engineered specifically for IT Help Desk and SysAdmin documentation. It compiles standard Markdown files containing troubleshooting guides into a fast, searchable, and responsive zero-dependency web portal.

- [Business Value](#business-value)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [How to Use](#how-to-use)
- [Markdown Schema](#markdown-schema)
- [Deployment Pipeline](#deployment-pipeline)
- [Security & Operations](#security--operations)

---

## Business Value

Help Desk documentation is often scattered across slow SharePoint sites, messy Word documents, or bloated Wiki software. Finding the right fix notes during a live incident is a high-stress, time-consuming task for technicians.

**Knowledge retrieval cost without automation:**

A technician typically spends 5-10 minutes searching across multiple platforms to find the correct diagnostic steps for a known issue. For a Help Desk handling 500 tickets a week, this translates to 40-80 hours of wasted labor per week simply searching for documentation.

**Documentation drift risk without automation:**

Traditional wikis require logging into a separate web interface, leading to "documentation drift" where technicians fix issues but avoid the friction of updating the wiki. 

**What this generator delivers:**

| Metric | Traditional Wiki/SharePoint | Automated Static Site (This Engine) |
|---|---|---|
| Load time per article | 2-5 seconds | Under 100 milliseconds |
| Search speed | Server-dependent, slow | Instant (Client-side JSON index) |
| Authoring friction | High (requires web portal login) | Low (Git + standard Markdown editors) |
| Hosting cost & maintenance | Requires DB, server patching, backups | $0. Zero backend infrastructure required. |
| Version control | Clunky wiki history | Native Git versioning & peer review (PRs) |

---

## Architecture

```text
IT-KB-Generator/
├── docs/                      # Markdown source of truth
│   ├── faq/                   # Frequently Asked Questions (.md)
│   └── how-to/                # Step-by-step guides (.md)
├── kb_builder.py              # Core Python static site generator
├── requirements.txt           # Python dependencies
├── .github/workflows/         # CI/CD deployment pipeline
└── output/                    # Compiled static assets (HTML/CSS/JS)
```

**Generation flow:**

The `kb_builder.py` script executes the following atomic sequence:
1. Crawls the `docs/` directory for `.md` files.
2. Extracts and validates YAML frontmatter (metadata).
3. Compiles Markdown body to HTML, applying Pygments syntax highlighting.
4. Generates a dynamic, client-side search index (`search_index.json`) for instant querying.
5. Renders a unified `index.html` featuring collapsible OS-based sidebars and filtering.

---

## Prerequisites

**Python Environment:**

```bash
python -m pip install -r requirements.txt
```

**Dependencies:**
- `markdown>=3.5.2` - Core parser
- `python-frontmatter>=1.1.0` - Metadata extraction
- `Pygments>=2.17.2` - Code block syntax highlighting

---

## How to Use

### 1. Authoring

Create a new Markdown file in the appropriate directory (`docs/faq/` or `docs/how-to/`). Adhere to the required YAML frontmatter schema.

### 2. Local Build & Testing

Run the generator to compile the site to the `output/` directory:

```bash
python kb_builder.py --docs ./docs --output ./output
```

Preview the site locally using a simple HTTP server:

```bash
cd output
python -m http.server 8000
```

---

## Markdown Schema

All articles must include valid YAML frontmatter. The parser explicitly looks for these fields to render metadata badges and sidebar navigation groups.

| Field | Required | Description |
|---|---|---|
| `title` | Yes | Short, punchy display title (e.g., "Print Spooler Crash") |
| `date_added` | Yes | ISO 8601 creation date |
| `last_updated` | Yes | ISO 8601 modification date |
| `author` | Yes | Author or team name (e.g., "Tier 1 Support") |
| `audience` | Yes | Target audience (e.g., "SysAdmin", "Help Desk") |
| `severity` | Yes | Impact level (e.g., "High", "Medium", "Low") |
| `tags` | Yes | Array of searchable keywords (must include the OS like `Windows` or `Linux`) |

**Example Document:**

```markdown
---
title: "BitLocker Recovery Key Prompt"
date_added: "2026-03-12"
last_updated: "2026-03-12"
author: "Tier 1 Support"
audience: "Help Desk"
severity: "High"
tags: ["Windows", "BitLocker", "Encryption"]
---

### Issue
User is prompted for a BitLocker recovery key at boot...
```

---

## Deployment Pipeline

This repository includes a continuous deployment pipeline configured for **GitHub Pages**. 

When code is pushed or a Pull Request is merged into the `main` branch, the `.github/workflows/deploy.yml` action automatically:
1. Provisions an Ubuntu runner.
2. Installs Python and the `requirements.txt` dependencies.
3. Executes `kb_builder.py`.
4. Uploads the `output/` directory as an artifact.
5. Deploys the static site to the GitHub Pages environment.

**Configuration:** Ensure GitHub Pages is set to use **GitHub Actions** as the source in the repository settings.

---

## Security & Operations

- **Zero-Day Resilience:** By compiling to 100% static HTML/CSS/JS, the deployed portal has no backend database, no PHP/Node.js runtime, and no dynamic server-side processing. This eliminates vulnerability to SQL injection, remote code execution (RCE), and common CMS exploits.
- **Access Control:** The live site can be deployed internally behind a corporate firewall or VPN, or authenticated via Cloudflare Access / Entra ID Application Proxy if hosted externally.
- **GitOps Driven:** All documentation changes go through standard Git workflows. Incorrect or malicious edits can be reverted instantly via standard Git commands.

---

## License

MIT
