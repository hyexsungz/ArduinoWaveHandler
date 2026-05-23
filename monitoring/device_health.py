import os
import platform
import time
import random
import socket
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

def get_hostname():
    try:
        return socket.gethostname()
    except:
        return "unknown"

def get_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "0.0.0.0"

def fake_cpu():
    return random.randint(10, 95)

def fake_ram():
    return random.randint(20, 95)

def fake_disk():
    return random.randint(10, 98)

def fake_temp():
    return random.randint(30, 85)

def health_score(cpu, ram, disk, temp):
    score = 100
    if cpu > 85: score -= 25
    if ram > 85: score -= 25
    if disk > 90: score -= 20
    if temp > 75: score -= 20
    return max(0, score)

def status(score):
    if score > 80:
        return "OPTIMAL"
    if score > 60:
        return "STABLE"
    if score > 40:
        return "DEGRADED"
    return "CRITICAL"

def mini_bar(v):
    blocks = int(v / 10)
    return "[" + "█" * blocks + "-" * (10 - blocks) + "]"

def run():
    session = str(uuid.uuid4())[:8].upper()
    hostname = get_hostname()
    ip = get_ip()

    clear()

    box([
        "ARDUINO WAVEHANDLE SYSTEM",
        "DEVICE HEALTH MONITOR MODULE",
        "════════════════════════════════════════════════",
        "ABOUT:",
        "Full system diagnostics engine designed to simulate",
        "and monitor CPU, RAM, storage, temperature, network",
        "state, and overall device stability for Arduino CLI",
        "and monitoring framework integration.",
        "",
        "FEATURES:",
        "- Real-time system health simulation",
        "- CPU / RAM / Disk / Temp tracking",
        "- Network identity detection",
        "- Dynamic health scoring engine",
        "- Stability classification system",
        "",
        f"PLATFORM   : {platform.system()}",
        f"RELEASE    : {platform.release()}",
        f"NODE       : {hostname}",
        f"IP         : {ip}",
        f"SESSION    : {session}",
        f"TIME       : {datetime.now()}",
        "",
        "INITIALIZING DIAGNOSTIC CORE..."
    ])

    time.sleep(2)

    cycle = 0

    while True:
        cycle += 1

        cpu = fake_cpu()
        ram = fake_ram()
        disk = fake_disk()
        temp = fake_temp()

        score = health_score(cpu, ram, disk, temp)
        state = status(score)

        clear()

        box([
            "DEVICE HEALTH LIVE DIAGNOSTICS",
            "════════════════════════════════════════════════",
            f"CYCLE      : {cycle}",
            f"SESSION    : {session}",
            f"TIME       : {datetime.now()}",
            "",
            "SYSTEM LOAD:",
            f"CPU        : {cpu}% {mini_bar(cpu)}",
            f"RAM        : {ram}% {mini_bar(ram)}",
            f"DISK       : {disk}% {mini_bar(disk)}",
            f"TEMP       : {temp}°C {mini_bar(temp)}",
            "",
            "HEALTH ENGINE:",
            f"SCORE      : {score}/100",
            f"STATUS     : {state}",
            "",
            "NETWORK:",
            f"HOST       : {hostname}",
            f"IP         : {ip}",
            "",
            "MONITORING ACTIVE - REALTIME SYSTEM SCAN"
        ])

        time.sleep(1)

if __name__ == "__main__":
    run()