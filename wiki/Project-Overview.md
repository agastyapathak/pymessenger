# Project Overview

## What this repo does
This repository is a local-network text messenger built in Python. It uses the same Wi‑Fi network to discover nearby devices and supports direct messaging between them.

## Built so far
- UDP broadcast-based peer discovery
- TCP-based direct chat
- Peer tracking and timeouts
- Terminal UI for selecting users and chatting
- Privacy/security mode
- Workspace scan of online devices
- Bulk self-test message validation

## Notes from the code review
The main app logic is in `pymessenger-main` and it already contains the core networking behavior. The app identifies nearby peers, tracks them in memory, handles message delivery, and offers a chat interface through the terminal.

The `pymessenger-workspace.py` file adds a local device scanning dashboard and classification of devices. The `security_privacy-Menu` file adds a stealth feature and an office network dashboard demo.

## Summary
The repo is a solid proof-of-concept for a LAN chat app with privacy and local discovery features. It is ready for further refinement into a cleaner product version.
