---
title: "Offboard a user from Microsoft 365 and managed access"
author: "Tier 1 Support Lab"
category: "User Lifecycle"
article_type: "Runbook"
last_updated: "2026-08-26"
evidence_status: "concept_reviewed"
kb_id: "KB-LIFECYCLE-002"
tags: ["Offboarding", "Microsoft 365", "Access Removal", "Data Retention"]
platforms: ["Microsoft 365", "Microsoft Entra ID", "Active Directory"]
support_tier: "Tier 1 with delegated role"
risk: "High"
---

## Summary

Disable access at the approved time, preserve business data according to retention requirements, recover assets, and document every handoff before account deletion is considered.

## Scope and safety

Offboarding requires an authorized request and effective time. Do not delete the user, mailbox, OneDrive data, or legal-hold content during initial access removal. Confidential termination details should not be copied into general ticket notes.

## Symptoms or trigger

- Human Resources or an authorized manager submits a separation request.
- A contractor reaches the approved access-expiration date.
- Emergency access revocation is requested through the security process.

## Information to collect

- Approved requester and effective date/time with time zone
- User principal name and asset assignments
- Manager or data recipient
- Mailbox, OneDrive, shared files, and application ownership
- Retention, legal-hold, and forwarding requirements
- Group, role, VPN, badge, and third-party access

## Diagnostic steps

1. Match the request to the correct identity and employment record.
2. Inventory assigned devices, licenses, groups, roles, and owned resources.
3. Confirm whether retention or legal review changes the standard sequence.
4. Identify application owners required for non-Microsoft access removal.

## Resolution or next action

At the approved effective time:

1. Block sign-in and revoke active sessions through authorized controls.
2. Reset credentials when the approved process requires it.
3. Remove privileged roles, remote access, and group memberships in the defined order.
4. Preserve or transfer mailbox and OneDrive data according to retention instructions.
5. Recover or remotely secure managed assets through the assigned device team.
6. Remove licenses only after data-retention consequences are reviewed.
7. Keep deletion as a separate, retention-controlled action.

## Validation

- Interactive sign-in is blocked and sessions are revoked.
- Required data access is transferred to the approved recipient.
- Privileged, VPN, and application access removal is confirmed.
- Asset recovery or remote-security status is recorded.
- Retention and license actions match the request.

## Ticket note example

> Simulated ticket note: Executed the fictional offboarding checklist at the approved time, blocked sign-in, revoked sessions, removed documented access, preserved mailbox and OneDrive data for the approved manager, and transferred the asset task to Endpoint Management. No account or retained data was deleted.

## Escalation criteria

Escalate emergency separations, privileged identities, legal holds, unclear data ownership, inaccessible devices, third-party application ownership, failed session revocation, or any conflict between deletion and retention instructions.

## References

- [Remove a former employee — Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365/admin/add-users/remove-former-employee)
- [Revoke user access in an emergency — Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access)
