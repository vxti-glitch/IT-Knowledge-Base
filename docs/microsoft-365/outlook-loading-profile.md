---
title: "Troubleshoot Outlook stuck on Loading Profile"
author: "Tier 1 Support Lab"
category: "Microsoft 365"
article_type: "FAQ"
last_updated: "2026-08-26"
kb_id: "KB-M365-001"
tags: ["Outlook", "Microsoft 365", "Profile", "Add-ins"]
platforms: ["Windows 11", "Outlook"]
support_tier: "Tier 1"
risk: "Moderate"
---

## Summary

Separate a device-specific Outlook profile or add-in problem from a Microsoft 365 account or service issue before rebuilding local data.

## Scope and safety

Confirm whether the user runs classic Outlook or new Outlook because repair steps differ. Do not delete an OST or profile until web access and mailbox synchronization are confirmed. Preserve locally stored PST files and unsynchronized data.

## Symptoms or trigger

- Classic Outlook remains on **Loading Profile**.
- Outlook opens only in safe mode.
- Outlook on the web works while the desktop client fails.

## Information to collect

- Outlook edition and version
- Exact point where startup stops
- Whether Outlook on the web works
- Recent add-in, Office, Windows, or profile changes
- Presence of PST files or shared mailboxes

## Diagnostic steps

1. Check the Microsoft 365 service-health channel available to the technician.
2. Confirm the mailbox works in Outlook on the web.
3. Close Outlook in Task Manager and try one clean launch.
4. For classic Outlook, test safe mode:

```powershell
Start-Process outlook.exe -ArgumentList "/safe"
```

5. If safe mode works, review COM add-ins and disable only the suspected add-in for testing.
6. Use **Control Panel > Mail > Show Profiles** to inspect the profile without deleting it.

## Resolution or next action

Repair Office or create a new Outlook profile only after web access is confirmed and local data has been assessed. Set the new profile as a temporary prompt choice, open Outlook, and allow mailbox synchronization to complete before removing the old profile.

## Validation

- Outlook opens normally twice without safe mode.
- New mail sends and receives.
- Required shared mailboxes and calendars appear.
- No local PST or unsynchronized content was lost.

## Ticket note example

> Simulated ticket note: Confirmed Outlook on the web was available, reproduced classic Outlook hanging at Loading Profile, and verified safe mode opened successfully. Disabled the identified test add-in, restarted Outlook normally twice, and confirmed mail flow.

## Escalation criteria

Escalate when web access also fails, multiple users are affected, mailbox licensing is uncertain, local-only data is at risk, Office repair fails, or the problem returns with all add-ins disabled.

## References

- [Outlook not responding or stuck — Microsoft Support](https://support.microsoft.com/en-us/office/outlook-not-responding-stuck-at-processing-stopped-working-freezes-or-hangs-5c313d04-64af-4441-82d2-44e5a43eee5a)
- [Create an Outlook profile — Microsoft Support](https://support.microsoft.com/en-us/office/create-an-outlook-profile-f544c1ba-3352-4b3b-be0b-8d42a540459d)
