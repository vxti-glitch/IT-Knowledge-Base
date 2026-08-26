---
title: "Triage a slow Windows 11 workstation"
author: "Tier 1 Support Lab"
category: "Windows Endpoint"
article_type: "FAQ"
last_updated: "2026-08-26"
kb_id: "KB-WINDOWS-002"
tags: ["Windows 11", "Performance", "Task Manager", "Disk Space"]
platforms: ["Windows 11"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

Collect evidence that distinguishes a single slow application from device-wide CPU, memory, storage, update, or network pressure.

## Scope and safety

Do not terminate unfamiliar business, security, backup, or management processes. Avoid broad cleanup utilities, registry changes, and operating-system repair commands until evidence supports them and the action is approved.

## Symptoms or trigger

- Sign-in or application launch takes longer than normal.
- Task Manager shows sustained high CPU, memory, or disk use.
- Only one application or website is slow.

## Information to collect

- Start time, frequency, and exact slow activity
- One application or the whole device affected
- Device model, uptime, and Windows version
- Available storage and recent updates
- Whether the device is on AC power, VPN, or a constrained network

## Diagnostic steps

Capture basic state without changing it:

```powershell
Get-CimInstance Win32_OperatingSystem |
    Select-Object Caption, Version, LastBootUpTime, FreePhysicalMemory

Get-Volume | Where-Object DriveLetter |
    Select-Object DriveLetter, FileSystemLabel, SizeRemaining, Size

Get-Process | Sort-Object CPU -Descending |
    Select-Object -First 10 Name, CPU, WorkingSet
```

Use Task Manager to observe sustained usage rather than a single spike. Check Windows Update status and test the affected application separately from network-dependent services.

## Resolution or next action

Close only user-owned applications confirmed unnecessary, restart when uptime or a pending update justifies it, free storage through approved Windows storage controls, and update the specifically affected approved application. Make one change at a time and retest.

## Validation

- Repeat the user's original task and compare response time.
- Confirm resource use returns to a reasonable baseline.
- Confirm required security and management processes remain running.
- Record which single change produced improvement.

## Ticket note example

> Simulated ticket note: Reproduced device-wide slowness, recorded 18 days of uptime and a pending Windows restart, observed no sustained resource spike, completed the approved restart, and verified normal application launch and browser response with the user.

## Escalation criteria

Escalate disk-health warnings, repeated crashes, suspected malware, sustained unexplained resource use, insufficient managed storage, failed updates, overheating, or performance that remains poor after evidence-based Tier 1 actions.

## References

- [Tips to improve PC performance in Windows — Microsoft Support](https://support.microsoft.com/en-us/windows/tips-to-improve-pc-performance-in-windows-b3b3ef5b-5953-fb6a-2528-4bbed82fba96)
- [Get-Process — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-process)
