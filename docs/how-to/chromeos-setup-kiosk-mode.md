---
title: "Setup ChromeOS Kiosk Mode"
author: "Tier 1 Support"
category: "How-To Guides"
last_updated: "2026-05-27"
kb_id: "HOW-260809234827"
tags: ["ChromeOS", "Kiosk"]
---

## Summary[¶](#summary "Permanent link")

This guide outlines the procedure to configure a ChromeOS device for Single App Kiosk Mode, locking the device to a specific application (e.g., a digital signage app or testing software).

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

* Google Workspace Admin privileges (Device Management).
* The Kiosk App ID from the Chrome Web Store.

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

1. **Move Device to Kiosk OU:**
2. In Google Admin, navigate to **Devices > Chrome > Devices**.
3. Select the target device and move it to the dedicated Kiosk Organizational Unit.
4. **Configure App & Extensions:**
5. Go to **Devices > Chrome > Apps & extensions > Kiosks**.
6. Select the Kiosk OU from the left pane.
7. Click the yellow **+** button to add an app by ID or from the Web Store.
8. **Set Auto-Launch:**
9. Once the app is added, click on it and change the `Installation policy` to **Installed**.
10. At the top of the app list, locate the `Auto-launch app` dropdown and select the newly added app.
11. **Verify Device Policies:**
12. Reboot the Chromebook.
13. It should automatically connect to the network, pull the policy, and launch the application without requiring a user login.