import time
import random
from datetime import datetime

DEVICES = [
    {"id": "ARD-001", "name": "Arduino Uno", "port": "COM3"},
    {"id": "ARD-002", "name": "ESP32", "port": "COM4"},
    {"id": "ARD-003", "name": "NodeMCU", "port": "COM5"},
    {"id": "ARD-004", "name": "Arduino Mega", "port": "COM6"}
]

SIGNAL_MODES = ["STABLE", "FLUCTUATING", "NOISY", "LOCKED"]

def banner():
    print()
    print("====================================================")
    print("        ArduinoWaveHandle Monitor Controller        ")
    print("====================================================")
    print()

def progress(title):
    print(title)

    for i in range(0, 101, 25):
        bar = "[" + "#" * (i // 25) + "-" * (4 - (i // 25)) + "]"
        print(f"\r{bar} {i}%", end="", flush=True)
        time.sleep(random.uniform(0.05, 0.2))

    print()
    print()

def generate_metrics():
    return {
        "cpu": random.randint(1, 95),
        "ram": random.randint(5, 90),
        "temp": round(random.uniform(30.0, 85.0), 2),
        "voltage": round(random.uniform(3.0, 5.2), 2),
        "packets": random.randint(100, 5000),
        "errors": random.randint(0, 10)
    }

def monitor_device(device):
    signal = random.choice(SIGNAL_MODES)
    metrics = generate_metrics()

    print("----------------------------------------------------")
    print(f"DEVICE ID          : {device['id']}")
    print(f"DEVICE NAME        : {device['name']}")
    print(f"PORT               : {device['port']}")
    print(f"SESSION TIME       : {datetime.now()}")
    print()

    progress("[INITIALIZING MONITOR]")
    progress("[READING SYSTEM METRICS]")
    progress("[ANALYZING SIGNAL FLOW]")

    print("[LIVE METRICS]")
    print(f"CPU USAGE          : {metrics['cpu']}%")
    print(f"RAM USAGE          : {metrics['ram']}%")
    print(f"TEMPERATURE        : {metrics['temp']} C")
    print(f"VOLTAGE            : {metrics['voltage']} V")
    print()

    print("[DATA FLOW]")
    print(f"PACKETS            : {metrics['packets']}")
    print(f"ERRORS             : {metrics['errors']}")
    print()

    print("[SIGNAL STATUS]")
    print(f"MODE               : {signal}")

    if metrics["errors"] > 7:
        status = "CRITICAL"
    elif metrics["errors"] > 3:
        status = "WARNING"
    else:
        status = "NORMAL"

    print(f"SYSTEM STATUS      : {status}")
    print()

    services = [
        "SERIAL LINK",
        "WAVE ENGINE",
        "SIGNAL PROCESSOR",
        "AUTH SYSTEM",
        "DEVICE DRIVER"
    ]

    print("[SERVICE HEALTH]")

    for service in services:
        state = random.choice(["OK", "OK", "OK", "DEGRADED"])
        print(f"{service:<18}: {state}")
        time.sleep(0.1)

    print()

    print("[MONITOR COMPLETE]")
    print("----------------------------------------------------")
    print()

def run(args=None):
    banner()

    print("[INITIALIZING MONITOR ENGINE]")
    time.sleep(0.4)

    print("LOADING SENSOR HUB")
    time.sleep(0.3)

    print("LOADING SIGNAL ANALYZER")
    time.sleep(0.3)

    print("LOADING METRICS ENGINE")
    time.sleep(0.3)

    print("LOADING DEVICE TRACKER")
    time.sleep(0.3)

    print()

    count = 0

    for device in DEVICES:
        monitor_device(device)
        count += 1
        time.sleep(0.6)

    print("[MONITOR SUMMARY]")
    print()
    print(f"TOTAL DEVICES MONITORED : {count}")
    print(f"ACTIVE CONNECTIONS      : {len(DEVICES)}")
    print(f"SIGNAL MODES AVAILABLE  : {len(SIGNAL_MODES)}")
    print()

    print("[ENGINE STATUS]")
    print("MONITOR ENGINE      : ACTIVE")
    print("SIGNAL ANALYZER     : ACTIVE")
    print("METRICS ENGINE      : ACTIVE")
    print("DEVICE TRACKER      : ACTIVE")
    print("SERIAL HUB          : ACTIVE")
    print()

    print("[MONITOR SESSION COMPLETE]")
    print()

if __name__ == "__main__":
    run()