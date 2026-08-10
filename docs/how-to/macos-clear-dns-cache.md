---
title: Clear macOS DNS Cache
kb_id: HOW-260809234827
author: Tier 1 Support
category: How-To Guides
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: Low
tags:
- macOS
- DNS
- Networking
---

## Summary
How to flush the local mDNSResponder DNS cache on modern macOS versions to resolve stale hostname resolution issues.

## Prerequisites for Tier 1 Technicians
- Terminal access on the affected Mac.
- `sudo` privileges.

## Diagnostic Steps

1. **Flush the DNS Cache:**
   On macOS High Sierra (10.13) and later (including Sonoma), the DNS cache is managed by `mDNSResponder`. Flush it using `dscacheutil` and restarting the responder.
   ```bash
   sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
   ```

2. **Verify the Flush:**
   Test resolution against the problematic internal resource to ensure it returns the new IP address.
   ```bash
   ping -c 4 internal-server.corp.local
   nslookup internal-server.corp.local
   ```

3. **Check Network Interface DNS Servers:**
   If flushing doesn't fix it, verify what DNS servers the Mac is actually using.
   ```bash
   networksetup -getdnsservers Wi-Fi
   ```
   If it returns `There aren't any DNS Servers set on Wi-Fi`, it is relying on DHCP provided DNS. Check the router or VPN configuration.
