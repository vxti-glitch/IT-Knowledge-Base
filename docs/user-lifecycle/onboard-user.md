---
title: "Onboard a user across Active Directory and Microsoft 365"
author: "Tier 1 Support Lab"
category: "User Lifecycle"
article_type: "Runbook"
last_updated: "2026-08-26"
evidence_status: "concept_reviewed"
kb_id: "KB-LIFECYCLE-001"
tags: ["Onboarding", "Active Directory", "Microsoft 365", "Licensing"]
platforms: ["Active Directory", "Microsoft 365", "Windows 11"]
support_tier: "Tier 1 with delegated role"
risk: "High"
---

## Summary

Turn an approved onboarding request into a validated identity, license, group-membership, device, and first-sign-in checklist without copying excessive access from another user.

## Scope and safety

An approved request is required before account creation or licensing. Use least privilege, separate requester approval from technician execution, and never copy all group memberships from a reference user. Temporary passwords must be generated and delivered through the approved secure process.

## Symptoms or trigger

- An approved new-hire or contractor request reaches the service desk.
- A start date requires identity, device, and application readiness.
- A manager reports missing baseline access after creation.

## Information to collect

- Approved legal/display name and username standard
- Start date, manager, department, role, and employment type
- Required license and approved applications
- Approved security and distribution groups
- Device, location, and remote-work requirements
- Expiration date for temporary or contractor access

## Diagnostic steps

Confirm the proposed username and email address are not already assigned. In a fictional AD lab, preview account creation before applying it:

```powershell
Get-ADUser -Filter "SamAccountName -eq 'test.user'"

New-ADUser `
    -Name "Test User" `
    -SamAccountName "test.user" `
    -UserPrincipalName "test.user@example.test" `
    -Path "OU=Lab Users,DC=example,DC=test" `
    -Enabled $true `
    -ChangePasswordAtLogon $true `
    -WhatIf
```

Review every approved group individually and confirm the required license is available.

## Resolution or next action

1. Create the identity through the approved system.
2. Set manager, department, role, and expiration attributes.
3. Assign only approved groups and Microsoft 365 licenses.
4. Prepare the managed device and required applications.
5. Deliver first-sign-in instructions through the approved channel.
6. Require password change and MFA registration according to policy.

## Validation

- Account attributes match the approved request.
- Required licenses and groups are present, with no unapproved access.
- The user completes first sign-in and MFA registration.
- Email, Teams, and required business applications open.
- Asset assignment and completion evidence are recorded.

## Ticket note example

> Simulated ticket note: Completed the approved lab onboarding checklist, created the fictional identity, assigned the documented baseline groups and Microsoft 365 license, recorded the device assignment, and verified first sign-in plus MFA registration. No access was copied from another user.

## Escalation criteria

Escalate missing approval, privileged access, unavailable licenses, conflicting identities, application-owner permissions, synchronization failure, or requests that exceed the documented role baseline.

## References

- [New-ADUser — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/activedirectory/new-aduser)
- [Add users and assign licenses — Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365/admin/add-users/add-users)
