---
title: "Clear a stuck Windows print queue"
author: "Tier 1 Support Lab"
category: "Printing"
article_type: "How-To"
last_updated: "2026-08-26"
evidence_status: "concept_reviewed"
kb_id: "KB-PRINT-002"
tags: ["Windows 11", "Printing", "Print Spooler", "Queue"]
platforms: ["Windows 11"]
support_tier: "Tier 1 with local admin approval"
risk: "Moderate"
---

## Summary

Clear a print job that remains in the Windows queue after normal cancellation fails.

## Scope and safety

Clearing the spooler directory permanently removes every queued job on that workstation. Confirm the affected printer, notify the user, and obtain the required administrative approval before stopping the service or deleting spool files.

## Symptoms or trigger

- A job remains in **Deleting** or **Error**.
- New jobs remain behind the stuck job.
- The printer is ready, but the workstation queue does not advance.

## Information to collect

- Computer and printer name
- Local, TCP/IP, or print-server connection
- Print-job ID, owner, and document name
- Whether other users or queues are affected
- Exact queue and printer-panel status

## Diagnostic steps

List jobs without removing them:

```powershell
Get-PrintJob -PrinterName "Printer name"
```

Attempt to remove only the affected job:

```powershell
Remove-PrintJob -PrinterName "Printer name" -ID 1 -Confirm
```

If the job remains, confirm no other local queue requires its pending jobs, then stop the spooler and inspect the files:

```powershell
Stop-Service -Name Spooler -Force -Confirm
Get-ChildItem -LiteralPath "$env:SystemRoot\System32\spool\PRINTERS" -File
```

## Resolution or next action

Preview the spool-file removal first:

```powershell
Get-ChildItem -LiteralPath "$env:SystemRoot\System32\spool\PRINTERS" -File |
    Remove-Item -Force -WhatIf
```

After confirming the exact target and approval, rerun without `-WhatIf`, then restart the service:

```powershell
Start-Service -Name Spooler
```

The user must resubmit removed jobs.

## Validation

```powershell
Get-Service -Name Spooler
Get-PrintJob -PrinterName "Printer name"
```

Confirm the service is running, the queue is clear, and one approved test page prints successfully.

## Ticket note example

> Simulated ticket note: Confirmed one Windows workstation was affected, recorded the stuck job, obtained approval to clear its local queue, restarted the Print Spooler, and verified successful test-page printing. The user was advised that removed jobs required resubmission.

## Escalation criteria

Escalate multiple affected users, repeated spooler stops, print-server unavailability, driver failures, hardware errors, or a queue that remains stuck after the approved local procedure.

## References

- [Remove-PrintJob — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/printmanagement/remove-printjob)
- [Printer not responding and Print Spooler guidance — Microsoft Learn](https://learn.microsoft.com/en-us/troubleshoot/windows-server/printing/printer-not-responding)
