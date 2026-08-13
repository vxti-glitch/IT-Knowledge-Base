---
title: "Spotlight Search Not Finding Applications"
author: "Tier 1 Support"
category: "FAQ"
last_updated: "2026-04-15"
kb_id: "FAQ-260809234827"
tags: ["macOS", "Spotlight"]
---

## Summary[¶](#summary "Permanent link")

Users report that macOS Spotlight (Cmd + Space) fails to find installed applications, documents, or returns partial/inaccurate results.

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

* Admin access to the affected Mac (via Jamf Remote or local admin credentials).

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

1. **Check Spotlight Privacy Settings:**  
   Ensure the Macintosh HD is not accidentally excluded from Spotlight.
2. Open **System Settings > Siri & Spotlight > Spotlight Privacy**.
3. If the main drive or Applications folder is listed, remove it.
4. **Force Spotlight Reindexing (GUI):**
5. Add the entire `Macintosh HD` to the Privacy tab.
6. Close System Settings.
7. Reopen the Privacy tab and remove `Macintosh HD`. This triggers a reindex.
8. **Force Spotlight Reindexing (CLI):**  
   If the GUI method fails or you are working remotely, use `mdutil`.  
   `bash
   # Turn off indexing
   sudo mdutil -i off /
   # Erase the current index
   sudo mdutil -E /
   # Turn indexing back on
   sudo mdutil -i on /`
9. **Verify Indexing Status:**  
   Check if the system is currently building the index.  
   `bash
   sudo mdutil -s /`  
   *Note: Indexing can take anywhere from 15 minutes to an hour depending on disk speed and size.*