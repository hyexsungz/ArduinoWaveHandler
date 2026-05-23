import time
import math
import statistics
import hashlib
import random

class WaveDetector:
    def __init__(self):
        self.samples = []
        self.detected = []
        self.noise = []
        self.history = []

        self.total_scans = 0
        self.total_detected = 0
        self.total_failed = 0

    def generate_signal(self, amplitude=1.0, frequency=1.0, size=64):
        signal = []

        for i in range(size):
            angle = 2 * math.pi * frequency * (i / size)
            value = amplitude * math.sin(angle)
            normalized = int((value + 1) * 127)
            signal.append(normalized)

        return signal

    def add_noise(self, signal, level=10):
        noisy = []

        for v in signal:
            delta = random.randint(-level, level)
            noisy.append(max(0, min(255, v + delta)))

        return noisy

    def analyze_signal(self, signal):
        if not signal:
            return {}

        return {
            "min": min(signal),
            "max": max(signal),
            "mean": statistics.mean(signal),
            "median": statistics.median(signal),
            "variance": statistics.pvariance(signal),
            "length": len(signal)
        }

    def similarity(self, a, b):
        if len(a) != len(b):
            return 0.0

        diff = 0

        for x, y in zip(a, b):
            diff += abs(x - y)

        max_diff = len(a) * 255

        return 1.0 - (diff / max_diff)

    def fingerprint(self, signal):
        return hashlib.sha256(bytes(signal)).hexdigest()

    def register(self, signal):
        entry = {
            "signal": signal,
            "fingerprint": self.fingerprint(signal),
            "analysis": self.analyze_signal(signal),
            "timestamp": int(time.time())
        }

        self.samples.append(entry)
        return entry

    def detect(self, signal, threshold=0.85):
        self.total_scans += 1

        best = None
        best_score = 0.0

        for entry in self.samples:
            score = self.similarity(signal, entry["signal"])

            if score > best_score:
                best_score = score
                best = entry

        if best and best_score >= threshold:
            result = {
                "detected": True,
                "score": best_score,
                "fingerprint": best["fingerprint"],
                "analysis": best["analysis"]
            }

            self.detected.append(result)
            self.total_detected += 1

            return result

        self.total_failed += 1

        return {
            "detected": False,
            "score": best_score
        }

    def benchmark(self, iterations=100):
        base = self.generate_signal()

        self.register(base)

        start = time.time()

        for _ in range(iterations):
            noisy = self.add_noise(base, level=5)
            self.detect(noisy)

        return {
            "iterations": iterations,
            "elapsed": time.time() - start
        }

    def clear(self):
        self.samples = []
        self.detected = []
        self.noise = []
        self.history = []

        self.total_scans = 0
        self.total_detected = 0
        self.total_failed = 0

    def status(self):
        return {
            "registered": len(self.samples),
            "detected": len(self.detected),
            "total_scans": self.total_scans,
            "total_detected": self.total_detected,
            "total_failed": self.total_failed
        }

    def pretty_print(self):
        print("============================================================")
        print("              ARDUINOWAVEHANDLER WAVE DETECTOR")
        print("============================================================")
        print("REGISTERED SIGNALS :", len(self.samples))
        print("DETECTED SIGNALS   :", len(self.detected))
        print("TOTAL SCANS        :", self.total_scans)
        print("FAILED DETECTIONS  :", self.total_failed)
        print("============================================================")

        if self.samples:
            print("")

            for i, s in enumerate(self.samples, start=1):
                print(f"[SIGNAL {i}]")
                print("FINGERPRINT :", s["fingerprint"][:32])
                print("MIN/MAX     :", s["analysis"]["min"], "/", s["analysis"]["max"])
                print("MEAN        :", round(s["analysis"]["mean"], 2))
                print("VARIANCE    :", round(s["analysis"]["variance"], 2))
                print("------------------------------------------------------------")


if __name__ == "__main__":
    wd = WaveDetector()

    base = wd.generate_signal(amplitude=1.5, frequency=2.0, size=128)
    wd.register(base)

    noisy = wd.add_noise(base, level=8)

    print(wd.detect(noisy))
    wd.pretty_print()