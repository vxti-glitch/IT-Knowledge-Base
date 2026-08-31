---
title: "Browser Sign-In, Cache, Extension, or Certificate Problem"
author: "Tier 1 Support Lab"
category: "Windows Endpoint"
article_type: "Troubleshooting"
content_type: "Troubleshooting"
last_updated: "2026-08-30"
reviewed_on: "2026-08-30"
evidence_status: "concept_reviewed"
audience: "Technician"
difficulty: "Intermediate"
prerequisites: ["Approved browser", "User consent before clearing site data"]
kb_id: "KB-WINDOWS-006"
tags: ["Browser", "Certificate", "Extensions", "Sign-In"]
platforms: ["Windows 11", "Microsoft Edge"]
support_tier: "Tier 1"
risk: "Moderate"
---

## Summary

Use a controlled comparison to distinguish site/service, network, identity, browser profile, extension, site data, date/time, and certificate trust failures.

## Scope and safety

Never bypass certificate warnings, install an unapproved certificate/extension, or clear all browser data without user impact review. Use official URLs and protect saved sessions/passwords.

## Symptoms or trigger

Sign-in loop, one site fails, blank page, extension interference, stale content, certificate warning, or web works in one browser/profile but not another.

## Information to collect

Exact URL/error, timestamp, browser/version/profile, one site or many, private-window result, another browser/device/network result, extensions, proxy/VPN, system time, and certificate issuer/validity details without private keys.

## Diagnostic steps

Verify official URL, service health, date/time, DNS and required port. Test a private window to isolate session/extension/profile effects, then a separate approved browser. Disable only a user-controlled extension for one test if permitted. Clear data only for the affected site after consent. Treat certificate name, expiry, chain, or interception errors as security/network evidence—not something to click through.

## Resolution or next action

Remove the isolated unapproved extension, clear affected-site data, correct date/time through approved settings, update the approved browser, or escalate certificate/proxy/identity evidence.

## Validation

Original URL and task work in the normal profile after restart without certificate bypass or lost required data.

## Ticket note example

> Simulated ticket note: Portal worked in an InPrivate window but looped in normal profile. With user consent, cleared data for only `portal.example.test`; normal sign-in then succeeded. Saved passwords and unrelated sites were untouched.

## Escalation criteria

Escalate certificate warnings, managed extensions/policies, suspicious redirect, multi-user impact, Conditional Access, or repeated profile corruption.

## References

- [Microsoft Edge support](https://support.microsoft.com/en-us/microsoft-edge)
