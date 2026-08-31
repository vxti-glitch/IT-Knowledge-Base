---
title: "No Audio, Wrong Output Device, or Microphone Not Working"
author: "Tier 1 Support Lab"
category: "Hardware & Peripherals"
article_type: "Troubleshooting"
content_type: "Troubleshooting"
last_updated: "2026-08-30"
reviewed_on: "2026-08-30"
evidence_status: "concept_reviewed"
audience: "Technician and End User"
difficulty: "Foundational"
prerequisites: ["User consent before test recording"]
kb_id: "KB-HARDWARE-002"
tags: ["Audio", "Microphone", "Privacy", "Teams"]
platforms: ["Windows 11", "Microsoft Teams"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

Separate Windows device selection, per-app selection, mute/level, privacy permission, Bluetooth/dock routing, driver, and physical failure.

## Scope and safety

Obtain consent before recording or test calls. Do not disable privacy/security controls globally. Avoid playing loud test tones and protect conversations from unintended speakers.

## Symptoms or trigger

No sound, wrong speaker, microphone absent, app-only failure, echo, or device changes when a dock/Bluetooth headset connects.

## Information to collect

Affected app, selected input/output, headset/dock/Bluetooth state, mute switches, whether Windows test works, privacy permission, recent update, and known-good device result.

## Diagnostic steps

Open Settings > System > Sound and select/test the intended output and input at a safe level. Check physical mute and volume mixer. Review Settings > Privacy & security > Microphone. Compare Windows Recorder/Camera with the affected app, then check the app’s own device selection. Reconnect one peripheral and review Device Manager only if the fault follows Windows.

## Resolution or next action

Select the correct device, unmute with user consent, allow the approved app, reconnect the isolated peripheral, or apply an approved driver update only when evidence points there.

## Validation

User hears a safe test, microphone level responds, a consented test call/recording succeeds, and the selection survives app restart.

## Ticket note example

> Simulated ticket note: Windows microphone test passed; Teams selected an inactive dock microphone. Selected the approved headset in Teams and verified a test call with user consent.

## Escalation criteria

Escalate hardware damage, driver/code errors, organization privacy policy, repeated dock/Bluetooth instability, or sensitive recording concerns.

## References

- [Fix sound or audio problems in Windows](https://support.microsoft.com/en-us/windows/fix-sound-or-audio-problems-in-windows-73025246-b61c-40fb-671a-2535c7cd56c8)
