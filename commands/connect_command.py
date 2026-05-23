import time
import random
from datetime import datetime

DEVICES = [
    {"id": "ARD-001", "board": "Arduino Uno", "port": "COM3"},
    {"id": "ARD-002", "board": "ESP32", "port": "COM4"},
    {"id": "ARD-003", "board": "NodeMCU", "port": "COM5"},
    {"id": "ARD-004", "board": "Arduino Mega", "port": "COM6"},
    {"id": "ARD-005", "board": "WaveSensor", "port": "COM7"}
]

CONNECTION_MODES = [
    "SERIAL",
    "USB",
    "WIRELESS",
    "BLUETOOTH"
]

def banner():
    print()
    print("====================================================")
    print("        ArduinoWaveHandle Connection Controller     ")
    print("====================================================")
    print()

def progress(title):
    print(title)
    for i in range(0, 101, 20):
        bar = "[" + "#" * (i // 20) + "-" * (5 - (i // 20)) + "]"
        print(f"\r{bar} {i}%", end="", flush=True)
        time.sleep(random.uniform(0.05, 0.2))
    print()
    print()

def handshake(device):
    mode = random.choice(CONNECTION_MODES)

    latency = round(random.uniform(0.1, 5.0), 2)
    signal = random.randint(60, 100)
    retries = random.randint(0, 3)

    print("----------------------------------------------------")
    print(f"DEVICE ID          : {device['id']}")
    print(f"BOARD              : {device['board']}")
    print(f"PORT               : {device['port']}")
    print(f"TIME               : {datetime.now()}")
    print()

    progress("[INIT CONNECTION STACK]")
    progress("[SEARCHING DEVICE]")
    progress("[ESTABLISHING HANDSHAKE]")

    print("[CONNECTION INFO]")
    print(f"MODE               : {mode}")
    print(f"LATENCY            : {latency} ms")
    print(f"SIGNAL STRENGTH    : {signal}%")
    print(f"RETRY COUNT        : {retries}")
    print()

    if signal > 75 and retries < 2:
        status = "CONNECTED"
        auth = "VALID"
    else:
        status = "FAILED"
        auth = "INVALID"

    print("[AUTH RESULT]")
    print(f"STATUS             : {status}")
    print(f"AUTH               : {auth}")
    print()

    services = [
        "SERIAL LINK",
        "SIGNAL PIPE",
        "WAVE ENGINE",
        "DEVICE DRIVER"
    ]

    print("[SERVICE SYNC]")

    for s in services:
        state = random.choice(["SYNCED", "SYNCED", "SYNCED", "DELAYED"])
        print(f"{s:<15}: {state}")
        time.sleep(0.1)

    print()

    print("[CONNECTION COMPLETE]")
    print("----------------------------------------------------")
    print()

def run(args=None):
    banner()

    print("[INITIALIZING CONNECTION ENGINE]")
    time.sleep(0.4)

    print("LOADING NETWORK STACK")
    time.sleep(0.3)

    print("LOADING DEVICE DISCOVERY")
    time.sleep(0.3)

    print("LOADING HANDSHAKE MODULE")
    time.sleep(0.3)

    print("LOADING AUTH SYSTEM")
    time.sleep(0.3)

    print()

    total = 0

    for device in DEVICES:
        handshake(device)
        total += 1
        time.sleep(0.5)

    print("[CONNECTION SUMMARY]")
    print()
    print(f"DEVICES PROCESSED   : {total}")
    print(f"CONNECTION MODES    : {len(CONNECTION_MODES)}")
    print(f"TOTAL DEVICES       : {len(DEVICES)}")
    print()

    print("[ENGINE STATUS]")
    print("CONNECTION ENGINE   : ACTIVE")
    print("NETWORK STACK       : ACTIVE")
    print("HANDSHAKE MODULE    : ACTIVE")
    print("AUTH SYSTEM         : ACTIVE")
    print("DEVICE DISCOVERY    : ACTIVE")
    print()

    print("[SESSION COMPLETE]")
    print()

if __name__ == "__main__":
    run()