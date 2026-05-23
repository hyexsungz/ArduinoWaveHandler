import time
import random
from datetime import datetime

PORTS = [
    {
        "name": "COM3",
        "device": "Arduino Uno",
        "status": "CONNECTED"
    },
    {
        "name": "COM4",
        "device": "ESP32",
        "status": "CONNECTED"
    },
    {
        "name": "COM5",
        "device": "NodeMCU",
        "status": "CONNECTED"
    },
    {
        "name": "COM6",
        "device": "Arduino Mega",
        "status": "CONNECTED"
    },
    {
        "name": "COM7",
        "device": "WaveSensor",
        "status": "IDLE"
    }
]

BAUD_RATES = [
    9600,
    19200,
    38400,
    57600,
    115200
]

PARITY_MODES = [
    "NONE",
    "EVEN",
    "ODD"
]

STOP_BITS = [
    1,
    2
]

def banner():
    print()
    print("====================================================")
    print("          ArduinoWaveHandle Port Manager            ")
    print("====================================================")
    print()

def progress(title):
    print(title)

    for i in range(0, 101, 20):
        filled = int(i / 20)
        empty = 5 - filled

        bar = "[" + "#" * filled + "-" * empty + "]"

        print(f"\r{bar} {i}%", end="", flush=True)

        time.sleep(random.uniform(0.05, 0.15))

    print()
    print()

def analyze_port(port):
    baud = random.choice(BAUD_RATES)
    parity = random.choice(PARITY_MODES)
    stop = random.choice(STOP_BITS)

    packets_in = random.randint(50, 5000)
    packets_out = random.randint(50, 5000)

    latency = round(random.uniform(0.2, 8.5), 2)
    signal = random.randint(70, 100)

    print("----------------------------------------------------")
    print(f"PORT NAME           : {port['name']}")
    print(f"DEVICE TYPE         : {port['device']}")
    print(f"PORT STATUS         : {port['status']}")
    print(f"SCAN TIME           : {datetime.now()}")
    print()

    progress("[SCANNING SERIAL CHANNEL]")
    progress("[READING PORT PARAMETERS]")
    progress("[CHECKING SIGNAL STATE]")

    print("[PORT CONFIGURATION]")
    print(f"BAUD RATE           : {baud}")
    print(f"PARITY MODE         : {parity}")
    print(f"STOP BITS           : {stop}")
    print()

    print("[TRAFFIC ANALYSIS]")
    print(f"PACKETS IN          : {packets_in}")
    print(f"PACKETS OUT         : {packets_out}")
    print(f"LATENCY             : {latency} ms")
    print(f"SIGNAL QUALITY      : {signal}%")
    print()

    states = [
        "LISTENING",
        "READY",
        "STREAMING",
        "ACTIVE"
    ]

    current_state = random.choice(states)

    print("[PORT STATE]")
    print(f"CURRENT MODE        : {current_state}")
    print("HANDSHAKE           : SUCCESS")
    print("AUTH STATUS         : VALID")
    print("SERIAL LOCK         : STABLE")
    print()

    protocols = [
        "UART",
        "SERIAL",
        "WAVE-LINK",
        "PROTO-X"
    ]

    print("[SUPPORTED PROTOCOLS]")

    for protocol in protocols:
        print(f"{protocol:<20}: ENABLED")

        time.sleep(0.1)

    print()

    print("[PORT ANALYSIS COMPLETE]")
    print("----------------------------------------------------")
    print()

def run(args=None):
    banner()

    print("[INITIALIZING PORT ENGINE]")
    time.sleep(0.4)

    print("LOADING SERIAL DETECTOR")
    time.sleep(0.3)

    print("LOADING DEVICE ANALYZER")
    time.sleep(0.3)

    print("LOADING SIGNAL VALIDATOR")
    time.sleep(0.3)

    print("LOADING CONNECTION MANAGER")
    time.sleep(0.3)

    print("LOADING TRAFFIC ANALYZER")
    time.sleep(0.3)

    print()

    scanned = 0

    for port in PORTS:
        analyze_port(port)

        scanned += 1

        time.sleep(0.5)

    print("[PORT SUMMARY]")
    print()

    print(f"TOTAL PORTS SCANNED  : {scanned}")
    print(f"ACTIVE DEVICES       : {len(PORTS)}")
    print(f"SUPPORTED BAUD RATES : {len(BAUD_RATES)}")
    print()

    print("[ENGINE STATUS]")
    print("PORT ENGINE         : ACTIVE")
    print("SERIAL DETECTOR     : ACTIVE")
    print("SIGNAL VALIDATOR    : ACTIVE")
    print("TRAFFIC ANALYZER    : ACTIVE")
    print("DEVICE ANALYZER     : ACTIVE")
    print("CONNECTION MANAGER  : ACTIVE")
    print()

    print("[PORT SESSION COMPLETE]")
    print()

if __name__ == "__main__":
    run()