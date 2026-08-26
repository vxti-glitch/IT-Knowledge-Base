---
title: "Handle a BitLocker recovery-key prompt"
author: "Tier 1 Support Lab"
category: "Windows Endpoint"
article_type: "Runbook"
last_updated: "2026-08-26"
kb_id: "KB-WINDOWS-001"
tags: ["Windows 11", "BitLocker", "Recovery Key", "Encryption"]
platforms: ["Windows 11", "Microsoft Entra ID"]
support_tier: "Tier 1 with delegated access"
risk: "High"
---

## Summary

Verify the user and device, retrieve only an authorized BitLocker recovery key, and record the reason a protected device entered recovery.

## Scope and safety

A recovery key protects encrypted data and must be handled as a secret. Do not place the key in a ticket, chat transcript, screenshot, or knowledge-base article. Never attempt to bypass encryption or provide a key for an unverified person or device.

## Symptoms or trigger

- Windows displays the BitLocker recovery screen during startup.
- The screen shows a recovery-key ID.
- The prompt followed a firmware, TPM, boot-order, or hardware change.

## Information to collect

- Verified user identity
- Device asset tag, serial number, and assigned owner
- Recovery-key ID displayed on screen, not the key itself
- Changes immediately before the prompt
- Whether the device is organization-owned and present in the approved management system

## Diagnostic steps

1. Match the asset record to the verified user and physical device.
2. Compare the displayed recovery-key ID with the authorized directory or device-management record.
3. Confirm the reason for recovery when the management portal provides one.
4. Stop if ownership, key ID, or device record does not match.

## Resolution or next action

Disclose the matched recovery key only through the approved secure process. Have the user enter it directly at the device. After Windows starts, document the trigger and route repeated recovery events for TPM, firmware, policy, or hardware review.

## Validation

After startup, an authorized technician can check protection state without exposing key material:

```powershell
manage-bde -status C:
```

Confirm the device boots normally and remains encrypted according to policy.

## Ticket note example

> Simulated ticket note: Verified the assigned user and asset, matched the displayed recovery-key ID to the managed-device record, delivered the key through the approved secure process, and confirmed Windows started with BitLocker protection enabled. The key itself was not recorded.

## Escalation criteria

Escalate an unmatched device or key ID, repeated recovery prompts, suspected tampering, TPM errors, firmware changes outside process, missing escrowed keys, or any request involving an unverified person.

## References

- [BitLocker recovery overview — Microsoft Learn](https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/recovery-overview)
- [Find your BitLocker recovery key — Microsoft Support](https://support.microsoft.com/en-us/windows/find-your-bitlocker-recovery-key-6b71ad27-0b89-ea08-f143-056f5ab347d6)
