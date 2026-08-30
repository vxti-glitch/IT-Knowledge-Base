---
title: "Blue Screen, Freeze, or Unexpected Restart: Evidence Collection"
author: "Tier 1 Support Lab"
category: "Windows Endpoint"
article_type: "Troubleshooting"
content_type: "Troubleshooting"
last_updated: "2026-08-30"
reviewed_on: "2026-08-30"
review_state: "Validated"
audience: "Technician"
difficulty: "Advanced"
prerequisites: ["Device is safe to power", "User data risk assessed"]
kb_id: "KB-WINDOWS-007"
tags: ["Blue Screen", "Reliability Monitor", "Event Logs", "Drivers"]
platforms: ["Windows 11"]
support_tier: "Tier 1 / Endpoint escalation"
risk: "High"
---

## Summary

Collect reproducible crash evidence and protect data instead of guessing from a single generic event.

## Scope and safety

Stop for overheating, smell, swelling, liquid, electrical damage, or storage noise. Do not run stress tests, firmware updates, cleaners, or dump analyzers on sensitive data without authorization.

## Symptoms or trigger

Stop code, frozen display/input, spontaneous restart, application hang, or repeated crash during a specific task.

## Information to collect

Exact stop code/parameters, timestamp, task, recurrence, power state, recent driver/update/hardware change, peripherals, temperature/fan symptoms, Reliability Monitor history, Event Viewer records, and dump-file presence/location.

## Diagnostic steps

Distinguish one application from operating-system freeze and unexpected power loss. Review Reliability Monitor around the timestamp and relevant System/Application events. A Kernel-Power event can record an unclean restart but does not by itself identify the cause. Check update/driver history and safely remove one nonessential peripheral only when evidence supports comparison.

## Resolution or next action

Preserve work and back up through approved controls. Apply only an approved correction tied to evidence, such as rollback of a just-installed driver. Otherwise package timestamps, stop code, recent changes, event records, and dump availability for endpoint/hardware escalation.

## Validation

Repeat the original workload safely, monitor recurrence through a controlled period, and confirm data/applications remain available.

## Ticket note example

> Simulated ticket note: Two restarts occurred during docking; recorded stop code and timestamps. Reliability history aligned both failures with the new dock driver. No stress test performed. Escalated with sanitized event details and driver version.

## Escalation criteria

Escalate repeated stop codes, hardware safety symptoms, dump analysis, suspected malware, encryption/storage risk, firmware changes, or any data-loss condition.

## References

- [Troubleshoot blue screen errors](https://support.microsoft.com/en-us/windows/resolving-blue-screen-errors-in-windows-60b01860-58f2-be66-7516-5c45a66ae3c6)
