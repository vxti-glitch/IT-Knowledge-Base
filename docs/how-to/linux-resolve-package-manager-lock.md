---
title: Resolve Package Manager Lock (dpkg/apt)
kb_id: HOW-260809234827
author: Tier 1 Support
category: How-To Guides
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: Medium
tags:
- Linux
- apt
- dpkg
---

## Summary
How to safely remove a stale lock file when `apt` or `dpkg` complains that it is locked by another process (e.g., `Could not get lock /var/lib/dpkg/lock`).

## Prerequisites for Tier 1 Technicians
- SSH access with `sudo` privileges.
- Debian/Ubuntu-based distribution.

## Diagnostic Steps

1. **Identify the Locking Process:**
   Before blindly deleting locks, check if an update is actively running in the background (like unattended-upgrades).
   ```bash
   sudo lsof /var/lib/dpkg/lock
   sudo lsof /var/lib/apt/lists/lock
   sudo lsof /var/cache/apt/archives/lock
   ```

2. **Kill the Stale Process:**
   If `lsof` returns a PID (e.g., `1234`) that is stuck or orphaned, kill it gracefully.
   ```bash
   sudo kill -9 <PID>
   ```

3. **Remove the Lock Files:**
   If the processes are dead but the locks remain, remove them manually.
   ```bash
   sudo rm /var/lib/apt/lists/lock
   sudo rm /var/cache/apt/archives/lock
   sudo rm /var/lib/dpkg/lock*
   ```

4. **Reconfigure dpkg:**
   Since the package manager was interrupted, you must reconfigure any half-installed packages.
   ```bash
   sudo dpkg --configure -a
   sudo apt update
   ```
