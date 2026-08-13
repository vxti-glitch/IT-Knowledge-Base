---
title: "Why does Outlook freeze when I try to open an attachment?"
author: "Tier 1 Support"
category: "FAQ"
last_updated: "2026-04-16"
kb_id: "FAQ-015"
tags: ["Email & Exchange", "Outlook", "Troubleshooting"]
---

## Summary[¶](#summary "Permanent link")

A Why does Outlook freeze when I try to open an attachment? issue reporting an “Offline” or “Disconnected” status does not guarantee that the mailbox server is down. The profile may be established at the local layer while Autodiscover resolution, OST corruption, or Modern Authentication (OAuth) tokens prevent traffic from reaching Exchange Online. This article covers the most common causes and their resolution paths for Exchange and M365 environments.

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

Before proceeding, confirm the following from the user:  
- Outlook client version (Current Channel, Monthly Enterprise, or OWA)  
- Whether they are on a corporate-managed device or BYOD  
- Which specific mailbox or calendar they cannot sync  
- Whether the issue started after a specific event (password change, M365 license change, MFA enrollment)

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

Step 1 — Test Autodiscover Resolution  
Instruct the user to open Command Prompt and run:  
`Resolve-DnsName autodiscover.domain.com`  
If the resolution by CNAME succeeds but Outlook fails, the issue is likely a local cache or credential manager conflict, not DNS.

Step 2 — Check Local Profile and OST State  
Navigate to the Outlook local app data:  
`%localappdata%\Microsoft\Outlook`  
Inspect the folder for:  
- Overly large .OST files (approaching 50GB limit)  
- Multiple .OST files indicating a corrupted profile rebuild  
If the OST is oversized, forcing a rebuild by renaming the file to `.ost.old` and restarting Outlook is the standard fix.

## When to Escalate to Tier 2 (Collaboration)[¶](#when-to-escalate-to-tier-2-collaboration "Permanent link")

Escalate if any of the following are true:  
- `Test-MapiConnectivity` or Microsoft Remote Connectivity Analyzer confirms the mailbox is unreachable from the outside  
- Autodiscover is correctly configured but Modern Auth fails to prompt for MFA  
- Multiple users on different databases are reporting the same Why does Outlook freeze when I try to open an attachment? issue simultaneously