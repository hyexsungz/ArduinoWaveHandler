import os
import time
import platform
import uuid
from datetime import datetime

WIDTH = 70

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

def fake_voltage():
    import random
    return round(random.uniform(4.7, 5.2), 2)

def fake_temp():
    import random
    return round(random.uniform(28.0, 55.0), 2)

def fake_io():
    import random
    return {
        "D0": random.randint(0, 1),
        "D1": random.randint(0, 1),
        "D2": random.randint(0, 1),
        "D3": random.randint(0, 1),
        "D4": random.randint(0, 1),
        "D5": random.randint(0, 1),
        "D6": random.randint(0, 1),
        "D7": random.randint(0, 1),
        "D8": random.randint(0, 1),
        "D9": random.randint(0, 1),
        "D10": random.randint(0, 1),
        "D11": random.randint(0, 1),
        "D12": random.randint(0, 1),
        "D13": random.randint(0, 1),
    }

def render_io(io):
    return " ".join([f"{k}:{v}" for k, v in io.items()])

def run():
    session = str(uuid.uuid4())[:8].upper()
    cycle = 0

    clear()
    box([
        "ARDUINO BOARD EMULATOR - MEGA 2560",
        "════════════════════════════════════════════════════════════════",
        "ABOUT:",
        "Hardware abstraction layer for Arduino Mega board simulation.",
        "Provides virtual GPIO state, voltage monitoring, and thermal",
        "readouts for testing CLI command frameworks.",
        "",
        "SPECIFICATIONS:",
        "- MCU: ATmega2560",
        "- Digital IO: 54 Pins",
        "- PWM: 15 Channels",
        "- UART: 4 Ports",
        "- Clock: 16 MHz",
        "",
        f"SESSION    : {session}",
        f"PLATFORM   : {platform.system()}",
        f"START TIME : {datetime.now()}",
        "",
        "BOOTING VIRTUAL BOARD..."
    ])

    time.sleep(2)

    while True:
        cycle += 1
        io = fake_io()
        v = fake_voltage()
        t = fake_temp()

        clear()

        box([
            "ARDUINO MEGA 2560 - LIVE STATUS",
            "════════════════════════════════════════════════════════════════",
            f"CYCLE      : {cycle}",
            f"SESSION    : {session}",
            f"TIME       : {datetime.now()}",
            "",
            "POWER:",
            f"VOLTAGE    : {v} V",
            f"TEMPERATURE: {t} C",
            "",
            "GPIO STATE:",
            render_io(io),
            "",
            "SYSTEM:",
            "RUNNING VIRTUAL HARDWARE EMULATION",
            "MONITOR ACTIVE"
        ])

        time.sleep(1)

if __name__ == "__main__":
    run()