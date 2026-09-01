---
title: "Respond to an unfamiliar MFA prompt"
author: "Tier 1 Support Lab"
category: "Identity & Access"
article_type: "Runbook"
last_updated: "2026-08-26"
evidence_status: "concept_reviewed"
kb_id: "KB-IDENTITY-003"
tags: ["MFA", "Microsoft Entra ID", "Account Security", "Escalation"]
platforms: ["Microsoft 365", "Microsoft Entra ID"]
support_tier: "Tier 1 intake"
risk: "High"
---

## Summary

Protect the user, preserve a useful timeline, and hand an unexpected MFA request to the authorized security or identity team without claiming a forensic conclusion.

## Scope and safety

Tell the user not to approve the prompt. Do not ask for MFA codes, passwords, or screenshots containing secrets. Tier 1 records user-visible facts and follows approved containment steps; sign-in-log investigation and compromise determination belong to the authorized resolver group.

## Symptoms or trigger

- An authenticator prompt appears when the user is not signing in.
- The user receives repeated approval requests or an unexpected number match.
- A text or voice code arrives without a user-initiated sign-in.

## Information to collect

- Verified username and contact method
- Time and time zone of each prompt
- Device receiving the prompt
- Whether any prompt was approved or any code was shared
- Recent password changes or sign-ins initiated by the user

## Diagnostic steps

1. Confirm the user is not currently attempting a sign-in.
2. Ask whether any prompt was approved.
3. Capture the visible application name and approximate location only if shown.
4. Check the support queue for a broader known incident without exposing other users' information.
5. Do not interpret sign-in telemetry unless that duty is assigned.

## Resolution or next action

1. Instruct the user to deny the request and use the application's fraud-reporting option when available.
2. Follow the approved password-reset or account-securement process.
3. Escalate immediately to the designated security or identity resolver group with the collected timeline.
4. Keep the user on an approved contact channel until the handoff is acknowledged when policy requires it.

## Validation

- Confirm the suspicious prompt was denied rather than approved.
- Confirm the escalation contains the user, time zone, device, prompt count, and approval status.
- Record the receiving resolver group and handoff time.

## Ticket note example

> Simulated ticket note: Verified the caller and documented three unexpected authenticator prompts between 14:05 and 14:12 ET. User denied all prompts and reported sharing no code. Escalated the timeline and device context to the fictional Security Operations queue; no compromise determination was made by Tier 1.

## Escalation criteria

Always escalate when a prompt was approved, a code was shared, privileged access is involved, multiple users report the behavior, or policy requires security review of any unexpected MFA request.

## References

- [Microsoft Authenticator authentication method — Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-authenticator-app)
- [Revoke user access in an emergency — Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access)
