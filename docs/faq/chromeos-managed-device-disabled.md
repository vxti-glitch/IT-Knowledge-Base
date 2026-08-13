---
title: "ChromeOS Managed Device Disabled"
author: "Tier 1 Support"
category: "FAQ"
last_updated: "2026-06-18"
kb_id: "FAQ-260809234827"
tags: ["ChromeOS", "Enrollment"]
---

## Summary[¶](#summary "Permanent link")

A user attempts to log into a ChromeOS device but encounters a screen stating “This device has been disabled by the administrator.”

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

* Access to the Google Admin console.
* Knowledge of the organization’s device lifecycle policy.

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

1. **Verify Device Status in Google Admin:**  
   Search for the device by Serial Number in the Google Admin console.
2. Go to **Devices > Chrome > Devices**.
3. Check the `Status` field. It will likely show as `Disabled`.
4. **Determine Reason for Disablement:**  
   Devices are typically disabled when marked as lost, stolen, or retired.
5. Review the device audit log to see which admin disabled the device and the provided reason.
6. **Re-enable the Device (If Authorized):**  
   If the device was mistakenly disabled or has been recovered:
7. Select the device in the Google Admin console.
8. Click the **Re-enable** button.
9. Reboot the device. It should now allow enrollment or login.
10. **Force Re-sync on the Device:**  
    If the device still shows disabled after re-enabling in the console, connect it to an open network and allow it to sync policy.