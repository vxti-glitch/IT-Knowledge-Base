---
title: "Triage an Active Directory account lockout"
author: "Tier 1 Support Lab"
category: "Identity & Access"
article_type: "Runbook"
last_updated: "2026-08-26"
evidence_status: "concept_reviewed"
kb_id: "KB-IDENTITY-001"
tags: ["Active Directory", "Account Lockout", "Authentication", "Remote Support"]
platforms: ["Windows 11", "Active Directory"]
support_tier: "Tier 1 with escalation"
risk: "Moderate"
---

## Summary

Identify whether an Active Directory account is locked, restore access when the support role is authorized to do so, and collect useful evidence when the lockout repeats.

## Scope and safety

Verify the caller with the approved identity-check process before discussing or changing an account. Do not repeatedly unlock an account without investigating the source of bad credentials. Domain-controller event-log review and security investigation remain escalation activities unless explicitly assigned.

## Symptoms or trigger

- The user receives an account-locked message.
- Valid credentials work in one service but fail in another.
- The account locks again shortly after a password reset.

## Information to collect

- Username and verified contact method
- Exact error and first observed time
- Recent password change time
- Devices, phones, mapped drives, VPN clients, and scheduled tasks using the account
- Whether the user can sign in to any approved service

## Diagnostic steps

From an authorized workstation with the Active Directory module, inspect the account without changing it:

```powershell
Get-ADUser -Identity "test.user" -Properties LockedOut, Enabled, PasswordLastSet |
    Select-Object SamAccountName, Enabled, LockedOut, PasswordLastSet
```

Check whether other accounts are locked only if that query is within the technician's approved scope:

```powershell
Search-ADAccount -LockedOut -UsersOnly
```

Ask whether an old password remains saved in Outlook, a phone, Windows Credential Manager, a VPN client, a mapped drive, or a scheduled task.

## Resolution or next action

If identity verification is complete, the account is enabled, and the service-desk role permits unlocking, use:

```powershell
Unlock-ADAccount -Identity "test.user" -Confirm
```

Have the user update saved credentials on every known device. If a password reset is also required, follow the separate password-reset procedure and require a change at next sign-in according to policy.

## Validation

- Recheck the `LockedOut` property.
- Ask the user to sign in once to an approved service.
- Confirm the account stays available during the observation period defined by the support process.

## Ticket note example

> Simulated ticket note: Verified the caller, confirmed the AD account was enabled but locked, recorded the recent password-change time and affected devices, performed the authorized unlock, and confirmed one successful sign-in. Advised the user to replace saved credentials on the VPN client and phone.

## Escalation criteria

Escalate when the account repeatedly relocks, multiple users are affected, privileged or service accounts are involved, the caller cannot be verified, or domain-controller/security-log analysis is required.

## References

- [Unlock-ADAccount — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/activedirectory/unlock-adaccount)
- [Search-ADAccount — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/activedirectory/search-adaccount)
