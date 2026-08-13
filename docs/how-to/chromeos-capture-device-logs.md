---
title: "Capture ChromeOS Device Logs"
author: "Tier 1 Support"
category: "How-To Guides"
last_updated: "2026-03-16"
kb_id: "HOW-260809234827"
tags: ["ChromeOS", "Troubleshooting", "Logs"]
---

## Summary[¶](#summary "Permanent link")

How to extract system logs (`net.log`, `messages`, `auth.log`) from a ChromeOS device for escalation to Tier 2 or Google Enterprise Support.

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

* A USB flash drive (FAT32 formatted).
* Physical access to the Chromebook.

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

1. **Access the Log Portal:**
2. Log into the Chromebook (or use Guest mode if permitted).
3. Open the Chrome browser and navigate to `chrome://network`.
4. **Generate System Logs:**
5. Click on the **Network State** tab.
6. Scroll to the bottom and click the **Store system logs** button.
7. Alternatively, navigate to `chrome://system`, click **Expand All**, and print to PDF.
8. **Extract via USB (Developer Mode):**  
   If advanced logs are needed and the device is in Developer Mode:
9. Open a crosh shell (`Ctrl + Alt + T`).
10. Type `shell`.
11. Copy logs to the chronos Downloads folder:  
    `bash
    cp -r /var/log/* /home/chronos/user/Downloads/`
12. Insert the USB drive and use the Files app to copy the logs over.