import os
import time
import random
import platform
import uuid
from datetime import datetime

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

def gen_signal():
    base = random.randint(40, 95)
    noise = random.randint(-15, 15)
    strength = max(0, min(100, base + noise))
    return strength

def quality(strength):
    if strength > 85:
        return "ULTRA"
    if strength > 70:
        return "HIGH"
    if strength > 50:
        return "MEDIUM"
    if strength > 30:
        return "LOW"
    return "CRITICAL"

def waveform(v):
    bars = int(v / 10)
    return "▁" * (10 - bars) + "▇" * bars

def run():
    session = str(uuid.uuid4())[:8].upper()
    cycle = 0

    clear()
    box([
        "ARDUINO WAVEHANDLE SYSTEM",
        "SIGNAL MONITOR MODULE",
        "════════════════════════════════════════════════",
        "ABOUT:",
        "Signal monitoring engine for real-time waveform",
        "analysis, strength evaluation, and stability tracking",
        "across simulated Arduino communication channels.",
        "",
        "FEATURES:",
        "- Live signal strength tracking",
        "- Waveform visualization engine",
        "- Noise simulation layer",
        "- Quality classification system",
        "- Stability drift detection",
        "",
        f"PLATFORM   : {platform.system()}",
        f"SESSION    : {session}",
        f"START TIME : {datetime.now()}",
        "",
        "BOOTING SIGNAL ANALYZER..."
    ])

    time.sleep(2)

    while True:
        cycle += 1

        strength = gen_signal()
        q = quality(strength)
        wave = waveform(strength)
        noise = random.randint(0, 25)
        jitter = random.randint(0, 18)

        clear()

        box([
            "SIGNAL MONITOR LIVE ENGINE",
            "════════════════════════════════════════════════",
            f"CYCLE      : {cycle}",
            f"SESSION    : {session}",
            f"TIME       : {datetime.now()}",
            "",
            "SIGNAL METRICS:",
            f"STRENGTH   : {strength}%",
            f"QUALITY    : {q}",
            f"NOISE      : {noise}%",
            f"JITTER     : {jitter}ms",
            "",
            "WAVEFORM:",
            wave,
            "",
            "STATUS:",
            "ANALYZING CHANNEL STABILITY...",
            "MONITOR ACTIVE"
        ])

        time.sleep(1)

if __name__ == "__main__":
    run()