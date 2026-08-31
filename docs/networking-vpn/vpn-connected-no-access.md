---
title: "Triage a VPN that connects but cannot reach company resources"
author: "Tier 1 Support Lab"
category: "Networking & VPN"
article_type: "FAQ"
last_updated: "2026-08-26"
evidence_status: "concept_reviewed"
kb_id: "KB-NETWORK-001"
tags: ["VPN", "DNS", "Routing", "Remote Work"]
platforms: ["Windows 11", "VPN Client"]
support_tier: "Tier 1"
risk: "Moderate"
---

## Summary

Determine whether a connected VPN failure is caused by local internet access, name resolution, routing, authentication, or a specific unavailable company service.

## Scope and safety

Use only approved hostnames and test addresses. Do not add persistent routes, change DNS servers, disable endpoint security, or alter split-tunnel policy. Capture existing state before reconnecting the client.

## Symptoms or trigger

- The VPN client reports connected, but an internal site does not open.
- Internal resources fail by name but work by approved IP address.
- Only one application or network share is unavailable.

## Information to collect

- VPN client, profile, and visible status
- User location and local network type
- Exact resource and error
- Whether internet access works before and after connection
- Whether coworkers using the same service are affected

## Diagnostic steps

Capture adapter, DNS, and route state:

```powershell
Get-NetIPConfiguration
Get-DnsClientServerAddress
Get-NetRoute -AddressFamily IPv4 |
    Sort-Object RouteMetric |
    Select-Object -First 20 DestinationPrefix, NextHop, InterfaceAlias, RouteMetric
```

Test one approved internal hostname and port:

```powershell
Resolve-DnsName "intranet.example.test"
Test-NetConnection "intranet.example.test" -Port 443
```

Compare failure by approved hostname and IP only when the support procedure provides both values.

## Resolution or next action

Correct local connectivity first. Reconnect the approved VPN profile once, refresh name resolution when DNS alone is stale, and relaunch the affected application. If the expected route, DNS suffix, or policy is absent, preserve the evidence and escalate rather than creating a manual workaround.

## Validation

- VPN status remains connected.
- The approved internal hostname resolves correctly.
- The required port test succeeds.
- The user opens the original company resource.

## Ticket note example

> Simulated ticket note: Confirmed local internet access and VPN connection, reproduced failure to one internal hostname, recorded the assigned DNS servers and route table, and found the expected VPN DNS suffix missing. Escalated captured adapter and client details to Network Support without adding a manual route.

## Escalation criteria

Escalate missing routes or DNS suffixes, multiple affected users, certificate or posture failures, gateway errors, required policy changes, or an unavailable internal service that is reachable from neither client nor approved monitoring path.

## References

- [Test-NetConnection — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection)
- [Get-NetIPConfiguration — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-netipconfiguration)
