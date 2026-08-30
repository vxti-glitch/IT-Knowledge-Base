---
title: "Troubleshooting by Symptom"
author: "Tier 1 Support Lab"
category: "Start Here"
article_type: "Quick Reference"
content_type: "Quick Reference"
last_updated: "2026-08-30"
reviewed_on: "2026-08-30"
review_state: "Validated"
audience: "Technician and End User"
difficulty: "Foundational"
prerequisites: ["Start with the user's exact words"]
kb_id: "KB-START-002"
tags: ["Symptoms", "Triage", "Decision Guide"]
platforms: ["Windows 11", "Microsoft 365"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

Choose a support path from the observable symptom rather than assuming a cause. Search the library using the bold phrases below for the detailed procedure.

## Scope and safety

Do not use a symptom as proof of root cause. A sign-in prompt may come from identity, licensing, service health, device time, network, or client state. A “network problem” may affect only one application.

## Reference

| User wording | Start with | Compare next |
|---|---|---|
| “I cannot sign in” | Microsoft 365 sign-in decision guide | Web vs desktop, another service, error/correlation ID |
| “Internet is down” | Connected to Wi-Fi but no internet | One device vs several; IP vs hostname |
| “The computer is slow” | CPU, memory, disk, startup triage | One app vs whole device; local vs network task |
| “No sound/camera” | Audio or Teams media guide | Windows vs one app; built-in vs dock/Bluetooth |
| “It won’t print” | Printer offline/queue guide | Local vs network printer; one user vs many |
| “The app crashes” | Application install/update/launch guide | Another profile/device; Event Viewer/error code |
| “Access denied” | File/share access guide | Path availability vs authorization |

## Interpretation

Start with scope, recent change, and a known-good comparison. Pick a test that separates hypotheses. Validation repeats the user’s original task; a command that returns successfully is not automatically proof the user’s problem is resolved.

## Common mistakes

- Clearing caches before recording the error
- Resetting credentials without verifying identity and source of authority
- Treating a service restart as a root cause
- Escalating without timestamps, impact, or attempted tests

## Ticket note example

> Simulated ticket note: Routed the reported “internet outage” through symptom triage. Device had a valid gateway and could reach an IP, but hostname resolution failed, so the case moved to DNS evidence collection.

## Escalation criteria

Escalate security indicators, multi-user impact, privileged actions, repeated failure, data loss, hardware safety concerns, or an issue outside the documented Tier 1 boundary.

## References

- [Microsoft troubleshooting documentation](https://learn.microsoft.com/en-us/troubleshoot/)
