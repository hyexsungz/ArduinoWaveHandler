import time
import random
import math
import statistics

CHANNELS = [
    "ALPHA",
    "BETA",
    "GAMMA",
    "DELTA",
    "OMEGA"
]

SIGNAL_TYPES = [
    "DIGITAL",
    "ANALOG",
    "HYBRID",
    "PULSE",
    "RF"
]

DEVICES = [
    "ARD-001",
    "ARD-002",
    "ARD-003",
    "ARD-004",
    "ARD-005"
]

def banner():
    print()
    print("====================================================")
    print("        ArduinoWaveHandle Signal Controller         ")
    print("====================================================")
    print()

def generate_signal_samples(count=64):
    samples = []

    for i in range(count):
        value = math.sin(i / 4.0) * random.uniform(0.8, 1.2)
        value += random.uniform(-0.2, 0.2)
        samples.append(round(value, 4))

    return samples

def analyze_signal(samples):
    peak = max(samples)
    minimum = min(samples)
    average = round(statistics.mean(samples), 4)
    deviation = round(statistics.pstdev(samples), 4)

    return {
        "peak": peak,
        "minimum": minimum,
        "average": average,
        "deviation": deviation
    }

def display_bar(value):
    normalized = int((value + 1.5) * 10)

    if normalized < 0:
        normalized = 0

    if normalized > 40:
        normalized = 40

    return "#" * normalized

def run(args=None):
    banner()

    print("[INITIALIZING SIGNAL ENGINE]")
    time.sleep(0.5)

    print("LOADING RF MODULE")
    time.sleep(0.3)

    print("LOADING DIGITAL FILTER")
    time.sleep(0.3)

    print("LOADING FREQUENCY ANALYZER")
    time.sleep(0.3)

    print("LOADING CHANNEL MANAGER")
    time.sleep(0.3)

    print("LOADING TELEMETRY SYSTEM")
    time.sleep(0.3)

    print()
    print("[SIGNAL SESSION STARTED]")
    print()

    session_total = 0

    for device in DEVICES:
        channel = random.choice(CHANNELS)
        signal_type = random.choice(SIGNAL_TYPES)

        frequency = random.randint(100, 5000)
        bandwidth = random.randint(10, 500)
        strength = random.randint(60, 100)
        noise = round(random.uniform(0.01, 0.50), 3)
        latency = round(random.uniform(0.1, 10.0), 2)
        packets = random.randint(1000, 9000)

        samples = generate_signal_samples()
        analysis = analyze_signal(samples)

        print("----------------------------------------------------")
        print(f"DEVICE             : {device}")
        print(f"CHANNEL            : {channel}")
        print(f"SIGNAL TYPE        : {signal_type}")
        print(f"FREQUENCY          : {frequency} Hz")
        print(f"BANDWIDTH          : {bandwidth} MHz")
        print(f"SIGNAL STRENGTH    : {strength}%")
        print(f"NOISE LEVEL        : {noise}")
        print(f"LATENCY            : {latency} ms")
        print(f"PACKETS            : {packets}")
        print(f"PEAK VALUE         : {analysis['peak']}")
        print(f"MINIMUM VALUE      : {analysis['minimum']}")
        print(f"AVERAGE VALUE      : {analysis['average']}")
        print(f"STANDARD DEVIATION : {analysis['deviation']}")
        print()

        print("[SIGNAL GRAPH]")
        print()

        for sample in samples[:20]:
            print(f"{sample:>8} | {display_bar(sample)}")

        print("----------------------------------------------------")
        print()

        time.sleep(0.7)

        session_total += 1

    print("[SIGNAL SUMMARY]")
    print()

    print(f"TOTAL DEVICES ANALYZED : {session_total}")
    print(f"TOTAL CHANNELS ACTIVE  : {len(CHANNELS)}")
    print(f"TOTAL SIGNAL TYPES     : {len(SIGNAL_TYPES)}")
    print()

    print("[ENGINE STATUS]")
    print("RF MODULE             : ACTIVE")
    print("SIGNAL ANALYZER       : ACTIVE")
    print("CHANNEL MANAGER       : ACTIVE")
    print("FREQUENCY OBSERVER    : ACTIVE")
    print("NOISE FILTER          : ACTIVE")
    print("TELEMETRY ENGINE      : ACTIVE")
    print()

    print("[SIGNAL SESSION COMPLETE]")
    print()

if __name__ == "__main__":
    run()