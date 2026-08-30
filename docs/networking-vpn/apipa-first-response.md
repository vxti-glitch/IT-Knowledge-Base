---
title: "169.254 Address: DHCP Failure First Response"
author: "Tier 1 Support Lab"
category: "Networking & VPN"
article_type: "Troubleshooting"
content_type: "Troubleshooting"
last_updated: "2026-08-30"
reviewed_on: "2026-08-30"
review_state: "Validated"
audience: "Technician"
difficulty: "Intermediate"
prerequisites: ["Authorized network", "Read-only adapter access"]
kb_id: "KB-NETWORK-005"
tags: ["APIPA", "DHCP", "IPv4", "Gateway"]
platforms: ["Windows 11"]
support_tier: "Tier 1 / Network escalation"
risk: "Low"
---

## Summary

An address in `169.254.0.0/16` is IPv4 link-local. It allows same-link communication in limited cases but normally indicates the endpoint did not obtain its expected DHCP configuration.

## Scope and safety

Do not assign a guessed static address, copy another device’s settings, or repeatedly release/renew without checking scope and link state. Preserve adapter/DHCP evidence first.

## Symptoms or trigger

No routed access, missing default gateway, `169.254.x.x` address, or network status changes after docking, roaming, cable movement, sleep, or lease renewal.

## Information to collect

Adapter/link state, address/prefix/origin, DHCP enabled/server/lease fields, gateway, DNS, wired/Wi-Fi/dock path, other affected devices, VLAN/location, and recent hardware/profile changes.

## Diagnostic steps

Capture `ipconfig /all` or `Get-NetIPConfiguration -All`. Confirm the address is link-local and no expected gateway/lease exists. Verify physical link or Wi-Fi association, isolate dock/cable with an approved known-good comparison, and check whether another device on the same approved network receives a lease. Run one approved `ipconfig /renew` only after evidence collection.

## Resolution or next action

Reconnect the approved network path, replace an isolated cable, or renew once. If the address returns, stop endpoint churn and escalate DHCP/switch/AP/VLAN evidence.

## Validation

Endpoint receives an expected non-link-local address, prefix, gateway, DNS, and lease; then DNS, required port, and original application task succeed.

## Ticket note example

> Simulated ticket note: Ethernet adapter showed DHCP enabled, 169.254.22.41, and no gateway. Known-good cable produced a valid lab lease; original cable failed again. Escalated for cable replacement with before/after evidence.

## Escalation criteria

Escalate multiple affected endpoints, recurring lease loss, switch/AP/VLAN ownership, DHCP server/scope issue, NAC/802.1X symptoms, or managed adapter policy.

## References

- [IPv4 link-local — RFC 3927](https://www.rfc-editor.org/rfc/rfc3927.html)
- [ipconfig — Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig)
