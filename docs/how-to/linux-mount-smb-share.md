---
title: Mount SMB Share on Linux
kb_id: HOW-260809234827
author: Tier 1 Support
category: How-To Guides
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: Medium
tags:
- Linux
- SMB
- Fileshares
---

## Summary
How to temporarily and permanently mount a Windows SMB/CIFS file share on a Linux workstation or server.

## Prerequisites for Tier 1 Technicians
- `sudo` access.
- `cifs-utils` package installed.
- Valid Active Directory credentials.

## Diagnostic Steps

1. **Install Dependencies:**
   Ensure the CIFS utilities are present.
   ```bash
   sudo apt install cifs-utils  # Debian/Ubuntu
   sudo yum install cifs-utils  # RHEL/CentOS
   ```

2. **Create the Mount Point:**
   Create a local directory where the share will be attached.
   ```bash
   sudo mkdir -p /mnt/finance_share
   ```

3. **Temporary Mount (For Testing):**
   Test the connection and credentials manually.
   ```bash
   sudo mount -t cifs -o username=domain_user,domain=CORP //server.corp.local/Finance /mnt/finance_share
   ```
   Enter the password when prompted. Check access with `ls /mnt/finance_share`.

4. **Permanent Mount (fstab):**
   To mount on boot, create a credentials file `/etc/smbcredentials`:
   ```text
   username=domain_user
   password=secretpassword
   domain=CORP
   ```
   Secure the file: `sudo chmod 600 /etc/smbcredentials`.
   Add to `/etc/fstab`:
   ```text
   //server.corp.local/Finance /mnt/finance_share cifs credentials=/etc/smbcredentials,iocharset=utf8 0 0
   ```
