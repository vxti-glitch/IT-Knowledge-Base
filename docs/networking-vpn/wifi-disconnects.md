---
title: "Triage repeated Wi-Fi disconnections on Windows 11"
author: "Tier 1 Support Lab"
category: "Networking & VPN"
article_type: "FAQ"
last_updated: "2026-08-26"
kb_id: "KB-NETWORK-002"
tags: ["Wi-Fi", "Windows 11", "Wireless", "Remote Work"]
platforms: ["Windows 11", "Wireless Network"]
support_tier: "Tier 1"
risk: "Low"
---

## Summary

Distinguish a single-device Wi-Fi problem from weak signal, one access point, one saved profile, driver state, or a wider network incident.

## Scope and safety

Do not reveal saved wireless keys, remove managed certificates, change adapter advanced properties, or install unapproved drivers. Avoid deleting the only working remote connection until another support channel is available.

## Symptoms or trigger

- Wi-Fi disconnects and reconnects during the day.
- The device shows weak signal or changes access points frequently.
- Other devices remain connected to the same network.

## Information to collect

- Network name, location, and approximate distance from the access point
- Time and frequency of drops
- One network or every network affected
- Whether other devices disconnect
- Adapter model, driver version, and recent update

## Diagnostic steps

Capture the current wireless state without exposing credentials:

```powershell
netsh wlan show interfaces
Get-NetAdapter -Physical |
    Select-Object Name, InterfaceDescription, Status, LinkSpeed
```

1. Compare behavior near the access point and at the reported location.
2. Test whether another device drops on the same network.
3. Test the affected device on another approved network when possible.
4. Review Windows Update and the approved device-management channel for a driver update.
5. Generate the Windows wireless report when repeated timing evidence is needed:

```powershell
netsh wlan show wlanreport
```

## Resolution or next action

Reconnect to the approved network, restart the adapter or workstation when appropriate, and apply only an approved OEM or managed driver update. Remove and re-add a profile only when credentials or certificates can be restored safely.

## Validation

- Maintain the connection for the agreed observation period.
- Confirm signal and link speed remain stable at the test location.
- Verify the user's original application works without interruption.
- Record whether the issue follows the device or the network.

## Ticket note example

> Simulated ticket note: Reproduced drops only in one workspace, recorded low signal and access-point changes in the wireless report, and confirmed the laptop remained stable on an approved alternate network. Escalated the location and timestamps to Network Support as a coverage issue.

## Escalation criteria

Escalate multiple affected devices, certificate-based authentication failures, suspected access-point coverage or capacity problems, unavailable approved drivers, or repeated disconnects across multiple networks after device-level checks.

## References

- [Fix Wi-Fi connection issues in Windows — Microsoft Support](https://support.microsoft.com/en-us/windows/fix-wi-fi-connection-issues-in-windows-9424a1f7-6a3b-65a6-4d78-7f07eee84d2c)
- [Wireless network report — Microsoft Support](https://support.microsoft.com/en-us/windows/analyzing-the-wireless-network-report-76da0daa-1db2-6049-d154-7bb679eb03ed)
