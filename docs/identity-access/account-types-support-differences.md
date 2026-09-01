---
title: "Local, Active Directory, and Microsoft Entra Accounts: Support Differences"
author: "Tier 1 Support Lab"
category: "Identity & Access"
article_type: "Concept"
content_type: "Concept"
last_updated: "2026-08-30"
reviewed_on: "2026-08-30"
evidence_status: "concept_reviewed"
audience: "Technician"
difficulty: "Intermediate"
prerequisites: ["Basic Windows sign-in knowledge"]
kb_id: "KB-IDENTITY-005"
tags: ["Active Directory", "Microsoft Entra ID", "Local Account", "Identity"]
platforms: ["Windows 11", "Microsoft Entra ID", "Active Directory"]
support_tier: "Tier 1"
risk: "Moderate"
---

## Summary

Identify the account’s source of authority before resetting a password, interpreting a sign-in name, or changing access.

## Why support cares

A local Windows account belongs to one device. An on-premises Active Directory account is controlled by a domain and may be synchronized to Microsoft Entra ID. A cloud-only Entra account is managed in the tenant. Guest/external identities remain owned by another directory. The same email-looking name can therefore have different reset and authentication paths.

## Core concepts

- Sign-in forms can include `DEVICE\\user`, `DOMAIN\\user`, `user@domain`, or a Windows Hello credential tied to an identity.
- Password, PIN, MFA method, license, group membership, device join, and application authorization are separate layers.
- `whoami`, Settings > Accounts > Access work or school, and `dsregcmd /status` provide local observations; they do not authorize changes or prove tenant assignments.
- Password writeback, federation, hybrid join, and sync introduce ownership boundaries that a Tier 1 technician must document.

## Examples and boundaries

If web sign-in succeeds but Windows says the PIN is unavailable, do not reset the cloud password first. If an Entra user is synchronized from on-premises AD, the permitted reset path depends on configuration and role. External-user passwords cannot be reset by the resource tenant.

## Related procedures

Use the Microsoft 365 sign-in decision guide, account-lockout article, MFA recovery procedure, and onboarding/offboarding checklists. Verify identity before any credential or authentication-method action.

## References

- [Microsoft Entra device identity fundamentals](https://learn.microsoft.com/en-us/entra/identity/devices/overview)
- [Reset a user password](https://learn.microsoft.com/en-us/entra/fundamentals/users-reset-password-azure-portal)
