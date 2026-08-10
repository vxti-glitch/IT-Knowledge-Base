---
author: Tier 1 Support
category: FAQ
date_added: '2026-01-22'
kb_id: FAQ-052
last_updated: '2026-06-11'
severity: High
short_title: Workstation Trust Relationship Failed
tags:
- Active Directory
- Authentication
- Windows
target_audience: SysAdmin
title: Workstation Trust Relationship Failed
---


## Summary
A Workstation Trust Relationship Failed failure reporting an "Access Denied" or "Not Found" status does not guarantee that the object is missing. The identity service may be functional at the domain controller layer while replication, SPN mismatches, or cached credentials prevent successful authentication. This article covers the most common causes and their resolution paths for Active Directory environments.

## Prerequisites for Tier 1 Technicians
Before proceeding, confirm the following from the user or system:
- Exact username, hostname, and OS version
- Whether the machine has line-of-sight to a Domain Controller
- Which specific Active Directory resource or policy is failing
- Whether the issue started after a specific event (password change, OU move, network change)

## Diagnostic Steps

Step 1 — Verify Secure Channel and Trust
Instruct the user or use remote PowerShell to run:
`Test-ComputerSecureChannel -Verbose`
If this returns False, the machine password has fallen out of sync with AD. Run with `-Repair` and `-Credential` to fix it without unjoining the domain.

Step 2 — Check Authentication and Replication State
Run the following to check logon servers and policies:
`nltest /dsgetdc:domain.local`
`gpresult /r /SCOPE COMPUTER`
The output should show:
- DC Name: \\DC01.domain.local
- Applied Group Policy Objects: Ensure the expected GPOs are listed.
If it shows "N/A" or points to an offline DC, the client is caching stale site information.

## When to Escalate to Tier 2 (Identity & AD)
Escalate if any of the following are true:
- `repadmin /showrepl` on the Domain Controllers shows RPC failures or replication topologies are broken
- The secure channel is correctly configured but Kerberos tickets (TGTs) are failing to issue
- Multiple users across different OUs are reporting the same Workstation Trust Relationship Failed issue simultaneously