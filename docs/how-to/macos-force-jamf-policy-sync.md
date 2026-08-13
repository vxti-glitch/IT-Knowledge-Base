---
title: "Force Jamf Policy Sync"
author: "Tier 1 Support"
category: "How-To Guides"
last_updated: "2026-05-22"
kb_id: "HOW-260809234827"
tags: ["macOS", "Jamf", "MDM"]
---

## Summary[¶](#summary "Permanent link")

How to manually force a macOS device to check in with the Jamf Pro server to download new profiles, policies, or software updates.

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

* Terminal access on the affected Mac.
* The Jamf binary must be installed.

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

1. **Force Policy Execution:**  
   Run the standard Jamf check-in command. This triggers any policies scoped to “Ongoing” or “Check-in”.  
   `bash
   sudo jamf policy`
2. **Force Reconnaissance (Inventory Sync):**  
   If you recently changed the computer’s extension attributes or smart group criteria in the Jamf console, force the Mac to submit a fresh inventory report.  
   `bash
   sudo jamf recon`
3. **Manage MDM Framework:**  
   If configuration profiles are failing to install, you can restart the MDM framework communication.  
   `bash
   sudo jamf manage`
4. **Check Jamf Logs for Errors:**  
   If policies still fail, check the local Jamf log for specific HTTP or script errors.  
   `bash
   tail -n 50 /var/log/jamf.log`