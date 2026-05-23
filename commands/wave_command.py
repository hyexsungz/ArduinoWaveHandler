import math
import time
import random
import statistics
from datetime import datetime

WAVE_TYPES = [
    "SINE",
    "SQUARE",
    "TRIANGLE",
    "SAWTOOTH",
    "PULSE"
]

CHANNELS = [
    "CH-A",
    "CH-B",
    "CH-C",
    "CH-D"
]

DEVICES = [
    "ARD-001",
    "ARD-002",
    "ARD-003",
    "ARD-004"
]

def banner():
    print()
    print("====================================================")
    print("         ArduinoWaveHandle Wave Controller          ")
    print("====================================================")
    print()

def create_wave(wave_type, samples=64):
    values = []

    for i in range(samples):
        angle = i / 5.0

        if wave_type == "SINE":
            value = math.sin(angle)

        elif wave_type == "SQUARE":
            value = 1 if math.sin(angle) >= 0 else -1

        elif wave_type == "TRIANGLE":
            value = (2 / math.pi) * math.asin(math.sin(angle))

        elif wave_type == "SAWTOOTH":
            value = 2 * (angle / math.pi - math.floor(0.5 + angle / math.pi))

        else:
            value = 1 if math.sin(angle) > 0.7 else -1

        noise = random.uniform(-0.08, 0.08)

        values.append(round(value + noise, 4))

    return values

def wave_stats(values):
    return {
        "max": round(max(values), 4),
        "min": round(min(values), 4),
        "avg": round(statistics.mean(values), 4),
        "dev": round(statistics.pstdev(values), 4)
    }

def draw_wave(values):
    for value in values[:32]:
        position = int((value + 1.5) * 18)

        if position < 0:
            position = 0

        if position > 60:
            position = 60

        graph = " " * position + "*"

        print(f"{value:>8} | {graph}")

def process_device(device):
    wave_type = random.choice(WAVE_TYPES)
    channel = random.choice(CHANNELS)

    frequency = random.randint(100, 8000)
    amplitude = round(random.uniform(0.5, 5.0), 2)
    phase = round(random.uniform(0.0, 360.0), 2)
    sample_rate = random.randint(1000, 96000)

    values = create_wave(wave_type)
    stats = wave_stats(values)

    print("----------------------------------------------------")
    print(f"DEVICE              : {device}")
    print(f"CHANNEL             : {channel}")
    print(f"WAVE TYPE           : {wave_type}")
    print(f"FREQUENCY           : {frequency} Hz")
    print(f"AMPLITUDE           : {amplitude} V")
    print(f"PHASE               : {phase} DEG")
    print(f"SAMPLE RATE         : {sample_rate} Hz")
    print(f"SESSION TIME        : {datetime.now()}")
    print()

    print("[WAVE ANALYSIS]")
    print(f"MAX VALUE           : {stats['max']}")
    print(f"MIN VALUE           : {stats['min']}")
    print(f"AVERAGE VALUE       : {stats['avg']}")
    print(f"STANDARD DEVIATION  : {stats['dev']}")
    print()

    print("[WAVE OUTPUT]")
    print()

    draw_wave(values)

    print()
    print("[SIGNAL PROCESSING]")
    print("FILTER              : ACTIVE")
    print("NOISE REDUCTION     : ENABLED")
    print("OSCILLATOR          : STABLE")
    print("SYNC STATUS         : LOCKED")
    print("WAVE STATE          : STREAMING")
    print()

    packets = random.randint(100, 1200)
    errors = random.randint(0, 2)

    print("[DATA FLOW]")
    print(f"PACKETS             : {packets}")
    print(f"ERRORS              : {errors}")
    print()

    print("[WAVE SESSION COMPLETE]")
    print("----------------------------------------------------")
    print()

def run(args=None):
    banner()

    print("[INITIALIZING WAVE ENGINE]")
    time.sleep(0.4)

    print("LOADING SIGNAL CORE")
    time.sleep(0.3)

    print("LOADING OSCILLATOR")
    time.sleep(0.3)

    print("LOADING FREQUENCY GENERATOR")
    time.sleep(0.3)

    print("LOADING FILTER SYSTEM")
    time.sleep(0.3)

    print("LOADING ANALYTICS ENGINE")
    time.sleep(0.3)

    print()

    total = 0

    for device in DEVICES:
        process_device(device)

        total += 1

        time.sleep(0.7)

    print("[GLOBAL SUMMARY]")
    print()

    print(f"DEVICES PROCESSED     : {total}")
    print(f"WAVE TYPES AVAILABLE  : {len(WAVE_TYPES)}")
    print(f"CHANNELS ACTIVE       : {len(CHANNELS)}")
    print()

    print("[ENGINE STATUS]")
    print("OSCILLATOR           : ACTIVE")
    print("SIGNAL ENGINE        : ACTIVE")
    print("WAVE ANALYZER        : ACTIVE")
    print("FILTER ENGINE        : ACTIVE")
    print("SYNC SYSTEM          : ACTIVE")
    print("OUTPUT STREAM        : ACTIVE")
    print()

    print("[WAVE ENGINE COMPLETE]")
    print()

if __name__ == "__main__":
    run()