---
title: "Start Here: First-Contact IT Support Triage"
author: "Tier 1 Support Lab"
category: "Start Here"
article_type: "Checklist"
content_type: "Checklist"
last_updated: "2026-08-30"
reviewed_on: "2026-08-30"
evidence_status: "concept_reviewed"
audience: "Technician"
difficulty: "Foundational"
prerequisites: ["Authorized support request", "Approved ticketing process"]
kb_id: "KB-START-001"
tags: ["First Contact", "Triage", "Ticket Notes", "Escalation"]
platforms: ["Windows 11", "Microsoft 365"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

Use this five-minute path to turn a vague report into a scoped, reproducible support case before changing the device or account.

## Scope and safety

Verify the requester through the approved process. Never ask for a password, MFA code, recovery key, or secret. Do not run elevated commands or change accounts, policies, security controls, or user data merely to “try something.”

## Checklist

1. Record the user’s words, affected task, exact error, time, device, location, and business impact.
2. Establish scope: one user, one device, one application, one site, or multiple users.
3. Ask what changed and when it last worked. Confirm whether the problem is repeatable.
4. Check service health or a known-good comparison before changing the endpoint.
5. Observe the current state and select one low-risk test that distinguishes two plausible causes.
6. Make one approved, reversible correction only when evidence supports it.
7. Repeat the original task, confirm with the user, and record the result.

## Completion evidence

A complete first-contact record contains the symptom, scope, timestamps, environment, evidence, action, validation, user communication, and next owner. “Restarted and fixed” is incomplete without the original condition and verified outcome.

## Exceptions and escalation

Stop and escalate suspected compromise, malicious MFA prompts, data loss, BitLocker recovery without verified ownership, multiple-user outage, repeated hardware failure, privileged changes, or any case outside the technician’s authorization.

## Ticket note example

> Simulated ticket note: User reported Outlook could not send at 10:12 ET on LAB-W11-04. Web mail worked and Microsoft service health showed no incident, isolating the issue to the desktop client. Reopened Outlook after an approved restart and verified a test message sent and arrived. User confirmed service restored.

## References

- [Computer user support specialist tasks — O*NET](https://www.onetonline.org/link/details/15-1232.00)
- [Microsoft 365 troubleshooting for IT professionals](https://learn.microsoft.com/en-us/troubleshoot/microsoft-365/)
