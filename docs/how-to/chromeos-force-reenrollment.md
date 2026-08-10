---
title: Force Re-enrollment for ChromeOS
kb_id: HOW-260809234827
author: Tier 1 Support
category: How-To Guides
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: High
tags:
- ChromeOS
- Enrollment
---

## Summary
Instructions on how to force a ChromeOS device to re-enroll into enterprise management if it has been wiped or deprovisioned improperly.

## Prerequisites for Tier 1 Technicians
- Physical access to the Chromebook.
- Enterprise enrollment credentials.

## Diagnostic Steps

1. **Trigger Developer Mode Wipe (If necessary):**
   If the device is stuck in a weird state, perform a wipe by pressing `Esc + Refresh + Power`. When the recovery screen appears, press `Ctrl + D`, then press `Enter` to turn OS verification off, and space to turn it back on. This completely wipes the device.

2. **Reach the Welcome Screen:**
   - Proceed through the initial setup screens until you reach the standard Google login prompt. DO NOT log in with a personal account.

3. **Invoke Enterprise Enrollment:**
   - At the login screen, press `Ctrl + Alt + E`.
   - The screen will change to the Enterprise Enrollment portal.

4. **Authenticate:**
   - Enter your enterprise admin credentials or a dedicated enrollment service account.
   - Once successful, the device will pull down all MDM policies and return to the managed login screen.
