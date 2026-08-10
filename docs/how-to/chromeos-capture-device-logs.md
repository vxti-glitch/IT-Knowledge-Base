---
title: Capture ChromeOS Device Logs
kb_id: HOW-260809234827
author: Tier 1 Support
category: How-To Guides
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: Low
tags:
- ChromeOS
- Troubleshooting
- Logs
---

## Summary
How to extract system logs (`net.log`, `messages`, `auth.log`) from a ChromeOS device for escalation to Tier 2 or Google Enterprise Support.

## Prerequisites for Tier 1 Technicians
- A USB flash drive (FAT32 formatted).
- Physical access to the Chromebook.

## Diagnostic Steps

1. **Access the Log Portal:**
   - Log into the Chromebook (or use Guest mode if permitted).
   - Open the Chrome browser and navigate to `chrome://network`.

2. **Generate System Logs:**
   - Click on the **Network State** tab.
   - Scroll to the bottom and click the **Store system logs** button.
   - Alternatively, navigate to `chrome://system`, click **Expand All**, and print to PDF.

3. **Extract via USB (Developer Mode):**
   If advanced logs are needed and the device is in Developer Mode:
   - Open a crosh shell (`Ctrl + Alt + T`).
   - Type `shell`.
   - Copy logs to the chronos Downloads folder:
   ```bash
   cp -r /var/log/* /home/chronos/user/Downloads/
   ```
   - Insert the USB drive and use the Files app to copy the logs over.
