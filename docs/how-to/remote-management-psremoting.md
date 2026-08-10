---
author: Tier 1 Support
category: How-To Guides
date_added: '2026-05-15'
kb_id: HOW-007
last_updated: '2026-06-15'
short_title: How to Remotely Manage Windows Endpoints via PowerShell PSRemoting
tags:
- PowerShell
- Windows
- Endpoint
- Automation
- Networking
title: Remotely manage windows endpoints via powershell psremoting
---


## Summary
A General Issue issue reporting a "Failed" or "Unresponsive" status does not guarantee that the hardware is at fault. The OS may be functional at the kernel layer while driver conflicts, WMI corruption, or endpoint security software prevent successful execution. This article covers the most common causes and their resolution paths for Windows 11 enterprise environments.

## Prerequisites for Tier 1 Technicians
Before proceeding, confirm the following from the user:
- Exact hardware model and Windows 11 build number (e.g., 22H2, 23H2)
- Whether they are experiencing a hard lock, BSOD, or application-specific hang
- Which specific driver or service is failing
- Whether the issue started after a specific event (Patch Tuesday, driver update, new peripheral)

## Diagnostic Steps

Step 1 — Verify Service and Driver State
Instruct the user to open an elevated PowerShell prompt and run:
`Get-Service -Name *general* | Select-Object Status, Name, StartType`
If the service is stopped, attempt to start it. If it immediately crashes, check the Application Event Log for Faulting Module Name.

Step 2 — Check Endpoint Security Blocks
Run the following to check for Antivirus/Defender interference:
`Get-MpPreference | Select-Object ExclusionPath, ExclusionProcess`
After reviewing the output, ensure that:
- Required paths for the application are excluded
- Attack Surface Reduction (ASR) rules aren't generating block events in Event Viewer (Event ID 1121).

## When to Escalate to Tier 2 (Endpoint Management)
Escalate if any of the following are true:
- `sfc /scannow` and `DISM /Online /Cleanup-Image /RestoreHealth` fail to repair corrupted OS components
- Endpoint security is correctly configured but WMI queries continuously time out
- Multiple users on the same hardware model are reporting the same General Issue issue simultaneously