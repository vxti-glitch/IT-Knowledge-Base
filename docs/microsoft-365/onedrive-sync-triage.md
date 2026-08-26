---
title: "Triage OneDrive files that are not syncing"
author: "Tier 1 Support Lab"
category: "Microsoft 365"
article_type: "FAQ"
last_updated: "2026-08-26"
kb_id: "KB-M365-003"
tags: ["OneDrive", "Microsoft 365", "File Sync", "Remote Support"]
platforms: ["Windows 11", "OneDrive"]
support_tier: "Tier 1"
risk: "Moderate"
---

## Summary

Identify whether a OneDrive problem affects one file, one device, the user's account, or the service before resetting or unlinking the client.

## Scope and safety

Do not delete local files, unlink the computer, or change Known Folder Move configuration until sync state and backup location are understood. A green check icon does not by itself prove every required file is available online.

## Symptoms or trigger

- Files remain in **Sync pending** or display a red error icon.
- Changes appear on the web but not on one computer.
- OneDrive reports storage, filename, permission, or sign-in errors.

## Information to collect

- Exact icon and error text
- One file, one folder, or all content affected
- Whether the file exists at OneDrive on the web
- Available local disk and cloud storage
- Filename, full path length, size, and file type

## Diagnostic steps

1. Check OneDrive on the web and the available Microsoft 365 service-health channel.
2. Select the OneDrive cloud icon and review **View sync problems**.
3. Confirm the user is signed into the expected organizational account.
4. Check storage capacity and Windows date/time.
5. Test a small, newly created text file in a known synced folder.
6. Review unsupported characters, path length, permissions, and whether another application has the file locked.

## Resolution or next action

Resolve the specific file or storage error first. Pause and resume synchronization, then restart OneDrive. Use the Microsoft-supported OneDrive reset only after confirming web copies and local-only content; unlinking the computer is a later step requiring additional review.

## Validation

- The test file appears on the web and on the workstation.
- Required files show a current synchronized state.
- No local-only folder was removed or redirected.
- The original error no longer appears.

## Ticket note example

> Simulated ticket note: Confirmed OneDrive web access and isolated the failure to one filename with an unsupported character. Renamed the file with user approval, observed successful synchronization, and verified the updated file from the web portal.

## Escalation criteria

Escalate suspected data loss, Known Folder Move policy conflicts, widespread service impact, permission errors on shared libraries, tenant storage issues, or sync failures that persist after supported client repair.

## References

- [Fix OneDrive sync problems — Microsoft Support](https://support.microsoft.com/en-us/office/fix-onedrive-sync-problems-0899b115-05f7-45ec-95b2-e4cc8c4670b2)
- [Restrictions and limitations in OneDrive and SharePoint — Microsoft Support](https://support.microsoft.com/en-us/office/restrictions-and-limitations-in-onedrive-and-sharepoint-64883a5d-228e-48f5-b3d2-eb39e07630fa)
