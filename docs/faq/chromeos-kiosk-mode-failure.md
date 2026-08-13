---
title: "ChromeOS Kiosk Mode Startup Failure"
author: "Tier 1 Support"
category: "FAQ"
last_updated: "2026-02-11"
kb_id: "FAQ-260809234827"
tags: ["ChromeOS", "Kiosk"]
---

## Summary[¶](#summary "Permanent link")

A managed ChromeOS device configured for Kiosk Mode fails to launch the kiosk app at startup, instead dropping back to the standard login screen or displaying an application crash error.

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

* Access to the Google Admin console.
* The Device ID or Serial Number of the affected Chromebook.

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

1. **Verify Kiosk App Assignment:**  
   Check the Google Admin console to ensure the correct kiosk app is assigned to the Organizational Unit (OU) where the device resides.
2. Navigate to **Devices > Chrome > Apps & extensions > Kiosks**.
3. Confirm the app status is set to “Auto-launch app”.
4. **Check Device Network Connectivity:**  
   Kiosk apps often require network connectivity to launch or authenticate. If the device cannot reach the network, the app may crash.
5. Verify that the device is connected to the correct SSID and that network policies are applied at the device level, not the user level.
6. **Examine Device Logs:**  
   To pull logs from the affected device:  
   `bash
   # On the ChromeOS device, navigate to chrome://network for network logs, or:
   file:///var/log/messages`  
   Look for app execution failures or missing dependencies.
7. **Clear Device Data:**  
   If the app data is corrupted, clearing device profiles can resolve it:
8. In Google Admin, select the device.
9. Click **Clear user profiles**.
10. Reboot the device to force a fresh download of the kiosk app.