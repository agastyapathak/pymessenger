# PyMessenger Wiki

## Project overview
PyMessenger is a Python-based local-network messenger for office or campus Wi‑Fi environments. It is designed to detect nearby devices on the same LAN and allow direct 1-on-1 text chat without internet access.

- Repository: https://github.com/agastyapathak/pymessenger
- Homepage: https://showcase-atlaspymessenger281912.lovable.app
- Language: Python

## What has been built so far
- LAN discovery using UDP broadcast
- Peer tracking with offline cleanup
- Direct messaging over TCP sockets
- Chat history per peer
- Privacy/stealth mode
- Workspace dashboard for nearby device scanning
- Bulk message self-test for reliability checks
- Terminal UI with commands like /users, /select, /back, /test, /quit

## Main files
- `pymessenger-main` — main messaging app and networking logic
- `pymessenger-workspace.py` — Wi‑Fi device scanning dashboard
- `security_privacy-Menu` — privacy/security module
- `README.md` — repo intro and setup notes
- `visual-showcase.pdf` — concept/showcase asset

## Homepage check
The repo homepage is:
https://showcase-atlaspymessenger281912.lovable.app

This looks like a product/demo landing page built with Lovable, and it matches the project concept.

## Current status
This repo is a working prototype / demo project, not a finished production application. The core idea is complete and functioning, but it still needs polish and documentation.

## Good next steps
- Clean up project structure into a proper package
- Add a real installation guide
- Improve cross-platform stability
- Add tests for message sending/receiving
- Add a better GUI or web client
- Document architecture and features more clearly

## Summary
PyMessenger already contains the main building blocks for a LAN-based messaging app: discovery, peer chat, privacy features, and a workspace dashboard. It is a strong prototype with a clear product direction.
