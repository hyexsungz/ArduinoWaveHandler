import os
import time
import random
import uuid
import platform
from datetime import datetime

WIDTH = 60

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

def gen_wave():
    wave = []
    base = random.randint(5, 20)
    for i in range(60):
        spike = random.randint(-3, 3)
        val = max(0, base + spike + int(10 * (random.random() - 0.5)))
        wave.append(val)
    return wave

def render_wave(wave):
    max_v = max(wave) if wave else 1
    graph = ""
    for v in wave:
        h = int((v / max_v) * 8)
        graph += "▁▂▃▄▅▆▇█"[min(h, 7)]
    return graph

def stability(wave):
    avg = sum(wave) / len(wave)
    variance = sum((x - avg) ** 2 for x in wave) / len(wave)
    if variance < 10:
        return "STABLE"
    if variance < 25:
        return "NORMAL"
    if variance < 50:
        return "UNSTABLE"
    return "CRITICAL"

def run():
    session = str(uuid.uuid4())[:8].upper()
    cycle = 0

    clear()
    box([
        "ARDUINO WAVEHANDLE SYSTEM",
        "WAVE MONITOR MODULE",
        "════════════════════════════════════════════════",
        "ABOUT:",
        "Real-time waveform analysis engine for Arduino",
        "signal streams with stability detection and pattern",
        "visualization using dynamic amplitude mapping.",
        "",
        "FEATURES:",
        "- Waveform generation engine",
        "- Signal smoothing simulation",
        "- Stability variance detection",
        "- ASCII waveform renderer",
        "- Live analysis cycles",
        "",
        f"PLATFORM   : {platform.system()}",
        f"SESSION    : {session}",
        f"START TIME : {datetime.now()}",
        "",
        "INITIALIZING WAVE ENGINE..."
    ])

    time.sleep(2)

    while True:
        cycle += 1
        wave = gen_wave()
        graph = render_wave(wave)
        state = stability(wave)

        clear()

        box([
            "WAVE MONITOR LIVE ENGINE",
            "════════════════════════════════════════════════",
            f"CYCLE      : {cycle}",
            f"SESSION    : {session}",
            f"TIME       : {datetime.now()}",
            "",
            "WAVE ANALYSIS:",
            f"STATE      : {state}",
            f"PEAK       : {max(wave)}",
            f"AVG        : {round(sum(wave)/len(wave),2)}",
            "",
            "WAVEFORM:",
            graph,
            "",
            "STATUS:",
            "ANALYZING SIGNAL PATTERNS...",
            "MONITOR ACTIVE"
        ])

        time.sleep(1)

if __name__ == "__main__":
    run()