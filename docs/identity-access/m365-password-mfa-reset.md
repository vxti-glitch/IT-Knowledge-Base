---
title: "Reset a Microsoft 365 password and require MFA registration"
author: "Tier 1 Support Lab"
category: "Identity & Access"
article_type: "How-To"
last_updated: "2026-08-26"
kb_id: "KB-IDENTITY-002"
tags: ["Microsoft 365", "Entra ID", "Password Reset", "MFA"]
platforms: ["Microsoft 365", "Microsoft Entra ID"]
support_tier: "Tier 1 with delegated role"
risk: "High"
---

## Summary

Model a controlled password reset and MFA re-registration for a verified Microsoft 365 user when the technician has the required delegated role.

## Scope and safety

Never reset credentials based only on an email or chat message. Verify the requester through the approved process, use the least-privileged administrative role, and do not read or disclose existing authentication methods. A suspected compromise follows the security-escalation process, not a routine reset alone.

## Symptoms or trigger

- The user forgot the password or cannot complete MFA.
- The user replaced or lost an authenticator device.
- Authentication methods are registered to an unavailable device.

## Information to collect

- Verified user principal name
- Approved identity-verification result
- Whether the password is forgotten, expired, or suspected compromised
- Whether any usable MFA method remains
- Business impact and required completion time

## Diagnostic steps

1. Locate the user in the Microsoft 365 admin center or Microsoft Entra admin center.
2. Confirm the account is enabled and the requested action is within the technician's role.
3. Review only the status needed to distinguish password failure from MFA registration failure.
4. If compromise is suspected, stop and use the security-escalation runbook.

## Resolution or next action

1. Generate a temporary password through the approved admin interface.
2. Require the user to change it at the next sign-in.
3. Deliver the temporary credential through the approved secure channel.
4. If authorized, select **Require re-register multifactor authentication** for the user.
5. Direct the user to the organization's approved security-info registration page.

Do not disable MFA as a shortcut.

## Validation

- Confirm the temporary password is changed by the user.
- Confirm the user registers an approved MFA method.
- Confirm one successful sign-in to an approved Microsoft 365 service.
- Record only the result, not authentication secrets.

## Ticket note example

> Simulated ticket note: Completed approved identity verification, issued a temporary Microsoft 365 password, required password change at next sign-in, required MFA re-registration, and confirmed successful access to the Microsoft 365 portal. No authentication secrets were recorded.

## Escalation criteria

Escalate suspected compromise, privileged accounts, unavailable delegated permissions, Conditional Access blocks, repeated registration failure, or any request to bypass MFA policy.

## References

- [Reset a user's password — Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365/admin/add-users/reset-passwords)
- [Manage user authentication methods — Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-userdevicesettings)
