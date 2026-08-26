---
title: "Triage a reported phishing message"
author: "Tier 1 Support Lab"
category: "Security & Escalation"
article_type: "Runbook"
last_updated: "2026-08-26"
kb_id: "KB-SECURITY-001"
tags: ["Phishing", "Email Security", "Incident Intake", "Escalation"]
platforms: ["Microsoft 365", "Outlook"]
support_tier: "Tier 1 intake"
risk: "High"
---

## Summary

Help the user stop interacting with a suspicious message, collect a clear exposure statement, and transfer the report to the authorized security process without performing unapproved analysis.

## Scope and safety

Do not click links, open attachments, forward the message normally, or request passwords. Preserve the original message through the approved reporting mechanism. Tier 1 records user actions and visible facts but does not declare a message safe or malicious without authority.

## Symptoms or trigger

- A message requests urgent credentials, payment, gift cards, or MFA approval.
- The display name and sender address do not match expectations.
- The user clicked, opened, replied, entered credentials, or approved a prompt.

## Information to collect

- Verified reporter and mailbox
- Received time and time zone
- Sender address and subject as displayed
- Whether a link, attachment, reply, credential entry, payment, or MFA approval occurred
- Device used and whether it remains connected

## Diagnostic steps

1. Ask the user to stop interacting with the message.
2. Determine exposure using direct yes/no questions.
3. Use the approved **Report Message** or **Report Phishing** control when available.
4. Capture only the minimum ticket details; preserve the original for security tooling.
5. Do not upload the message to public analysis services.

## Resolution or next action

If there was no interaction, report the message and follow the approved deletion guidance. If the user clicked, entered credentials, opened an attachment, approved MFA, or made a payment, initiate the corresponding urgent security handoff and account/device containment process.

## Validation

- The message was submitted through the approved reporting channel.
- The ticket states exactly what the user did or did not do.
- The appropriate urgency and resolver group were selected.
- The user received a clear safe next step.

## Ticket note example

> Simulated ticket note: User reported a suspicious invoice message received at 09:42 ET. User opened the message but did not click, reply, enter credentials, approve MFA, or open the attachment. Submitted through the fictional Report Phishing control and routed to Security Operations; Tier 1 made no malware determination.

## Escalation criteria

Escalate any user interaction, credential or MFA exposure, payment request, executive impersonation, multiple recipients, sensitive-data disclosure, or message that cannot be preserved through the standard reporting control.

## References

- [Phishing and suspicious behavior in Outlook — Microsoft Support](https://support.microsoft.com/en-us/outlook/mail/phishing-and-suspicious-behavior-in-outlook)
- [User reported message settings — Microsoft Learn](https://learn.microsoft.com/en-us/defender-office-365/submissions-user-reported-messages-custom-mailbox)
