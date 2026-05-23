import time
import json
import threading
from pathlib import Path

from utils.logger import logger
from utils.file_utils import file_utils
from utils.parser import parser
from utils.string_utils import string_utils
from utils.time_utils import time_utils
from utils.console import Console

if __name__ == "__main__":
    Console().run()

class ArduinoWaveHandler:
    def __init__(self):
        self.root = Path.cwd()
        self.running = True
        self.start_time = time.time()
        self.config = {}
        self.devices = {}
        self.scan_count = 0
        self.lock = threading.Lock()

    def load_config(self):
        cfg_path = self.root / "config.json"
        if cfg_path.exists():
            with open(cfg_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
            logger.info("Config loaded")
        else:
            logger.warn("Config not found")

    def banner(self):
        if self.config.get("console", {}).get("show_ascii_banner", True):
            print("\n" + "=" * 60)
            print(" ArduinoWaveHandler LIVE DEVICE ENGINE")
            print("=" * 60 + "\n")

    def scan_loop(self):
        while self.running:
            try:
                self.scan_count += 1

                devices = console.scan_devices()

                with self.lock:
                    self.devices = devices

                logger.info(f"Scan #{self.scan_count} | Devices: {len(devices)}")

                time.sleep(self.config.get("runtime", {}).get("scan_interval_ms", 1000) / 1000)

            except Exception as e:
                logger.error(f"Scan error: {e}")

    def display_loop(self):
        while self.running:
            try:
                time.sleep(2)

                uptime = int(time.time() - self.start_time)

                print("\n" + "-" * 60)
                print("ArduinoWaveHandler LIVE DEVICE ENGINE")
                print(f"TIME {time.strftime('%H:%M:%S')}")
                print(f"UPTIME {uptime}s")
                print(f"SCAN {self.scan_count}")
                print("EVENT STABLE LINK")

                with self.lock:
                    connected = len(self.devices)

                print(f"CONNECTED {connected} DISCONNECTED 0")
                print("\nDEVICES")

                with self.lock:
                    for k, v in list(self.devices.items())[:10]:
                        print(k)
                        print(v)
                        print("UNKNOWN\n")

            except Exception as e:
                logger.error(f"Display error: {e}")

    def run(self):
        self.load_config()
        self.banner()

        t1 = threading.Thread(target=self.scan_loop, daemon=True)
        t2 = threading.Thread(target=self.display_loop, daemon=True)

        t1.start()
        t2.start()

        logger.success("System started")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            logger.warn("Shutting down...")


if __name__ == "__main__":
    app = ArduinoWaveHandler()
    app.run()