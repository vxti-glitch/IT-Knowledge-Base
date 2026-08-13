---
title: "Reset SMC and PRAM"
author: "Tier 1 Support"
category: "How-To Guides"
last_updated: "2026-07-03"
kb_id: "HOW-260809234827"
tags: ["macOS", "Hardware", "Reset"]
---

## Summary[¶](#summary "Permanent link")

How to perform a System Management Controller (SMC) and Parameter RAM (PRAM/NVRAM) reset on Intel-based Macs to resolve hardware oddities (battery not charging, fan noise, display issues).

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

* Physical access to the Mac.
* Note: **Apple Silicon (M1/M2/M3) Macs do not have a traditional SMC/NVRAM reset process.** A simple reboot performs similar checks.

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

1. **PRAM/NVRAM Reset (Intel Macs):**
2. Shut down the Mac.
3. Turn it on and immediately press and hold these four keys together: **Option, Command, P, and R**.
4. Hold them for about 20 seconds, during which the Mac might appear to restart.
5. Release the keys after the second startup sound, or after the Apple logo appears and disappears for the second time.
6. **SMC Reset (MacBooks with T2 Security Chip):**
7. Shut down the Mac.
8. Press and hold the power button for 10 seconds, then release. Wait a few seconds, then turn it on.
9. If issues persist, shut down again. Press and hold the **right Shift**, **left Option**, and **left Control** keys for 7 seconds. Keep holding them and press the **Power** button for another 7 seconds.
10. Release all keys, wait a few seconds, and turn on the Mac.
11. **SMC Reset (Desktop Intel Macs):**
12. Shut down the Mac and unplug the power cord.
13. Wait 15 seconds.
14. Plug the power cord back in. Wait 5 seconds, then press the power button.