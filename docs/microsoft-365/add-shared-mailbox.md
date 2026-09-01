---
title: "Add an authorized shared mailbox in Outlook"
author: "Tier 1 Support Lab"
category: "Microsoft 365"
article_type: "How-To"
last_updated: "2026-08-26"
evidence_status: "concept_reviewed"
kb_id: "KB-M365-004"
tags: ["Outlook", "Shared Mailbox", "Exchange Online", "Permissions"]
platforms: ["Microsoft 365", "Outlook"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

Add a shared mailbox after confirming the user has been granted the required Exchange Online permission.

## Scope and safety

A shared mailbox normally does not use a separate password for end-user access. Do not attempt to sign in directly as the mailbox or grant permissions unless that administrative action is explicitly assigned to the support role.

## Symptoms or trigger

- Access was approved but the mailbox has not appeared automatically.
- The mailbox opens, but sending as the mailbox fails.
- The user needs to open the mailbox in Outlook on the web.

## Information to collect

- User principal name and shared-mailbox address
- Approval or request record
- Required permission: Full Access, Send As, or Send on Behalf
- Outlook edition and whether web access works
- Time permission was granted

## Diagnostic steps

1. Confirm the access request is approved and completed by the authorized resolver group.
2. Allow for permission propagation according to the support process.
3. Test **Open another mailbox** in Outlook on the web.
4. Determine whether only automatic mapping is delayed or permission is actually absent.

## Resolution or next action

If web access works, restart Outlook. When automatic mapping is not expected, add the shared mailbox through the supported account settings for the installed Outlook edition. Test **From** behavior separately because Full Access does not automatically grant Send As.

## Validation

- The user can open folders in the shared mailbox.
- A test message sends only with the approved sender permission.
- The sent item appears in the expected mailbox according to policy.
- No direct mailbox password was used or requested.

## Ticket note example

> Simulated ticket note: Verified the approved Full Access and Send As request, confirmed the shared mailbox opened in Outlook on the web, added it to the desktop client after restart, and validated one approved test message.

## Escalation criteria

Escalate missing Exchange permissions, delivery restrictions, automapping configuration questions, mailbox licensing issues, or access requests without documented approval.

## References

- [Open and use a shared mailbox in Outlook — Microsoft Support](https://support.microsoft.com/en-us/office/open-and-use-a-shared-mailbox-in-outlook-d94a8e9e-21f1-4240-808b-de9c9c088afd)
- [Permissions in Exchange Online — Microsoft Learn](https://learn.microsoft.com/en-us/exchange/recipients-in-exchange-online/manage-permissions-for-recipients)
