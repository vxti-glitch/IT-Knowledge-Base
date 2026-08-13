---
title: "macOS FileVault Recovery Procedures"
author: "Tier 1 Support"
category: "FAQ"
last_updated: "2026-05-13"
kb_id: "FAQ-060"
tags: ["macOS", "Encryption", "Security"]
---

## Summary[¶](#summary "Permanent link")

A macOS FileVault Recovery Procedures issue reporting a “Sync Error” or “Not Managed” status does not guarantee that the user’s account is locked. The system may be functional at the OS layer while Secure Enclave desyncs, Jamf MDM profile failures, or Keychain corruption prevent successful operation. This article covers the most common causes and their resolution paths for macOS enterprise environments.

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

Before proceeding, confirm the following from the user:  
- Mac model (Intel vs Apple Silicon) and macOS version (e.g., Sonoma, Ventura)  
- Whether they are on a corporate-managed Jamf device or BYOD  
- Which specific keychain or preference pane they cannot access  
- Whether the issue started after a specific event (password sync via Platform SSO, OS upgrade, FileVault enablement)

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

Step 1 — Test MDM Enrollment and Profile Status  
Instruct the user to open Terminal and run:  
`profiles status -type enrollment`  
If the output indicates “Enrolled via DEP: Yes” and “MDM enrollment: Yes (User Approved)”, but software isn’t installing, the issue is likely a stalled Jamf agent, not the APNs connection.

Step 2 — Check Local FileVault and Keychain State  
Run the following to check encryption:  
`fdesetup status`  
After connecting, the output should show:  
- FileVault is On.  
If keychain prompts repeatedly appear, run `security lock-keychain` and then attempt to unlock it. If the local password and AD password have diverged, the login keychain must be reset or synced via NoMAD/Jamf Connect.

## When to Escalate to Tier 2 (Mac Admins)[¶](#when-to-escalate-to-tier-2-mac-admins "Permanent link")

Escalate if any of the following are true:  
- `sudo jamf manage` confirms the agent exists but communication with the JSS times out repeatedly  
- Platform SSO is correctly configured but Kerberos tickets fail to renew after waking from sleep  
- Multiple Macs on the same OS version are reporting the same macOS FileVault Recovery Procedures issue simultaneously