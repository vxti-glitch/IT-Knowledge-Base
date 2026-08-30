---
title: "Connected to Wi-Fi but No Internet: First Response"
author: "Tier 1 Support Lab"
category: "Networking & VPN"
article_type: "Troubleshooting"
content_type: "Troubleshooting"
last_updated: "2026-08-30"
reviewed_on: "2026-08-30"
review_state: "Validated"
audience: "Technician"
difficulty: "Foundational"
prerequisites: ["Authorized network", "Read-only evidence collection"]
kb_id: "KB-NETWORK-004"
tags: ["Wi-Fi", "DNS", "DHCP", "Gateway"]
platforms: ["Windows 11"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

“Connected” confirms association, not DHCP, gateway, DNS, captive-portal, proxy/VPN, or application success. Isolate the failing boundary.

## Scope and safety

Do not forget/recreate managed profiles, change DNS/proxy/firewall settings, or reset the network before preserving evidence. Do not test private targets from an untrusted network.

## Symptoms or trigger

Wi-Fi icon shows connected but websites/services fail, a captive portal loops, or only VPN/internal resources fail.

## Information to collect

One device or many, SSID classification (redacted in published evidence), location, IP/prefix/gateway/DNS, captive portal, VPN/proxy, IP-vs-hostname behavior, affected services, and recent change.

## Diagnostic steps

Use `Get-NetIPConfiguration` or `ipconfig /all` to record adapter, address, gateway, DHCP, and DNS. A `169.254/16` address indicates IPv4 link-local operation and normally cannot reach routed resources. Test the default gateway when appropriate, an approved external IP, then an explicit DNS query and required application TCP port. Compare another device and official service health.

## Resolution or next action

Complete the authorized captive portal, reconnect the approved SSID, renew DHCP only under procedure, or pause a conflicting user-controlled VPN when permitted. Route deep layer isolation to the Network Triage Lab.

## Validation

Device has expected addressing, resolves an approved name, reaches the required port/application, and repeats the user’s original task.

## Ticket note example

> Simulated ticket note: Wi-Fi associated but device had a 169.254 address and no gateway. Another device worked. Approved reconnect obtained a valid lab lease; DNS and original service then succeeded.

## Escalation criteria

Escalate multi-user/site impact, persistent DHCP failure, managed proxy/VPN/profile issue, suspected rogue network, or infrastructure changes.

## References

- [ipconfig — Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig)
- [IPv4 link-local — RFC 3927](https://www.rfc-editor.org/rfc/rfc3927.html)
