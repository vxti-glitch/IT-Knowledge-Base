---
title: "Windows Will Not Start: Recovery Triage"
author: "Tier 1 Support Lab"
category: "Windows Endpoint"
article_type: "Troubleshooting"
content_type: "Troubleshooting"
last_updated: "2026-08-30"
reviewed_on: "2026-08-30"
evidence_status: "concept_reviewed"
audience: "Technician"
difficulty: "Advanced"
prerequisites: ["Physical or approved remote access", "Recovery authorization"]
kb_id: "KB-WINDOWS-005"
tags: ["Windows 11", "WinRE", "Startup Repair", "BitLocker"]
platforms: ["Windows 11"]
support_tier: "Tier 1 / Endpoint escalation"
risk: "High"
---

## Summary

Separate no power, no display, firmware/boot failure, Windows startup failure, and sign-in failure before using recovery tools.

## Scope and safety

Protect user data. Do not reinstall, reset, repartition, change firmware security, or bypass encryption. Verify asset and requester identity. Windows Recovery Environment may require the authorized BitLocker recovery key.

## Symptoms or trigger

No power indicators, blank display, firmware error, boot loop, automatic repair, blue screen, or Windows reaches sign-in but rejects access.

## Information to collect

Power/display behavior, exact screen/error/stop code, recent update/driver/hardware event, external devices, encryption state, backup status, recurrence, and whether the firmware detects the storage device.

## Diagnostic steps

Check power and display with known-good approved components. Disconnect only nonessential peripherals. Record the first failing stage. If Windows enters WinRE, use Troubleshoot > Advanced options > Startup Repair when approved; record the result. Do not assume Startup Repair can fix storage failure, malware, or every boot configuration issue.

## Resolution or next action

Use the lowest-risk action supported by evidence: correct power/display input, remove a faulty peripheral, run approved Startup Repair, or hand off with boot-stage and recovery evidence. Preserve data and encryption state.

## Validation

Windows reaches sign-in, the authorized user signs in, required data/applications are present, encryption remains active, and a controlled restart succeeds.

## Ticket note example

> Simulated ticket note: Device powered on and firmware detected storage, but Windows entered automatic repair after an update. With recovery authorization and verified key ownership, Startup Repair completed. Device booted twice and user confirmed files and applications present.

## Escalation criteria

Escalate missing storage, hardware noise/damage, unavailable recovery key, data-loss risk, repeated repair loop, suspected malware, firmware/TPM issue, or any reinstall/reset decision.

## References

- [Startup Repair — Microsoft Support](https://support.microsoft.com/en-us/windows/experience/startup-boot/startup-repair)
