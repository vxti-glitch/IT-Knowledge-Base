---
title: "Provision ChromeOS WiFi Certificate"
author: "Tier 1 Support"
category: "How-To Guides"
last_updated: "2026-03-30"
kb_id: "HOW-260809234827"
tags: ["ChromeOS", "WiFi", "Certificates"]
---

## Summary[¶](#summary "Permanent link")

How to manually deploy or verify an 802.1x EAP-TLS certificate on a ChromeOS device for enterprise wireless networks.

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

* The organization’s Root CA certificate (in `.pem` or `.crt` format).
* Access to Google Admin console.

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

1. **Verify Google Admin Network Settings:**
2. Certificates should deploy automatically. Go to **Devices > Chrome > Networks > Wi-Fi**.
3. Ensure the 802.1x network is configured to use the correct Root CA.
4. **Manual Certificate Installation (Local Debugging):**  
   If auto-deployment fails, manually test the certificate installation:
5. On the Chromebook, open Chrome and navigate to `chrome://settings/certificates`.
6. Click the **Authorities** tab.
7. Click **Import** and select the Root CA file.
8. Check the box for “Trust this certificate for identifying websites” and save.
9. **Connect to the Enterprise Network:**
10. Click the network icon in the system tray.
11. Select the Enterprise SSID.
12. Set `EAP method` to `TLS`.
13. Select the newly imported certificate in the `Server CA certificate` dropdown.
14. Click Connect.