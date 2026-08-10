---
title: Active Directory Account Lockout
kb_id: FAQ-050
author: Tier 1 Support
category: FAQ
date_added: '2026-03-10'
last_updated: '2026-06-22'
severity: High
tags:
- Windows
- ActiveDirectory
- Security
- Authentication
---

## Summary
An Active Directory (AD) user account becomes unexpectedly locked out, preventing the user from logging into their workstation, VPN, or Microsoft 365 services. This is one of the most common escalation tickets in enterprise environments and can stem from multiple sources: stale cached credentials, a misconfigured mobile device, or a legitimate brute-force attempt.

## Prerequisites for Tier 1 Technicians
- Read access to Active Directory Users and Computers (ADUC) or Active Directory Administrative Center (ADAC).
- Access to the domain controller event logs (via Event Viewer or a SIEM).
- LockoutStatus.exe tool (from Microsoft) recommended.

## Diagnostic Steps

### Step 1: Confirm the Account is Locked
Open an elevated PowerShell session and verify the lock state:
```powershell
Get-ADUser -Identity "john.doe" -Properties LockedOut, BadLogonCount, BadPasswordTime, LastLogonDate | Select-Object Name, LockedOut, BadLogonCount, BadPasswordTime
```
If `LockedOut` returns `True`, proceed.

### Step 2: Unlock the Account Immediately
Provide immediate relief to the user while you investigate the root cause.
```powershell
Unlock-ADAccount -Identity "john.doe"
```
Inform the user they can attempt to log in again. However, do **not** close the ticket — identify the source to prevent immediate re-lockout.

### Step 3: Identify the Lockout Source
Use the Microsoft Lockout Status tool or query the Security event log on the PDC Emulator:
```powershell
# Find the PDC Emulator
(Get-ADDomain).PDCEmulator

# Query Security log for lockout events (Event ID 4740) on the PDC
Get-WinEvent -ComputerName "dc01.corp.local" -FilterHashtable @{LogName='Security'; Id=4740} |
    Where-Object {$_.Properties[0].Value -eq "john.doe"} |
    Select-Object TimeCreated, Message | Format-List
```
The `Caller Computer Name` field in Event ID 4740 identifies which machine is triggering the lockouts.

### Step 4: Remediate on the Source Machine
Navigate to or remote into the identified machine and check for:
- **Stale saved credentials**: Open `Credential Manager` (Control Panel) and remove any stored entries for domain resources.
- **Connected mobile devices**: Check if the user's phone or tablet has a configured Exchange ActiveSync account using an old password.
- **Scheduled tasks running as the user**: Open Task Scheduler on the source machine and check if any tasks are running under the user's credentials.
- **Running services**: In `services.msc`, check if any service is configured with the user's domain account.
- **Mapped drives with saved credentials**: Run `net use` to check for any mapped drives authenticating as that user.

### Step 5: Force a Password Change if Compromised
If the lockout pattern suggests a brute-force or credential stuffing attack:
```powershell
Set-ADAccountPassword -Identity "john.doe" -Reset -NewPassword (ConvertTo-SecureString "NewS3cur3P@ss!" -AsPlainText -Force)
Set-ADUser -Identity "john.doe" -ChangePasswordAtLogon $true
```
Notify the security team via your established incident response procedure.
