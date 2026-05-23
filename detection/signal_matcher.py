import time
import math
import hashlib
import statistics
import random

class SignalMatcher:
    def __init__(self):
        self.signals = []
        self.matches = []
        self.failed = []

        self.total_processed = 0
        self.total_matches = 0
        self.total_failed = 0

    def _fingerprint(self, signal):
        return hashlib.sha256(
            bytes(signal)
        ).hexdigest()

    def generate_wave(
        self,
        amplitude=1.0,
        frequency=1.0,
        samples=64
    ):
        signal = []

        for i in range(samples):
            angle = 2 * math.pi * frequency * (i / samples)

            value = amplitude * math.sin(angle)

            normalized = int((value + 1.0) * 127)

            signal.append(normalized)

        return signal

    def noise(
        self,
        signal,
        level=5
    ):
        noisy = []

        for value in signal:
            delta = random.randint(-level, level)

            noisy.append(
                max(0, min(255, value + delta))
            )

        return noisy

    def similarity(self, signal_a, signal_b):
        if len(signal_a) != len(signal_b):
            return 0.0

        total = 0

        for a, b in zip(signal_a, signal_b):
            total += abs(a - b)

        max_diff = len(signal_a) * 255

        score = 1.0 - (total / max_diff)

        return max(0.0, score)

    def analyze(self, signal):
        if not signal:
            return {}

        return {
            "min": min(signal),
            "max": max(signal),
            "average": statistics.mean(signal),
            "median": statistics.median(signal),
            "variance": statistics.pvariance(signal),
            "length": len(signal)
        }

    def register(self, name, signal):
        entry = {
            "name": name,
            "signal": signal,
            "fingerprint": self._fingerprint(signal),
            "analysis": self.analyze(signal),
            "timestamp": int(time.time())
        }

        self.signals.append(entry)

        return entry

    def match(self, signal, threshold=0.90):
        self.total_processed += 1

        best = None
        best_score = 0.0

        for entry in self.signals:
            score = self.similarity(
                signal,
                entry["signal"]
            )

            if score > best_score:
                best_score = score
                best = entry

        if best and best_score >= threshold:
            result = {
                "matched": True,
                "name": best["name"],
                "score": best_score,
                "fingerprint": best["fingerprint"],
                "analysis": best["analysis"]
            }

            self.matches.append(result)
            self.total_matches += 1

            return result

        result = {
            "matched": False,
            "score": best_score
        }

        self.failed.append(result)
        self.total_failed += 1

        return result

    def benchmark(self, iterations=100):
        start = time.time()

        base = self.generate_wave()

        self.register("base_wave", base)

        for _ in range(iterations):
            modified = self.noise(base)

            self.match(modified)

        elapsed = time.time() - start

        return {
            "iterations": iterations,
            "elapsed": elapsed,
            "per_second": iterations / elapsed if elapsed > 0 else 0
        }

    def clear(self):
        self.signals = []
        self.matches = []
        self.failed = []

        self.total_processed = 0
        self.total_matches = 0
        self.total_failed = 0

    def status(self):
        return {
            "registered_signals": len(self.signals),
            "matches": len(self.matches),
            "failed": len(self.failed),
            "total_processed": self.total_processed,
            "total_matches": self.total_matches,
            "total_failed": self.total_failed
        }

    def pretty_print(self):
        print("============================================================")
        print("              ARDUINOWAVEHANDLER SIGNAL MATCHER")
        print("============================================================")
        print("REGISTERED SIGNALS :", len(self.signals))
        print("MATCHES            :", len(self.matches))
        print("FAILED             :", len(self.failed))
        print("TOTAL PROCESSED    :", self.total_processed)
        print("============================================================")

        if self.signals:
            print("")

            for index, signal in enumerate(self.signals, start=1):
                print(f"[SIGNAL {index}]")
                print("NAME         :", signal["name"])
                print("FINGERPRINT  :", signal["fingerprint"][:32])
                print("LENGTH       :", signal["analysis"]["length"])
                print("AVERAGE      :", round(signal["analysis"]["average"], 2))
                print("VARIANCE     :", round(signal["analysis"]["variance"], 2))
                print("------------------------------------------------------------")


if __name__ == "__main__":
    matcher = SignalMatcher()

    base = matcher.generate_wave(
        amplitude=1.0,
        frequency=2.0,
        samples=128
    )

    matcher.register(
        "wave_alpha",
        base
    )

    noisy = matcher.noise(
        base,
        level=3
    )

    result = matcher.match(
        noisy,
        threshold=0.85
    )

    print(result)

    matcher.pretty_print()