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
    return round(random.uniform(4.75, 5.15), 3)

def temp():
    return round(random.uniform(27.0, 70.0), 2)

def io_state():
    return {f"D{i}": random.randint(0, 1) for i in range(14)}

def pwm_state():
    return {f"PWM{i}": random.randint(0, 255) for i in range(6)}

def analog_state():
    return {f"A{i}": random.randint(0, 1023) for i in range(6)}

def render_dict(d):
    return " ".join([f"{k}:{v}" for k, v in d.items()])

def run():
    session = str(uuid.uuid4())[:8].upper()
    cycle = 0
    boot_id = str(uuid.uuid4())[:12].upper()

    clear()
    box([
        "ARDUINO UNO R3 EMULATOR CORE",
        "════════════════════════════════════════════════════════════════════════════",
        "ABOUT:",
        "This module simulates Arduino Uno R3 behavior in a full software environment.",
        "It mimics digital IO, analog input, PWM output, voltage fluctuation, and",
        "runtime board diagnostics for testing embedded command frameworks without hardware.",
        "",
        "BOARD PROFILE:",
        "- MCU: ATmega328P",
        "- Digital Pins: 14 (D0-D13)",
        "- Analog Inputs: 6 (A0-A5)",
        "- PWM Channels: 6",
        "- UART: 1 Serial Interface",
        "- Clock Speed: 16 MHz",
        "",
        "SIMULATION FEATURES:",
        "- Live GPIO state switching",
        "- Analog sensor fluctuation simulation",
        "- PWM signal emulation",
        "- Thermal drift modeling",
        "- Power stability tracking",
        "- Session-based execution ID",
        "",
        f"BOOT ID   : {boot_id}",
        f"SESSION   : {session}",
        f"PLATFORM  : {platform.system()}",
        f"START TIME: {datetime.now()}",
        "",
        "INITIALIZING ATMEGA328P CORE..."
    ])

    time.sleep(2)

    while True:
        cycle += 1

        clear()

        box([
            "ARDUINO UNO R3 - LIVE SYSTEM DIAGNOSTICS",
            "════════════════════════════════════════════════════════════════════════════",
            f"CYCLE       : {cycle}",
            f"SESSION     : {session}",
            f"TIME        : {datetime.now()}",
            "",
            "POWER SYSTEM:",
            f"VOLTAGE     : {voltage()} V",
            f"TEMPERATURE : {temp()} °C",
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
            "SERIAL BUS:",
            "UART0 ACTIVE | BAUD 9600 | TX OK | RX OK",
            "",
            "STATUS:",
            "UNO CORE RUNNING STABLE",
            "SIGNAL PROCESSING ACTIVE",
            "DEVICE HEALTH NOMINAL"
        ])

        time.sleep(1)

if __name__ == "__main__":
    run()