---
title: "Handle a reported lost or stolen managed device"
author: "Tier 1 Support Lab"
category: "Security & Escalation"
article_type: "Runbook"
last_updated: "2026-08-26"
kb_id: "KB-SECURITY-002"
tags: ["Lost Device", "Intune", "Incident Intake", "Data Protection"]
platforms: ["Windows 11", "Microsoft Intune"]
support_tier: "Tier 1 intake"
risk: "High"
---

## Summary

Record the loss quickly, protect the user's account, and hand device actions to the authorized security or endpoint team without sending an unapproved wipe command.

## Scope and safety

Remote lock, retire, and wipe actions can make data unavailable and may have legal or evidence implications. Tier 1 must not trigger them unless the role and procedure explicitly authorize the exact action. Do not expose location information beyond the approved incident team.

## Symptoms or trigger

- A managed laptop or mobile device cannot be located.
- The device was left in transit, a public place, or a stolen vehicle.
- The user believes an unauthorized person may have physical access.

## Information to collect

- Verified user and alternate contact method
- Asset tag, serial number, device type, and ownership
- Last known time, time zone, and general location
- Whether the device was powered on, signed in, encrypted, or unlocked
- Network connectivity and sensitive-data concerns
- Police or facilities report number when policy requires one

## Diagnostic steps

1. Match the device to the asset and management record.
2. Record the last check-in and encryption/compliance status visible to the assigned role.
3. Ask whether credentials, badges, tokens, or removable media were lost with it.
4. Do not attempt personal tracking or contact a suspected possessor.

## Resolution or next action

1. Escalate immediately through the lost-device/security channel.
2. Follow the approved account-protection and session-revocation process.
3. Transfer remote-device action to the authorized Intune or endpoint responder.
4. Start the asset, replacement-device, and facilities workflows as required.
5. Preserve timestamps and command acknowledgements returned by the resolver group.

## Validation

- The incident is acknowledged by the correct resolver group.
- Account-protection actions are recorded.
- Device action and status are documented without exposing location publicly.
- Asset and replacement tasks have owners.

## Ticket note example

> Simulated ticket note: Verified the caller and matched the fictional laptop asset. Recorded last known time, encryption status, and last management check-in, then escalated to Security and Endpoint Management. Tier 1 did not issue a wipe or disclose device location.

## Escalation criteria

Every lost or stolen managed device is escalated. Use the highest urgency defined by policy for an unlocked device, privileged user, sensitive-data exposure, missing encryption, theft, or an active unauthorized sign-in.

## References

- [Remote actions for devices in Microsoft Intune — Microsoft Learn](https://learn.microsoft.com/en-us/intune/intune-service/remote-actions/device-management)
- [Revoke user access in an emergency — Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access)
