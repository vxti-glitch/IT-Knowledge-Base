---
title: Provision ChromeOS WiFi Certificate
kb_id: HOW-260809234827
author: Tier 1 Support
category: How-To Guides
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: Medium
tags:
- ChromeOS
- WiFi
- Certificates
---

## Summary
How to manually deploy or verify an 802.1x EAP-TLS certificate on a ChromeOS device for enterprise wireless networks.

## Prerequisites for Tier 1 Technicians
- The organization's Root CA certificate (in `.pem` or `.crt` format).
- Access to Google Admin console.

## Diagnostic Steps

1. **Verify Google Admin Network Settings:**
   - Certificates should deploy automatically. Go to **Devices > Chrome > Networks > Wi-Fi**.
   - Ensure the 802.1x network is configured to use the correct Root CA.

2. **Manual Certificate Installation (Local Debugging):**
   If auto-deployment fails, manually test the certificate installation:
   - On the Chromebook, open Chrome and navigate to `chrome://settings/certificates`.
   - Click the **Authorities** tab.
   - Click **Import** and select the Root CA file.
   - Check the box for "Trust this certificate for identifying websites" and save.

3. **Connect to the Enterprise Network:**
   - Click the network icon in the system tray.
   - Select the Enterprise SSID.
   - Set `EAP method` to `TLS`.
   - Select the newly imported certificate in the `Server CA certificate` dropdown.
   - Click Connect.
