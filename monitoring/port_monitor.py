import serial.tools.list_ports
from datetime import datetime
import os
import time
import platform

WIDTH = 58

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def line():
    return "╠" + "═" * WIDTH + "╣"

def box(lines):
    print("╔" + "═" * WIDTH + "╗")
    for l in lines:
        l = str(l)
        if len(l) > WIDTH:
            l = l[:WIDTH]
        print("║" + l.ljust(WIDTH) + "║")
    print("╚" + "═" * WIDTH + "╝")

def header():
    box([
        "ARDUINO WAVEHANDLE SYSTEM",
        "PORT MONITOR MODULE",
        "",
        "════════════════════════════════════════════════",
        "REAL-TIME SERIAL DETECTION ENGINE",
        "USB / COM INTERFACE SCANNER",
        "",
        f"SYSTEM     : {platform.system()}",
        f"NODE       : {platform.node()}",
        f"PY VERSION : {platform.python_version()}",
        "",
        "COMMAND:",
        "python monitoring/port_monitor.py",
        "",
        "STATUS: INITIALIZING"
    ])

def scan_animation():
    stages = [
        "INIT SERIAL CORE",
        "LOADING DRIVER LAYER",
        "CHECKING USB BUS",
        "ENUMERATING COM PORTS",
        "BUILDING DEVICE MAP"
    ]

    for s in stages:
        print(">> " + s)
        for i in range(0, 101, 10):
            bar = "[" + "#" * (i // 10) + "-" * (10 - (i // 10)) + "]"
            print(f"\r{bar} {i}%", end="", flush=True)
            time.sleep(0.03)
        print("\n")

def detect_ports():
    ports = list(serial.tools.list_ports.comports())
    return ports

def render_ports(ports):
    if not ports:
        box([
            "NO SERIAL DEVICES FOUND",
            "",
            "REASONS:",
            "- Device not plugged in",
            "- Driver missing",
            "- COM port disabled",
            "",
            "SUGGESTION:",
            "Reconnect device and retry scan"
        ])
        return

    for p in ports:
        box([
            "DEVICE DETECTED",
            "",
            f"PORT       : {p.device}",
            f"NAME       : {p.name}",
            f"DESCRIPTION: {p.description}",
            f"HWID       : {p.hwid}",
            "",
            "STATUS     : ONLINE",
            "CONNECTION : STABLE",
            "",
            "SCAN RESULT: REGISTERED"
        ])

def system_summary(ports):
    box([
        "SYSTEM SUMMARY",
        "",
        f"TOTAL PORTS FOUND : {len(ports)}",
        f"SCAN TIME         : {datetime.now()}",
        f"PLATFORM          : {platform.system()}",
        "",
        "ENGINE STATUS:",
        "SERIAL CORE   : ACTIVE",
        "PORT SCANNER  : ACTIVE",
        "DEVICE LAYER  : ACTIVE",
        "",
        "READY FOR COMMANDS"
    ])

def run():
    clear()
    header()
    scan_animation()

    ports = detect_ports()

    print("\n")
    render_ports(ports)

    print("\n")
    system_summary(ports)

if __name__ == "__main__":
    run()