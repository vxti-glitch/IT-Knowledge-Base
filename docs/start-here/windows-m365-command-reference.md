---
title: "Windows and Microsoft 365 Command Quick Reference"
author: "Tier 1 Support Lab"
category: "Start Here"
article_type: "Quick Reference"
content_type: "Quick Reference"
last_updated: "2026-08-30"
reviewed_on: "2026-08-30"
evidence_status: "concept_reviewed"
audience: "Technician"
difficulty: "Intermediate"
prerequisites: ["Use read-only commands first", "Redact exported evidence"]
kb_id: "KB-START-003"
tags: ["PowerShell", "Commands", "Evidence", "Windows 11"]
platforms: ["Windows 11", "PowerShell"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

Use these read-only checks to capture state. Each result is one observation, not an automatic diagnosis.

## Scope and safety

Run in a standard shell unless the command explicitly requires authorized elevation. Redact user names, paths, device names, domains, public addresses, and identifiers before publishing evidence.

## Reference

| Command | Shows | Does not prove |
|---|---|---|
| `Get-ComputerInfo` | Windows/build and device facts | Health or compliance |
| `Get-Volume` | Mounted volumes and free space | Physical disk health |
| `Get-Process` | Current process resource totals | Why usage is high |
| `Get-NetIPConfiguration` | Connected interfaces, IP, gateway, DNS | Internet/application success |
| `Resolve-DnsName name -DnsOnly` | A DNS query through configured behavior | Which server answered unless `-Server` is specified |
| `Test-NetConnection host -Port 443` | TCP connection result to that host/port | Application, TLS, or account health |
| `dsregcmd /status` | Local device registration/join state | Correct Intune assignments |
| `Get-WinEvent` | Matching local event records | Root cause without interpretation |

## Interpretation

Record timestamp, command, target, result, and why the test was selected. Compare expected with observed, then choose the next lowest-risk discriminating test. A failed ping may reflect ICMP filtering while the application port still works.

## Common mistakes

Avoid broad repair scripts, destructive cleanup, copied registry commands, unapproved resets, and publishing raw diagnostic bundles. Never describe TCP port 53 reachability as a DNS query.

## Ticket note example

> Simulated ticket note: Captured read-only IP configuration and an explicit DNS query at 14:08 ET. Device had a valid address/gateway; configured resolver returned no answer for the affected name. No settings were changed.

## Escalation criteria

Escalate when collection requires elevation not granted, output contains security indicators, evidence points to managed policy/service infrastructure, or the correct next test requires another owner.

## References

- [Get-NetIPConfiguration](https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-netipconfiguration)
- [Resolve-DnsName](https://learn.microsoft.com/en-us/powershell/module/dnsclient/resolve-dnsname)
- [Test-NetConnection](https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection)
