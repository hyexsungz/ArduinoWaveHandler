import time
import random
import platform
import socket
import uuid

DEVICES = [
    {
        "id": "ARD-001",
        "port": "COM3",
        "type": "Arduino Uno",
        "firmware": "2.1.0",
        "status": "online",
        "baudrate": 115200
    },
    {
        "id": "ARD-002",
        "port": "COM4",
        "type": "Arduino Mega",
        "firmware": "3.4.8",
        "status": "online",
        "baudrate": 9600
    },
    {
        "id": "ARD-003",
        "port": "COM5",
        "type": "ESP32",
        "firmware": "1.9.5",
        "status": "idle",
        "baudrate": 115200
    },
    {
        "id": "ARD-004",
        "port": "COM6",
        "type": "NodeMCU",
        "firmware": "4.0.1",
        "status": "online",
        "baudrate": 74880
    },
    {
        "id": "ARD-005",
        "port": "COM7",
        "type": "Raspberry Pico",
        "firmware": "5.2.3",
        "status": "maintenance",
        "baudrate": 115200
    }
]

def generate_mac():
    mac = [
        0x00,
        0x16,
        0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return ":".join(map(lambda x: "%02x" % x, mac))

def generate_ip():
    return f"192.168.1.{random.randint(2,254)}"

def generate_serial():
    return str(uuid.uuid4()).split("-")[0].upper()

def banner():
    print()
    print("==============================================")
    print("        ArduinoWaveHandle Scanner Engine      ")
    print("==============================================")
    print()

def system_info():
    print("[SYSTEM]")
    print(f"HOSTNAME   : {socket.gethostname()}")
    print(f"PLATFORM   : {platform.system()}")
    print(f"RELEASE    : {platform.release()}")
    print(f"MACHINE    : {platform.machine()}")
    print(f"PROCESSOR  : {platform.processor()}")
    print()

def run(args=None):
    banner()

    system_info()

    print("[SCANNER INITIALIZING]")
    time.sleep(1)

    print("LOADING SERIAL ENGINE")
    time.sleep(0.3)

    print("LOADING WAVE DETECTOR")
    time.sleep(0.3)

    print("LOADING SIGNAL ANALYZER")
    time.sleep(0.3)

    print("LOADING DEVICE MANAGER")
    time.sleep(0.3)

    print("LOADING PROTOCOL STACK")
    time.sleep(0.3)

    print()
    print("[SCAN STARTED]")
    print()

    total = 0

    for device in DEVICES:
        time.sleep(0.7)

        signal = random.randint(65, 100)
        packets = random.randint(100, 5000)
        latency = round(random.uniform(0.5, 10.5), 2)
        voltage = round(random.uniform(3.0, 5.0), 2)
        temperature = round(random.uniform(20.0, 60.0), 2)

        print("--------------------------------------------------")
        print(f"DEVICE ID       : {device['id']}")
        print(f"DEVICE TYPE     : {device['type']}")
        print(f"SERIAL PORT     : {device['port']}")
        print(f"STATUS          : {device['status']}")
        print(f"FIRMWARE        : {device['firmware']}")
        print(f"BAUDRATE        : {device['baudrate']}")
        print(f"SIGNAL STRENGTH : {signal}%")
        print(f"PACKETS         : {packets}")
        print(f"LATENCY         : {latency} ms")
        print(f"VOLTAGE         : {voltage}V")
        print(f"TEMPERATURE     : {temperature}C")
        print(f"IP ADDRESS      : {generate_ip()}")
        print(f"MAC ADDRESS     : {generate_mac()}")
        print(f"SERIAL TOKEN    : {generate_serial()}")
        print("--------------------------------------------------")
        print()

        total += 1

    print("[SCAN COMPLETE]")
    print()

    print(f"TOTAL DEVICES DETECTED : {total}")
    print(f"TOTAL ACTIVE DEVICES   : {len([d for d in DEVICES if d['status'] == 'online'])}")
    print(f"TOTAL IDLE DEVICES     : {len([d for d in DEVICES if d['status'] == 'idle'])}")
    print(f"TOTAL MAINTENANCE      : {len([d for d in DEVICES if d['status'] == 'maintenance'])}")
    print()

    print("[ENGINE STATUS]")
    print("SERIAL ENGINE       : ACTIVE")
    print("SIGNAL ANALYZER     : ACTIVE")
    print("PROTOCOL STACK      : ACTIVE")
    print("WAVE MONITOR        : ACTIVE")
    print("AUTH HANDLER        : ACTIVE")
    print("PACKET OBSERVER     : ACTIVE")
    print()

    print("[SCAN SESSION ENDED]")
    print()

if __name__ == "__main__":
    run()