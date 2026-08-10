---
title: Group Policy Not Applying
kb_id: FAQ-071
author: Tier 1 Support
category: FAQ
date_added: '2026-04-08'
last_updated: '2026-07-14'
severity: Medium
tags:
- Windows
- GPO
- GroupPolicy
- Active Directory
---

## Summary
A user reports that a recently deployed or modified Group Policy Object (GPO) is not applying to their workstation or user account, despite the policy being confirmed active in the Group Policy Management Console (GPMC).

## Prerequisites for Tier 1 Technicians
- Remote access to the affected workstation (RDP or PSRemoting).
- Ability to run `gpresult` and `gpupdate` on the target machine.

## Diagnostic Steps

### Step 1: Force a Group Policy Refresh
Trigger an immediate policy refresh on the target machine. Group Policy normally applies during startup and login (computer) or at 90-minute intervals (user).
```powershell
# Run on the remote workstation
Invoke-Command -ComputerName "WORKSTATION01" -ScriptBlock { gpupdate /force }
```
Or, to do it locally on the machine:
```cmd
gpupdate /force
```
Wait for `Computer Policy update has completed successfully` and `User Policy update has completed successfully`.

### Step 2: Generate the GP Resultant Set of Policy (RSoP)
This command outputs a detailed HTML report of every policy applied (and any that failed to apply) for the current user and computer:
```powershell
# Run on the affected machine as the affected user
gpresult /H C:\Temp\gpresult.html /F
```
Open the report and examine the **Computer Configuration** and **User Configuration** sections. Look for the specific GPO under **Applied GPOs** or **Denied GPOs**.

### Step 3: Diagnose Denied GPOs
If the GPO appears under **Denied GPOs**, the most common reasons are:
- **Security Filtering**: The computer account or user is not in the security group specified in the GPO's Security Filtering.
  - In GPMC, check the **Scope** tab of the GPO. Verify the machine/user is a member of the listed group.
- **WMI Filter**: The GPO has a WMI filter that is returning false for this machine (e.g., filtering for OS version).
- **OU Scope**: The computer or user object is not in the OU the GPO is linked to.
- **Loopback Processing**: The user GPO may require loopback to be enabled on the computer GPO.

### Step 4: Check for Replication Issues
If the policy applies on some machines but not others, the issue may be DC replication lag.
```powershell
# Check replication status on domain controllers
repadmin /showrepl
# Force sync
repadmin /syncall /AdeP
```
