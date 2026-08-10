---
title: Reset SMC and PRAM
kb_id: HOW-260809234827
author: Tier 1 Support
category: How-To Guides
date_added: '2026-05-15'
last_updated: '2026-06-20'
severity: Medium
tags:
- macOS
- Hardware
- Reset
---

## Summary
How to perform a System Management Controller (SMC) and Parameter RAM (PRAM/NVRAM) reset on Intel-based Macs to resolve hardware oddities (battery not charging, fan noise, display issues).

## Prerequisites for Tier 1 Technicians
- Physical access to the Mac.
- Note: **Apple Silicon (M1/M2/M3) Macs do not have a traditional SMC/NVRAM reset process.** A simple reboot performs similar checks.

## Diagnostic Steps

1. **PRAM/NVRAM Reset (Intel Macs):**
   - Shut down the Mac.
   - Turn it on and immediately press and hold these four keys together: **Option, Command, P, and R**.
   - Hold them for about 20 seconds, during which the Mac might appear to restart.
   - Release the keys after the second startup sound, or after the Apple logo appears and disappears for the second time.

2. **SMC Reset (MacBooks with T2 Security Chip):**
   - Shut down the Mac.
   - Press and hold the power button for 10 seconds, then release. Wait a few seconds, then turn it on.
   - If issues persist, shut down again. Press and hold the **right Shift**, **left Option**, and **left Control** keys for 7 seconds. Keep holding them and press the **Power** button for another 7 seconds.
   - Release all keys, wait a few seconds, and turn on the Mac.

3. **SMC Reset (Desktop Intel Macs):**
   - Shut down the Mac and unplug the power cord.
   - Wait 15 seconds.
   - Plug the power cord back in. Wait 5 seconds, then press the power button.
