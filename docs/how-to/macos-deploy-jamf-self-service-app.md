---
title: "Deploy Mac App via Jamf Self Service"
author: "Tier 1 Support"
category: "How-To Guides"
last_updated: "2026-05-21"
kb_id: "HOW-260809234827"
tags: ["macOS", "Jamf", "Software"]
---

## Summary[¶](#summary "Permanent link")

Instructions for instructing users on how to install authorized enterprise applications through the Jamf Self Service portal on macOS.

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

* Ensure the requested software is actually scoped to the user’s department in Jamf Pro.

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

1. **Open Jamf Self Service:**
2. Instruct the user to press `Cmd + Space` to open Spotlight.
3. Type “Self Service” and press Enter.
4. Alternatively, navigate to **Applications > Self Service.app**.
5. **Locate the Application:**
6. Use the search bar in the top right corner of Self Service to find the software (e.g., “Slack”, “Adobe Creative Cloud”).
7. Browse the categories on the left sidebar if the name is unknown.
8. **Install and Authorize:**
9. Click the **Install** button next to the application.
10. Wait for the progress bar to complete. The app is downloaded and silently installed via the Jamf binary.
11. No local admin credentials are required for Self Service installations, as they execute as root via the MDM profile.
12. **Troubleshoot Stalled Installations:**  
    If the installation hangs on “Downloading”:
13. Ask the user to cancel the install and click the “Refresh” (Cmd + R) button in Self Service.
14. If that fails, escalate to run `sudo jamf policy` via Terminal or Jamf Remote.