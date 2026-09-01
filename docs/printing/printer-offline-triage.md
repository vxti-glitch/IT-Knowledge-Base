---
title: "Triage a Windows printer that shows Offline"
author: "Tier 1 Support Lab"
category: "Printing"
article_type: "FAQ"
last_updated: "2026-08-26"
evidence_status: "concept_reviewed"
kb_id: "KB-PRINT-001"
tags: ["Windows 11", "Printing", "Printer Offline", "TCP/IP"]
platforms: ["Windows 11", "Network Printer"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

Determine whether an offline printer problem is physical, queue-specific, workstation-specific, network-related, or a wider print-service incident.

## Scope and safety

Do not change a printer's IP address, port, driver, firmware, or print-server configuration without approval. Avoid deleting a shared queue when other users may depend on it.

## Symptoms or trigger

- Windows displays the printer as **Offline**.
- Jobs remain queued on one workstation.
- The printer panel is ready, but a network queue is unavailable.

## Information to collect

- Printer display name, asset tag, and location
- USB, direct TCP/IP, or print-server connection
- One user or multiple users affected
- Printer-panel status and visible error
- Queue name, port, and driver shown on the workstation

## Diagnostic steps

1. Check power, paper, toner, cable, and printer-panel errors.
2. Confirm whether another user can print to the same queue.
3. Inspect the local queue for **Pause Printing** or **Use Printer Offline**.
4. Record the Windows printer and port state:

```powershell
Get-Printer | Select-Object Name, PrinterStatus, DriverName, PortName
```

5. For an approved network-printer address, test reachability without changing configuration:

```powershell
Test-NetConnection "printer.example.test" -Port 9100
```

## Resolution or next action

Resume the queue or clear **Use Printer Offline** when it was selected accidentally. Correct a physical printer error the user can safely address. Restart the local queue only after confirming the impact. For a shared print-server or network failure, preserve the queue and port details for escalation.

## Validation

- Printer status returns to ready or normal.
- One approved test page leaves the queue.
- The printer produces the page.
- Other users' queues remain unaffected.

## Ticket note example

> Simulated ticket note: Confirmed the printer panel was ready and other users could print. Found **Use Printer Offline** selected on one Windows workstation, cleared the setting, and verified a successful test page from the affected queue.

## Escalation criteria

Escalate multiple affected users, failed network-port tests, print-server outages, repeated spooler failures, hardware codes, driver replacement needs, or any required printer/port configuration change.

## References

- [Fix printer connection and printing problems — Microsoft Support](https://support.microsoft.com/en-us/windows/fix-printer-connection-and-printing-problems-in-windows-fb830bff-7702-6349-33cd-9443fe987f73)
- [Get-Printer — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/printmanagement/get-printer)
