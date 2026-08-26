---
title: "Reset the Microsoft Teams desktop client safely"
author: "Tier 1 Support Lab"
category: "Microsoft 365"
article_type: "How-To"
last_updated: "2026-08-26"
kb_id: "KB-M365-002"
tags: ["Microsoft Teams", "Microsoft 365", "Cache", "Sign-in"]
platforms: ["Windows 11", "Microsoft Teams"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

Reset a malfunctioning Teams desktop client after confirming that the account and Teams web application remain available.

## Scope and safety

This procedure targets client-side state, not tenant configuration. Confirm the installed Teams edition and preserve unsent user content. Use the Windows app reset option instead of deleting undocumented folders whenever possible.

## Symptoms or trigger

- Teams opens to a blank screen or sign-in loop.
- Presence or chat updates remain stale on one device.
- Teams on the web works while the desktop app fails.

## Information to collect

- Windows and Teams versions
- Exact error and time observed
- Whether Teams on the web works
- Whether one user, one device, or multiple users are affected
- Recent update or account change

## Diagnostic steps

1. Check the support channel for a known Teams service incident.
2. Test the same account in Teams on the web.
3. Sign out of Teams if the interface is responsive.
4. Quit Teams from the notification area and confirm its processes close in Task Manager.
5. Reopen once before performing a reset.

## Resolution or next action

On Windows 11, open **Settings > Apps > Installed apps > Microsoft Teams > Advanced options**. Select **Repair** first. If the problem remains, select **Reset**, reopen Teams, and sign in through the approved organizational flow.

## Validation

- Teams opens without a blank screen or loop.
- A test chat updates in both web and desktop clients.
- Calendar and presence data refresh.
- Required audio devices remain selectable.

## Ticket note example

> Simulated ticket note: Confirmed Teams web access and isolated the issue to one Windows desktop client. Closed Teams, used the supported Windows app repair/reset sequence, signed the user back in, and verified chat synchronization and calendar display.

## Escalation criteria

Escalate when Teams web also fails, multiple users are affected, Conditional Access blocks sign-in, required meeting features remain unavailable, or app repair/reset does not resolve the client issue.

## References

- [Clear the Teams client cache — Microsoft Learn](https://learn.microsoft.com/en-us/troubleshoot/microsoftteams/teams-administration/clear-teams-cache)
- [Repair apps and programs in Windows — Microsoft Support](https://support.microsoft.com/en-us/windows/repair-apps-and-programs-in-windows-e90eefe4-d0a2-7c1b-dd59-949a9030f317)
