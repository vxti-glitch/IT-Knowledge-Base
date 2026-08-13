---
title: "Force Re-enrollment for ChromeOS"
author: "Tier 1 Support"
category: "How-To Guides"
last_updated: "2026-05-04"
kb_id: "HOW-260809234827"
tags: ["ChromeOS", "Enrollment"]
---

## Summary[¶](#summary "Permanent link")

Instructions on how to force a ChromeOS device to re-enroll into enterprise management if it has been wiped or deprovisioned improperly.

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

* Physical access to the Chromebook.
* Enterprise enrollment credentials.

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

1. **Trigger Developer Mode Wipe (If necessary):**  
   If the device is stuck in a weird state, perform a wipe by pressing `Esc + Refresh + Power`. When the recovery screen appears, press `Ctrl + D`, then press `Enter` to turn OS verification off, and space to turn it back on. This completely wipes the device.
2. **Reach the Welcome Screen:**
3. Proceed through the initial setup screens until you reach the standard Google login prompt. DO NOT log in with a personal account.
4. **Invoke Enterprise Enrollment:**
5. At the login screen, press `Ctrl + Alt + E`.
6. The screen will change to the Enterprise Enrollment portal.
7. **Authenticate:**
8. Enter your enterprise admin credentials or a dedicated enrollment service account.
9. Once successful, the device will pull down all MDM policies and return to the managed login screen.