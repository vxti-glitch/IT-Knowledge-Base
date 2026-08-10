---
title: Deploy Mac App via Jamf Self Service
kb_id: HOW-260809234827
author: Tier 1 Support
category: How-To Guides
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: Medium
tags:
- macOS
- Jamf
- Software
---

## Summary
Instructions for instructing users on how to install authorized enterprise applications through the Jamf Self Service portal on macOS.

## Prerequisites for Tier 1 Technicians
- Ensure the requested software is actually scoped to the user's department in Jamf Pro.

## Diagnostic Steps

1. **Open Jamf Self Service:**
   - Instruct the user to press `Cmd + Space` to open Spotlight.
   - Type "Self Service" and press Enter.
   - Alternatively, navigate to **Applications > Self Service.app**.

2. **Locate the Application:**
   - Use the search bar in the top right corner of Self Service to find the software (e.g., "Slack", "Adobe Creative Cloud").
   - Browse the categories on the left sidebar if the name is unknown.

3. **Install and Authorize:**
   - Click the **Install** button next to the application.
   - Wait for the progress bar to complete. The app is downloaded and silently installed via the Jamf binary.
   - No local admin credentials are required for Self Service installations, as they execute as root via the MDM profile.

4. **Troubleshoot Stalled Installations:**
   If the installation hangs on "Downloading":
   - Ask the user to cancel the install and click the "Refresh" (Cmd + R) button in Self Service.
   - If that fails, escalate to run `sudo jamf policy` via Terminal or Jamf Remote.
