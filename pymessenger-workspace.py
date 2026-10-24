#!/usr/init/env python3
"""
Search nearby Devices with PyMessenger

Code: https://github.com/agastyapathak
"""

import socket
import threading
import json
import time
import sys
import subprocess
import platform
from datetime import datetime

# --- CONFIGURATION ---
UDP_PORT = 50000          # Port used by PyMessenger for active detection
BUFFER_SIZE = 4096


def get_local_ip():
    """Finds the actual local network (LAN/Wi-Fi) IP address of this computer."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class PyMessengerWorkspace:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.local_ip = get_local_ip()
        self.running = True

        # Discovered devices dictionary:
        # key = ip, value = {"name": str, "type": str, "pymessenger": bool, "online": bool, "python_compat": bool, "last_seen": float}
        self.devices = {}
        self.devices_lock = threading.Lock()

        # Add local machine by default
        self.devices[self.local_ip] = {
            "name": f"{self.hostname} (This PC)",
            "type": f"Workstation ({platform.system()})",
            "pymessenger": True,
            "online": True,
            "python_compat": True,
            "last_seen": time.time()
        }

    def start(self):
        """Starts background network discovery threads and launches the interactive workspace UI."""
        threading.Thread(target=self._listen_pymessenger_broadcasts, daemon=True).start()
        threading.Thread(target=self._background_subnet_scanner, daemon=True).start()

        self._run_workspace_ui()

    # =====================================================================
    # BACKGROUND NETWORK SCANNING & DETECTION LOGIC
    # =====================================================================
    def _listen_pymessenger_broadcasts(self):
        """Listens for active PyMessenger UDP broadcasts (Green Dot detection)."""
        listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if hasattr(socket, "SO_REUSEPORT"):
            try:
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except OSError:
                pass

        try:
            listener.bind(("", UDP_PORT))
        except Exception:
            return

        while self.running:
            try:
                data, addr = listener.recvfrom(BUFFER_SIZE)
                info = json.loads(data.decode("utf-8"))
                if info.get("type") == "PYMSG_HELLO":
                    ip = addr[0]
                    name = info.get("name", "Unknown PyMessenger User")
                    with self.devices_lock:
                        self.devices[ip] = {
                            "name": name,
                            "type": "PyMessenger Node (LAN)",
                            "pymessenger": True,
                            "online": True,
                            "python_compat": True,
                            "last_seen": time.time()
                        }
            except Exception:
                continue
        listener.close()

    def _background_subnet_scanner(self):
        """Actively pings local subnet IP addresses to discover online devices (Blue/Red Dot assignment)."""
        base_subnet = ".".join(self.local_ip.split(".")[:3]) + "."

        while self.running:
            # Scan a subset of local IPs (e.g., .1 to .50 for fast response)
            for i in range(1, 51):
                if not self.running:
                    break
                target_ip = base_subnet + str(i)
                if target_ip == self.local_ip:
                    continue

                # Quick socket connection check on common ports (or ping) to see if online
                is_online = self._ping_ip(target_ip)
                if is_online:
                    try:
                        hostname = socket.gethostbyaddr(target_ip)[0]
                    except Exception:
                        hostname = f"Device-{target_ip.split('.')[-1]}"

                    with self.devices_lock:
                        if target_ip not in self.devices:
                            # Classify device type and dot status
                            # If name suggests mobile/printer/router vs computer
                            lower_name = hostname.lower()
                            if any(k in lower_name for k in ["iphone", "android", "ipad", "phone"]):
                                dev_type = "Mobile / Tablet"
                                python_compat = False
                            elif any(k in lower_name for k in ["router", "gateway", "print"]):
                                dev_type = "Network / Peripheral"
                                python_compat = False
                            else:
                                dev_type = "Computer / Server"
                                python_compat = True  # Assumed compatible if standard PC

                            self.devices[target_ip] = {
                                "name": hostname,
                                "type": dev_type,
                                "pymessenger": False,
                                "online": True,
                                "python_compat": python_compat,
                                "last_seen": time.time()
                            }
                        else:
                            self.devices[target_ip]["online"] = True
                            self.devices[target_ip]["last_seen"] = time.time()
            time.sleep(10.0)

    def _ping_ip(self, ip):
        """Performs a fast socket connection test on common ports to verify if a device is online."""
        for port in [50001, 80, 443, 22]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                result = s.connect_ex((ip, port))
                s.close()
                if result == 0:
                    return True
            except Exception:
                pass
        return False

    # =====================================================================
    # WORKSPACE UI & COMMAND HANDLER
    # =====================================================================
    def _print_banner(self):
        print("=" * 70)
        print(" PyMessenger Workspace by Agastya Pathak")
        print("=" * 70)
        print(f" Local Wi-Fi IP : {self.local_ip}")
        print(" Legend: 🟢 Active on PyMessenger | 🔵 Online / VS Code Active | 🔴 Incompatible (No Python)")
        print("-" * 70)

    def _render_dashboard(self):
        self._print_banner()
        with self.devices_lock:
            dev_list = list(self.devices.items())

        if not dev_list:
            print("\n[i] Scanning local Wi-Fi network for devices...")
        else:
            print("\n--- Connected Wi-Fi Devices Dashboard ---")
            for idx, (ip, d) in enumerate(dev_list, start=1):
                # Determine Dot status
                if d.get("pymessenger"):
                    dot = "🟢"
                    status_text = "Active on PyMessenger"
                elif d.get("online") and d.get("python_compat"):
                    dot = "🔵"
                    status_text = "Online / VS Code Active"
                else:
                    dot = "🔴"
                    status_text = "Incompatible Device / No Python"

                print(f"  [{idx}] {dot} {d['name']} ({ip})")
                print(f"      Type   : {d['type']}")
                print(f"      Status : {status_text}")
                print("-" * 55)

        print("\n Available Command:")
        print("   /refresh -> Re-scan local Wi-Fi network & update dashboard")
        print("=" * 70)

    def _run_workspace_ui(self):
        self._render_dashboard()

        while self.running:
            try:
                user_input = input("Workspace> ").strip()
                if not user_input:
                    continue

                if user_input.lower() == "/refresh":
                    print("\n🔄 Refreshing local Wi-Fi scan and device states...")
                    time.sleep(0.5)
                    self._render_dashboard()

                elif user_input.lower() in ("/quit", "/exit"):
                    print("Closing PyMessenger Workspace...")
                    self.running = False
                    break
                else:
                    print("[!] Unknown command. Type '/refresh' to update the dashboard.")

            except (KeyboardInterrupt, EOFError):
                print("\nClosing PyMessenger Workspace...")
                self.running = False
                break


if __name__ == "__main__":
    app = PyMessengerWorkspace()
    app.start()
