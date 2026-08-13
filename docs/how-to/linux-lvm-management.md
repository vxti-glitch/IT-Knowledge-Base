---
title: "Lvm (logical volume manager) in linux"
author: "Tier 1 Support"
category: "How-To Guides"
last_updated: "2026-08-02"
kb_id: "HOW-034"
tags: ["Linux", "Storage", "Admin"]
---

## Summary[¶](#summary "Permanent link")

A Managing LVM (Logical Volume Manager) in Linux issue reporting a “Failed” or “Permission Denied” status does not guarantee that the configuration file is incorrect. The daemon may be established at the application layer while SELinux, AppArmor, or kernel resource limits (OOM) prevent successful execution. This article covers the most common causes and their resolution paths for Enterprise Linux (RHEL/Ubuntu) environments.

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

Before proceeding, confirm the following:  
- Server hostname and OS distribution/version  
- Whether the server is a VM, bare metal, or containerized  
- Which specific service or mount point is failing  
- Whether the issue started after a specific event (kernel upgrade, config push, storage expansion)

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

Step 1 — Test via Systemd and Journalctl  
Log into the server and run:  
`systemctl status managing -l`  
`journalctl -xeu managing`  
If the service fails to start but the syntax is correct, the issue is likely environmental (permissions, ports, memory), not configuration.

Step 2 — Check Mandatory Access Control (MAC)  
Run the following to check SELinux/AppArmor states:  
`sestatus` (RHEL) or `aa-status` (Ubuntu)  
If enforcing, check audit logs:  
`ausearch -m avc -ts recent`  
If you see denied events matching the service, you must generate a local policy module or fix the file context using `restorecon -Rv`.

## When to Escalate to Tier 2 (Linux SysAdmin)[¶](#when-to-escalate-to-tier-2-linux-sysadmin "Permanent link")

Escalate if any of the following are true:  
- `dmesg -T | grep -i oom` confirms the kernel is indiscriminately killing critical management processes  
- MAC policies are correctly configured but the filesystem remains read-only due to underlying SAN/LVM issues  
- Multiple nodes in the cluster are reporting the same Managing LVM (Logical Volume Manager) in Linux issue simultaneously