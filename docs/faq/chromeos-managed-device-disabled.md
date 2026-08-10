---
title: ChromeOS Managed Device Disabled
kb_id: FAQ-260809234827
author: Tier 1 Support
category: FAQ
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: High
tags:
- ChromeOS
- Enrollment
---

## Summary
A user attempts to log into a ChromeOS device but encounters a screen stating "This device has been disabled by the administrator."

## Prerequisites for Tier 1 Technicians
- Access to the Google Admin console.
- Knowledge of the organization's device lifecycle policy.

## Diagnostic Steps

1. **Verify Device Status in Google Admin:**
   Search for the device by Serial Number in the Google Admin console.
   - Go to **Devices > Chrome > Devices**.
   - Check the `Status` field. It will likely show as `Disabled`.

2. **Determine Reason for Disablement:**
   Devices are typically disabled when marked as lost, stolen, or retired.
   - Review the device audit log to see which admin disabled the device and the provided reason.

3. **Re-enable the Device (If Authorized):**
   If the device was mistakenly disabled or has been recovered:
   - Select the device in the Google Admin console.
   - Click the **Re-enable** button.
   - Reboot the device. It should now allow enrollment or login.

4. **Force Re-sync on the Device:**
   If the device still shows disabled after re-enabling in the console, connect it to an open network and allow it to sync policy.
