---
title: "Handle an approved software installation blocked by permissions"
author: "Tier 1 Support Lab"
category: "Windows Endpoint"
article_type: "Runbook"
last_updated: "2026-08-26"
kb_id: "KB-WINDOWS-003"
tags: ["Windows 11", "Software Installation", "Permissions", "Application Control"]
platforms: ["Windows 11", "Intune"]
support_tier: "Tier 1 intake"
risk: "High"
---

## Summary

Confirm that requested software is approved and identify the control blocking installation without sharing administrator credentials or bypassing security policy.

## Scope and safety

Do not disable antivirus, application control, SmartScreen, or User Account Control. Never enter or disclose an administrator password for an unapproved installer. Software approval and privileged installation must follow the organization's documented process.

## Symptoms or trigger

- Windows requests administrator credentials.
- Company Portal or Software Center reports a failed installation.
- SmartScreen or application control blocks the package.

## Information to collect

- Application, version, publisher, and business purpose
- Approved request or catalog entry
- Installer source and filename
- Exact error, timestamp, and deployment method
- Device asset and management status

## Diagnostic steps

1. Search the approved software catalog for the application.
2. Confirm the installer came from the approved source.
3. Record the digital-signature status without executing the file:

```powershell
Get-AuthenticodeSignature -FilePath "C:\ApprovedPath\installer.exe" |
    Select-Object Status, StatusMessage, SignerCertificate
```

4. Review the user-visible Company Portal or Software Center error.
5. Do not interpret or change enterprise application-control policy unless assigned.

## Resolution or next action

Install from the approved self-service catalog when available. Otherwise attach the approval, signature status, error, device record, and business requirement to the privileged deployment or endpoint-management queue.

## Validation

- The installed version matches the approved request.
- The application launches for the user.
- Security controls remain enabled.
- No administrator credential was shared or stored.

## Ticket note example

> Simulated ticket note: Verified the application and version were approved, confirmed the installer signature was valid, reproduced the Company Portal failure, and escalated the device ID, deployment error, and approval record to Endpoint Management. No security control was bypassed.

## Escalation criteria

Escalate unsigned or unexpected installers, application-control blocks, requests outside the catalog, privileged deployment needs, repeated managed-app failures, or any request to weaken endpoint security.

## References

- [Get-AuthenticodeSignature — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-authenticodesignature)
- [Install work apps from Company Portal — Microsoft Learn](https://learn.microsoft.com/en-us/intune/user-help/apps/install-apps-windows)
