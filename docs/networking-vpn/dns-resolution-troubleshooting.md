---
title: "Troubleshoot a hostname that does not resolve"
author: "Tier 1 Support Lab"
category: "Networking & VPN"
article_type: "How-To"
last_updated: "2026-08-26"
evidence_status: "concept_reviewed"
kb_id: "KB-NETWORK-003"
tags: ["DNS", "Windows 11", "Name Resolution", "Networking"]
platforms: ["Windows 11", "DNS"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

Prove whether a failure is limited to DNS by comparing approved hostname resolution with general connectivity and a known service port.

## Scope and safety

Use hostnames, IP addresses, and DNS servers supplied by the lab or approved support procedure. Do not change DNS server assignments, edit the hosts file, or expose internal addressing in public tickets.

## Symptoms or trigger

- A site or server fails by hostname.
- General internet or network connectivity still works.
- An approved IP test succeeds while the hostname fails.

## Information to collect

- Exact hostname and error
- Connection type and VPN state
- Expected DNS suffix or zone
- Whether other users resolve the same name
- When the record last worked or changed

## Diagnostic steps

```powershell
Get-DnsClientServerAddress
Resolve-DnsName "host.example.test"
Test-NetConnection "host.example.test" -Port 443
```

If the hostname lookup fails but an approved gateway or external connectivity test succeeds, record the resolver and error. Compare short-name and fully qualified domain name only when both are expected. Check the DNS client cache:

```powershell
Get-DnsClientCache | Where-Object Entry -Like "*example.test*"
```

## Resolution or next action

For a stale client cache, clear it and retry:

```powershell
Clear-DnsClientCache
Resolve-DnsName "host.example.test"
```

If the expected DNS server, suffix, or record is missing, preserve the output and escalate rather than assigning a public resolver or adding a hosts-file entry.

## Validation

- The approved hostname returns the expected record type.
- The required service port succeeds.
- The original application opens by hostname.
- No unauthorized resolver or local override was added.

## Ticket note example

> Simulated ticket note: Confirmed gateway and approved IP connectivity, reproduced failure only for the internal hostname, recorded the client DNS servers, cleared one stale client-cache entry, and verified name resolution plus HTTPS access after retest.

## Escalation criteria

Escalate missing or incorrect authoritative records, widespread failure, DNS server timeouts, VPN DNS-policy problems, DNSSEC errors, or any required server-side record change.

## References

- [Resolve-DnsName — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/dnsclient/resolve-dnsname)
- [Clear-DnsClientCache — Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/dnsclient/clear-dnsclientcache)
