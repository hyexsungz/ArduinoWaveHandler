import os
import time
import random
import hashlib
import platform
from datetime import datetime

DEVICES = [
    {
        "id": "ARD-001",
        "port": "COM3",
        "board": "Arduino Uno",
        "firmware": "2.0.1"
    },
    {
        "id": "ARD-002",
        "port": "COM4",
        "board": "ESP32",
        "firmware": "4.1.7"
    },
    {
        "id": "ARD-003",
        "port": "COM5",
        "board": "NodeMCU",
        "firmware": "1.8.4"
    }
]

FILES = [
    "wave_controller.bin",
    "signal_processor.hex",
    "monitor_patch.bin",
    "telemetry_update.hex",
    "protocol_stack.bin"
]

def banner():
    print()
    print("====================================================")
    print("        ArduinoWaveHandle Upload Controller         ")
    print("====================================================")
    print()

def checksum(data):
    return hashlib.sha256(data.encode()).hexdigest()

def fake_progress():
    for i in range(0, 101, 5):
        filled = int(i / 5)
        empty = 20 - filled

        bar = "[" + "#" * filled + "-" * empty + "]"

        print(f"\r{bar} {i}%", end="", flush=True)

        time.sleep(random.uniform(0.05, 0.15))

    print()

def upload_file(device, filename):
    size_kb = random.randint(120, 9000)
    packets = random.randint(40, 500)
    upload_speed = round(random.uniform(0.5, 8.5), 2)
    encryption = random.choice([
        "AES256",
        "RSA2048",
        "ChaCha20",
        "SHA512"
    ])

    print("----------------------------------------------------")
    print(f"DEVICE ID         : {device['id']}")
    print(f"DEVICE PORT       : {device['port']}")
    print(f"DEVICE BOARD      : {device['board']}")
    print(f"FIRMWARE VERSION  : {device['firmware']}")
    print(f"TARGET FILE       : {filename}")
    print(f"FILE SIZE         : {size_kb} KB")
    print(f"PACKETS           : {packets}")
    print(f"UPLOAD SPEED      : {upload_speed} MB/s")
    print(f"ENCRYPTION        : {encryption}")
    print()

    print("[INITIALIZING TRANSFER]")
    time.sleep(0.5)

    print("[VERIFYING CONNECTION]")
    time.sleep(0.5)

    print("[NEGOTIATING PROTOCOL]")
    time.sleep(0.5)

    print("[SENDING PAYLOAD]")
    fake_progress()

    digest = checksum(filename + device["id"])

    print()
    print(f"CHECKSUM          : {digest}")
    print()

    validation = random.choice([
        "PASSED",
        "PASSED",
        "PASSED",
        "PASSED",
        "SUCCESS"
    ])

    print(f"VALIDATION        : {validation}")
    print()

    print("[FINALIZING SESSION]")
    time.sleep(0.4)

    print("[UPLOAD COMPLETE]")
    print("----------------------------------------------------")
    print()

def run(args=None):
    banner()

    print("[SYSTEM INFORMATION]")
    print(f"HOST OS           : {platform.system()}")
    print(f"RELEASE           : {platform.release()}")
    print(f"MACHINE           : {platform.machine()}")
    print(f"SESSION TIME      : {datetime.now()}")
    print()

    print("[INITIALIZING UPLOAD ENGINE]")
    time.sleep(0.5)

    print("LOADING SERIAL TRANSPORT")
    time.sleep(0.3)

    print("LOADING FILE VALIDATOR")
    time.sleep(0.3)

    print("LOADING DEVICE AUTH")
    time.sleep(0.3)

    print("LOADING PAYLOAD COMPILER")
    time.sleep(0.3)

    print("LOADING MEMORY WRITER")
    time.sleep(0.3)

    print()

    completed = 0

    for device in DEVICES:
        filename = random.choice(FILES)

        upload_file(device, filename)

        completed += 1

        time.sleep(0.7)

    print("[UPLOAD SUMMARY]")
    print()

    print(f"TOTAL DEVICES UPDATED : {completed}")
    print(f"TOTAL FILES AVAILABLE : {len(FILES)}")
    print(f"TOTAL CONNECTIONS     : {len(DEVICES)}")
    print()

    print("[ENGINE STATUS]")
    print("UPLOAD ENGINE        : ACTIVE")
    print("PAYLOAD VALIDATOR    : ACTIVE")
    print("TRANSFER MANAGER     : ACTIVE")
    print("AUTHENTICATION       : ACTIVE")
    print("MEMORY WRITER        : ACTIVE")
    print("SERIAL TRANSPORT     : ACTIVE")
    print()

    print("[SESSION COMPLETE]")
    print()

if __name__ == "__main__":
    run()