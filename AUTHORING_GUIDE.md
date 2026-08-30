# Knowledge-Base Authoring Guide

This guide defines the publication standard for the simulated IT Support Knowledge Base Lab.

## Article template

Create the file under the folder matching its `category`:

```markdown
---
title: "Specific user-visible issue or support action"
author: "Tier 1 Support Lab"
category: "Windows Endpoint"
article_type: "FAQ"
content_type: "Troubleshooting"
last_updated: "2026-08-26"
reviewed_on: "2026-08-26"
review_state: "Validated"
audience: "Technician"
difficulty: "Foundational"
prerequisites: ["Authorized support context"]
kb_id: "KB-WINDOWS-004"
tags: ["Windows 11", "Troubleshooting"]
platforms: ["Windows 11"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

State the outcome and affected scope in plain language.

## Scope and safety

Define approval, privilege, data-loss, credential, or security boundaries.

## Symptoms or trigger

- List observable symptoms instead of assumed causes.

## Information to collect

- Capture the exact error, time, device, user impact, and recent change.

## Diagnostic steps

Start with read-only checks and make one hypothesis test at a time.

## Resolution or next action

Describe the lowest-risk approved correction or handoff.

## Validation

Repeat the original task and define observable success.

## Ticket note example

> Simulated ticket note: Record scope, evidence, action, result, and user communication.

## Escalation criteria

Define the Tier 1 boundary and the evidence the next resolver needs.

## References

- [Official vendor documentation](https://example.test/)
```

The example above is the **Troubleshooting** archetype. Other validated archetypes are **How-To**, **Checklist**, **Quick Reference**, **Concept**, and **Security Response**. Use the structure that makes the content easiest to follow; the validator still enforces safety, expected results or validation, ownership boundaries, references, and a reusable handoff when appropriate.

## Supported metadata

| Field | Rule |
|---|---|
| `title` | Specific and user-focused |
| `author` | `Tier 1 Support Lab` for the simulated library |
| `category` | Must match a configured support domain and folder |
| `article_type` | Display label: `FAQ`, `How-To`, `Runbook`, `Troubleshooting`, `Checklist`, `Quick Reference`, `Concept`, or `Security Response` |
| `content_type` | Validated archetype controlling the required section structure |
| `last_updated` | ISO `YYYY-MM-DD` |
| `reviewed_on` | Date the technical sources and procedure were reviewed |
| `review_state` | `Validated`, `Review Needed`, or `Archived` |
| `audience` | `Technician`, `End User`, or `Technician and End User` |
| `difficulty` | `Foundational`, `Intermediate`, or `Advanced` |
| `prerequisites` | Access, authorization, tools, or prior knowledge needed |
| `kb_id` | Unique `KB-DOMAIN-###` value |
| `tags` | At least two normalized terms |
| `platforms` | At least one supported platform |
| `support_tier` | Explicit ownership boundary |
| `risk` | `Low`, `Moderate`, or `High` |

## Writing standard

- Write what a technician should observe, not what a template assumes.
- Use read-only diagnostics before changes.
- State required authorization and possible user impact.
- Never include real names, credentials, recovery keys, tenants, addresses, or employer data.
- Use reserved example domains such as `example.test`.
- Include a concrete validation step.
- Separate Tier 1 facts from security, identity, network, or endpoint conclusions.
- Prefer official vendor references.
- Keep ticket-note examples explicitly simulated.

## Publication check

```powershell
python -m kb check --docs .\docs
python -m unittest discover -s tests -v
python -m kb build --docs .\docs --output .\output
```
