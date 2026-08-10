---
title: Spotlight Search Not Finding Applications
kb_id: FAQ-260809234827
author: Tier 1 Support
category: FAQ
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: Low
tags:
- macOS
- Spotlight
---

## Summary
Users report that macOS Spotlight (Cmd + Space) fails to find installed applications, documents, or returns partial/inaccurate results.

## Prerequisites for Tier 1 Technicians
- Admin access to the affected Mac (via Jamf Remote or local admin credentials).

## Diagnostic Steps

1. **Check Spotlight Privacy Settings:**
   Ensure the Macintosh HD is not accidentally excluded from Spotlight.
   - Open **System Settings > Siri & Spotlight > Spotlight Privacy**.
   - If the main drive or Applications folder is listed, remove it.

2. **Force Spotlight Reindexing (GUI):**
   - Add the entire `Macintosh HD` to the Privacy tab.
   - Close System Settings.
   - Reopen the Privacy tab and remove `Macintosh HD`. This triggers a reindex.

3. **Force Spotlight Reindexing (CLI):**
   If the GUI method fails or you are working remotely, use `mdutil`.
   ```bash
   # Turn off indexing
   sudo mdutil -i off /
   # Erase the current index
   sudo mdutil -E /
   # Turn indexing back on
   sudo mdutil -i on /
   ```

4. **Verify Indexing Status:**
   Check if the system is currently building the index.
   ```bash
   sudo mdutil -s /
   ```
   *Note: Indexing can take anywhere from 15 minutes to an hour depending on disk speed and size.*
