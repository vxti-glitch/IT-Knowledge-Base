---
title: macOS Admin Credentials Rejected for System Update
kb_id: FAQ-260809234827
author: Tier 1 Support
category: FAQ
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: Medium
tags:
- macOS
- Security
- Updates
---

## Summary
A local administrator or Jamf LAPS account is unable to authorize system updates or install software, despite the password being verified as correct. The prompt violently shakes to indicate a failure.

## Prerequisites for Tier 1 Technicians
- Access to Jamf Pro or the local LAPS password repository.
- Verify the user is actually typing the correct password.

## Diagnostic Steps

1. **Verify SecureToken Status:**
   On modern versions of macOS (APFS/FileVault), an admin account must possess a SecureToken to authorize OS-level changes.
   ```bash
   sysadminctl -secureTokenStatus <admin_username>
   ```
   If it returns `Secure token is DISABLED`, the account lacks necessary cryptographic privileges.

2. **Grant SecureToken (Requires an existing tokenized user):**
   If the standard user has a SecureToken but the admin does not, you must grant it using the standard user's credentials.
   ```bash
   sysadminctl -adminUser <tokenized_user> -adminPassword - -secureTokenOn <admin_username> -password -
   ```

3. **Check MDM Bootstrap Token:**
   If Jamf is managing the device, ensure the Bootstrap Token is escrowed.
   ```bash
   sudo profiles status -type bootstraptoken
   ```
   If not escrowed, force an escrow:
   ```bash
   sudo profiles install -type bootstraptoken
   ```
