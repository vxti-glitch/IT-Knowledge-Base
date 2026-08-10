---
title: Setup ChromeOS Kiosk Mode
kb_id: HOW-260809234827
author: Tier 1 Support
category: How-To Guides
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: Medium
tags:
- ChromeOS
- Kiosk
---

## Summary
This guide outlines the procedure to configure a ChromeOS device for Single App Kiosk Mode, locking the device to a specific application (e.g., a digital signage app or testing software).

## Prerequisites for Tier 1 Technicians
- Google Workspace Admin privileges (Device Management).
- The Kiosk App ID from the Chrome Web Store.

## Diagnostic Steps

1. **Move Device to Kiosk OU:**
   - In Google Admin, navigate to **Devices > Chrome > Devices**.
   - Select the target device and move it to the dedicated Kiosk Organizational Unit.

2. **Configure App & Extensions:**
   - Go to **Devices > Chrome > Apps & extensions > Kiosks**.
   - Select the Kiosk OU from the left pane.
   - Click the yellow **+** button to add an app by ID or from the Web Store.

3. **Set Auto-Launch:**
   - Once the app is added, click on it and change the `Installation policy` to **Installed**.
   - At the top of the app list, locate the `Auto-launch app` dropdown and select the newly added app.

4. **Verify Device Policies:**
   - Reboot the Chromebook.
   - It should automatically connect to the network, pull the policy, and launch the application without requiring a user login.
