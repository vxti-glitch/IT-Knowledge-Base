---
title: "Check Service Health Before Changing the Endpoint"
author: "Tier 1 Support Lab"
category: "Support Operations"
article_type: "How-To"
content_type: "How-To"
last_updated: "2026-08-30"
reviewed_on: "2026-08-30"
evidence_status: "concept_reviewed"
audience: "Technician"
difficulty: "Foundational"
prerequisites: ["Approved public status page or authorized admin portal"]
kb_id: "KB-OPS-004"
tags: ["Service Health", "Scope", "Microsoft 365"]
platforms: ["Microsoft 365", "SaaS"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

Determine whether a reported failure is broader than one endpoint before clearing caches, rebuilding profiles, or changing credentials.

## Scope and safety

Use official public status pages or an authorized service-health portal. Do not publish tenant incident details or infer “no outage” solely because a public page is green.

## Prerequisites

Record the affected service/feature, first observed time and time zone, geography/site, user count, client path, and a known-good comparison.

## Procedure

Check the official service-health source and active advisories. Compare another user, device, network, web client, or separate feature without exposing data. Align incident start time, region, feature, and error with the report. If no advisory matches, continue endpoint/identity/network triage; absence of a posted incident is not proof the service is healthy.

## Expected result

The ticket states whether an official incident matches, whether the failure is widespread or isolated, and what evidence supports the next owner. Avoid endpoint changes when the vendor is already investigating a matching issue.

## Recovery or rollback

No state is changed. If a temporary workaround is approved, document limitations and remove it after official recovery validation.

## Ticket note example

> Simulated ticket note: Three users reported Teams presence delay beginning 13:05 ET. Authorized service health showed a matching regional advisory. No endpoints changed; users received status/workaround guidance and the case was linked for monitoring.

## Escalation criteria

Escalate widespread impact without a matching advisory, business-critical outage, security concern, or vendor incident requiring organizational coordination.

## References

- [Microsoft 365 troubleshooting for IT professionals](https://learn.microsoft.com/en-us/troubleshoot/microsoft-365/)
