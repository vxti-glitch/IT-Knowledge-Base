# Enterprise IT Knowledge Base Generator

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=flat-square) [![Build and test](https://github.com/vxti-glitch/IT-Knowledge-Base/actions/workflows/ci.yml/badge.svg)](https://github.com/vxti-glitch/IT-Knowledge-Base/actions/workflows/ci.yml) ![Output](https://img.shields.io/badge/Output-Static%20HTML%2FCSS%2FJS-success.svg?style=flat-square)

A Python static-site generator for IT help-desk and system-administration documentation. It compiles Markdown troubleshooting guides into a searchable, responsive HTML portal that can be reviewed locally or deployed as static files.

> **Portfolio boundary:** The organizations, systems, incidents, and support procedures in the sample articles are fictional lab material. They are documentation examples, not production runbooks or employment records. Validate commands, permissions, and vendor guidance before using any procedure in a real environment.

- [Business Value](#business-value)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [How to Use](#how-to-use)
- [Markdown Schema](#markdown-schema)
- [Deployment Pipeline](#deployment-pipeline)
- [Security & Operations](#security--operations)

---

## Business Value

This project models a lightweight documentation workflow in which Markdown is the source of truth and every change can be reviewed in Git. The generated site provides client-side search, categories, article metadata, and static deployment without requiring a database or server-side application.

The portfolio value is the workflow itself: consistent article metadata, repeatable builds, searchable output, automated tests, and reviewable documentation changes. No unsupported time-savings, performance, cost, or production-usage claims are made.

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

Run the automated parser and build tests:

```bash
python -m unittest discover -s tests -v
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
| `category` | Yes | `FAQ` or `How-To Guides` |
| `last_updated` | No | ISO 8601 modification date; displayed as `Unknown` if omitted |
| `author` | No | Author or team name (for example, `Tier 1 Support`) |
| `tags` | No | Array or comma-separated list of searchable keywords |
| `severity` | No | Impact level such as `High`, `Medium`, or `Low` |
| `kb_id` | No | Optional internal article identifier |

**Example Document:**

```markdown
---
title: "BitLocker Recovery Key Prompt"
category: "FAQ"
last_updated: "2026-03-12"
author: "Tier 1 Support"
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

- **Reduced server-side attack surface:** The generated portal is static and does not require a database or server-side application runtime. Generated HTML and third-party dependencies must still be reviewed and maintained.
- **Access Control:** The live site can be deployed internally behind a corporate firewall or VPN, or authenticated via Cloudflare Access / Entra ID Application Proxy if hosted externally.
- **GitOps Driven:** Documentation changes can be reviewed through pull requests and reverted through Git history.
