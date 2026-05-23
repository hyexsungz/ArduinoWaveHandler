import time
import random
from datetime import datetime

DEVICES = [
    {
        "id": "ARD-001",
        "board": "Arduino Uno",
        "port": "COM3"
    },
    {
        "id": "ARD-002",
        "board": "ESP32",
        "port": "COM4"
    },
    {
        "id": "ARD-003",
        "board": "NodeMCU",
        "port": "COM5"
    },
    {
        "id": "ARD-004",
        "board": "Arduino Mega",
        "port": "COM6"
    }
]

RESET_TYPES = [
    "SOFT_RESET",
    "HARD_RESET",
    "BOOTLOADER_RESET",
    "POWER_CYCLE"
]

def banner():
    print()
    print("====================================================")
    print("         ArduinoWaveHandle Reset Controller         ")
    print("====================================================")
    print()

def progress(title):
    print(title)

    for i in range(0, 101, 10):
        filled = int(i / 10)
        empty = 10 - filled

        bar = "[" + "#" * filled + "-" * empty + "]"

        print(f"\r{bar} {i}%", end="", flush=True)

        time.sleep(random.uniform(0.05, 0.15))

    print()
    print()

def reset_device(device):
    reset_type = random.choice(RESET_TYPES)

    uptime = random.randint(1000, 900000)
    memory_usage = random.randint(20, 90)
    cpu_load = random.randint(10, 95)
    voltage = round(random.uniform(3.1, 5.2), 2)

    print("----------------------------------------------------")
    print(f"DEVICE ID           : {device['id']}")
    print(f"BOARD TYPE          : {device['board']}")
    print(f"SERIAL PORT         : {device['port']}")
    print(f"RESET TYPE          : {reset_type}")
    print(f"SESSION TIME        : {datetime.now()}")
    print()

    print("[DEVICE STATUS BEFORE RESET]")
    print(f"UPTIME              : {uptime} seconds")
    print(f"MEMORY USAGE        : {memory_usage}%")
    print(f"CPU LOAD            : {cpu_load}%")
    print(f"VOLTAGE             : {voltage}V")
    print()

    progress("[DISCONNECTING ACTIVE CHANNELS]")
    progress("[CLEARING MEMORY CACHE]")
    progress("[RESETTING DEVICE STATE]")
    progress("[REINITIALIZING BOOT SEQUENCE]")

    new_uptime = random.randint(1, 5)
    new_memory = random.randint(5, 20)
    new_cpu = random.randint(1, 10)

    print("[DEVICE STATUS AFTER RESET]")
    print(f"UPTIME              : {new_uptime} seconds")
    print(f"MEMORY USAGE        : {new_memory}%")
    print(f"CPU LOAD            : {new_cpu}%")
    print(f"VOLTAGE             : {voltage}V")
    print()

    services = [
        "SIGNAL ENGINE",
        "WAVE MANAGER",
        "SERIAL HANDLER",
        "PROTOCOL STACK",
        "AUTH MODULE",
        "MONITOR ENGINE"
    ]

    print("[SERVICE VALIDATION]")

    for service in services:
        status = random.choice([
            "ONLINE",
            "ONLINE",
            "ONLINE",
            "ACTIVE"
        ])

        print(f"{service:<22}: {status}")

        time.sleep(0.1)

    print()

    packets = random.randint(10, 500)
    reconnect_time = round(random.uniform(0.2, 3.0), 2)

    print("[POST RESET ANALYSIS]")
    print(f"RECOVERED PACKETS    : {packets}")
    print(f"RECONNECT TIME       : {reconnect_time} seconds")
    print()

    print("[RESET STATUS]")
    print("RESULT               : SUCCESS")
    print("----------------------------------------------------")
    print()

def run(args=None):
    banner()

    print("[INITIALIZING RESET ENGINE]")
    time.sleep(0.4)

    print("LOADING POWER MANAGER")
    time.sleep(0.3)

    print("LOADING SERIAL CONTROLLER")
    time.sleep(0.3)

    print("LOADING BOOT HANDLER")
    time.sleep(0.3)

    print("LOADING MEMORY CLEANER")
    time.sleep(0.3)

    print("LOADING DEVICE VALIDATOR")
    time.sleep(0.3)

    print()

    completed = 0

    for device in DEVICES:
        reset_device(device)

        completed += 1

        time.sleep(0.6)

    print("[RESET SUMMARY]")
    print()

    print(f"TOTAL DEVICES RESET   : {completed}")
    print(f"RESET MODES AVAILABLE : {len(RESET_TYPES)}")
    print(f"ACTIVE CONNECTIONS    : {len(DEVICES)}")
    print()

    print("[ENGINE STATUS]")
    print("RESET ENGINE         : ACTIVE")
    print("BOOT HANDLER         : ACTIVE")
    print("POWER MANAGER        : ACTIVE")
    print("SERIAL CONTROLLER    : ACTIVE")
    print("MEMORY CLEANER       : ACTIVE")
    print("VALIDATION ENGINE    : ACTIVE")
    print()

    print("[RESET SESSION COMPLETE]")
    print()

if __name__ == "__main__":
    run()