import os
import time
import platform
import uuid
from datetime import datetime
import random

WIDTH = 78

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

def voltage():
    return round(random.uniform(4.6, 5.2), 3)

def temp():
    return round(random.uniform(26.0, 68.0), 2)

def io_state():
    return {f"D{i}": random.randint(0, 1) for i in range(14)}

def pwm_state():
    return {f"PWM{i}": random.randint(0, 255) for i in range(6)}

def analog_state():
    return {f"A{i}": random.randint(0, 1023) for i in range(8)}

def render_dict(d):
    return " ".join([f"{k}:{v}" for k, v in d.items()])

def run():
    session = str(uuid.uuid4())[:8].upper()
    boot_id = str(uuid.uuid4())[:12].upper()
    cycle = 0

    clear()
    box([
        "ARDUINO NANO EMULATOR CORE",
        "════════════════════════════════════════════════════════════════════════════",
        "ABOUT:",
        "Nano simulation module for embedded testing environments.",
        "Emulates ATmega328-based Nano behavior with lightweight memory footprint",
        "and simplified GPIO/PWM/ADC systems for rapid command testing.",
        "",
        "BOARD PROFILE:",
        "- MCU: ATmega328P",
        "- Digital Pins: 14 (D0-D13)",
        "- Analog Inputs: 8 (A0-A7)",
        "- PWM Channels: 6",
        "- UART: 1 Serial Interface",
        "- Clock Speed: 16 MHz",
        "",
        "SIMULATION FEATURES:",
        "- GPIO random state fluctuation",
        "- Analog sensor noise simulation",
        "- PWM signal variation engine",
        "- Power drift + thermal simulation",
        "- Nano-optimized low latency loop",
        "",
        f"BOOT ID   : {boot_id}",
        f"SESSION   : {session}",
        f"PLATFORM  : {platform.system()}",
        f"START TIME: {datetime.now()}",
        "",
        "INITIALIZING NANO CORE..."
    ])

    time.sleep(2)

    while True:
        cycle += 1

        clear()

        box([
            "ARDUINO NANO - LIVE SYSTEM MONITOR",
            "════════════════════════════════════════════════════════════════════════════",
            f"CYCLE      : {cycle}",
            f"SESSION    : {session}",
            f"TIME       : {datetime.now()}",
            "",
            "POWER:",
            f"VOLTAGE    : {voltage()} V",
            f"TEMP       : {temp()} °C",
            "",
            "DIGITAL I/O:",
            render_dict(io_state()),
            "",
            "ANALOG INPUTS:",
            render_dict(analog_state()),
            "",
            "PWM OUTPUTS:",
            render_dict(pwm_state()),
            "",
            "SERIAL:",
            "UART ACTIVE | BAUD 9600 | TX OK | RX OK",
            "",
            "STATUS:",
            "NANO CORE STABLE",
            "SIGNAL FLOW NORMAL",
            "DEVICE HEALTH OK"
        ])

        time.sleep(1)

if __name__ == "__main__":
    run()