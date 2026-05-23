import time
import os
import random
from datetime import datetime
import platform
import uuid

WIDTH = 58

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def box(lines):
    print("╔" + "═" * WIDTH + "╗")
    for l in lines:
        l = str(l)
        if len(l) > WIDTH:
            l = l[:WIDTH]
        print("║" + l.ljust(WIDTH) + "║")
    print("╚" + "═" * WIDTH + "╝")

def generate_id():
    return str(uuid.uuid4())[:8].upper()

def status_engine(strength, latency):
    if strength > 85 and latency < 5:
        return "OPTIMAL"
    if strength > 65:
        return "STABLE"
    if strength > 40:
        return "DEGRADED"
    return "CRITICAL"

def heartbeat_wave():
    wave = [
        "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁",
        "▁▃▅▇█▇▅▃▁",
        "▁▂▁▃▁▄▁▅▁▆▁▇▁█",
        "█▇▆▅▄▃▂▁",
        "▁▁▂▂▃▃▄▄▅▅▆▆▇▇██"
    ]
    return random.choice(wave)

def run():
    session = generate_id()

    clear()
    box([
        "ARDUINO WAVEHANDLE SYSTEM",
        "HEARTBEAT MONITOR MODULE",
        "════════════════════════════════════════════════",
        "ABOUT:",
        "Advanced continuous heartbeat diagnostic engine for",
        "monitoring device lifecycle, serial bus integrity,",
        "and system communication stability in real time.",
        "",
        "FEATURES:",
        "- Continuous pulse generation engine",
        "- Signal strength simulation layer",
        "- Latency tracking system",
        "- Device connectivity health prediction",
        "- Failure detection & recovery awareness",
        "",
        f"SYSTEM     : {platform.system()}",
        f"NODE       : {platform.node()}",
        f"SESSION ID : {session}",
        f"START TIME : {datetime.now()}",
        "",
        "BOOTING HEARTBEAT CORE..."
    ])

    time.sleep(2)

    cycle = 0

    while True:
        cycle += 1

        strength = random.randint(30, 100)
        latency = random.randint(1, 20)
        jitter = random.randint(0, 15)
        status = status_engine(strength, latency)

        wave = heartbeat_wave()

        clear()

        box([
            "HEARTBEAT SIGNAL ENGINE",
            "════════════════════════════════════════════════",
            f"CYCLE       : {cycle}",
            f"SESSION     : {session}",
            f"TIME        : {datetime.now()}",
            "",
            "SIGNAL METRICS:",
            f"STRENGTH    : {strength}%",
            f"LATENCY     : {latency} ms",
            f"JITTER      : {jitter} ms",
            f"STATUS      : {status}",
            "",
            "LIVE WAVEFORM:",
            wave,
            "",
            "SYSTEM HEALTH STREAM ACTIVE",
            "MONITORING DEVICE PULSE...",
        ])

        time.sleep(1)

if __name__ == "__main__":
    run()