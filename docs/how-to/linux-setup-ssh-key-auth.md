---
title: "Setup SSH Key Authentication"
author: "Tier 1 Support"
category: "How-To Guides"
last_updated: "2026-03-01"
kb_id: "HOW-260809234827"
tags: ["Linux", "SSH", "Security"]
---

## Summary[¶](#summary "Permanent link")

How to generate an SSH key pair on a client machine and configure a Linux server to accept the key for passwordless authentication.

## Prerequisites for Tier 1 Technicians[¶](#prerequisites-for-tier-1-technicians "Permanent link")

* Command-line access to the client machine.
* Current password access to the target Linux server.

## Diagnostic Steps[¶](#diagnostic-steps "Permanent link")

1. **Generate the Key Pair (Client Side):**  
   Run the following on the user’s local machine to generate an ED25519 key.  
   `bash
   ssh-keygen -t ed25519 -C "user@company.com"`  
   Accept the default file location (`~/.ssh/id_ed25519`) and optionally set a passphrase.
2. **Copy the Public Key to the Server:**  
   Use `ssh-copy-id` to push the public key to the server’s `authorized_keys` file.  
   `bash
   ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server_ip_or_hostname`
3. **Test Authentication:**  
   Attempt to SSH into the server. It should authenticate using the key rather than prompting for the server password.  
   `bash
   ssh user@server_ip_or_hostname`
4. **Troubleshooting Permissions:**  
   If the server still prompts for a password, verify the server-side permissions:  
   `bash
   # On the server:
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys`