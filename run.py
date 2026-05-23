import os
import sys
import time
import json
import signal
import threading
from pathlib import Path

from utils.logger import logger
from utils.console import console
from utils.file_utils import file_utils
from utils.parser import parser
from utils.string_utils import string_utils
from utils.time_utils import time_utils
from monitor import Monitor


class Runtime:
    def __init__(self):
        self.root = Path.cwd()
        self.running = True
        self.started = time.time()

        self.monitor = None
        self.config = {}

        self.runtime_stats = {
            "loops": 0,
            "errors": 0,
            "events": 0
        }

    def load_config(self):
        try:
            cfg = self.root / "config.json"

            if cfg.exists():
                with open(cfg, "r", encoding="utf-8") as f:
                    self.config = json.load(f)

                logger.success("config_loaded")
            else:
                logger.warn("config_missing")

        except Exception as e:
            logger.error(f"config_error {e}")
            self.runtime_stats["errors"] += 1

    def banner(self):
        print("\n")
        print("=" * 70)
        print(" ArduinoWaveHandler Runtime Environment ")
        print("=" * 70)
        print(f"TIME     {time.strftime('%H:%M:%S')}")
        print(f"PROJECT  ArduinoWaveHandler")
        print(f"MODE     {self.config.get('mode', 'development')}")
        print("=" * 70)
        print("\n")

    def initialize(self):
        logger.info("runtime_initialize")

        self.load_config()

        self.monitor = Monitor(
            console=console,
            logger=logger,
            interval=self.config.get("runtime", {}).get("scan_interval_ms", 1000) / 1000
        )

        logger.success("runtime_initialized")

    def stats_loop(self):
        while self.running:
            try:
                uptime = int(time.time() - self.started)

                stats = self.monitor.stats()

                print("\n")
                print("-" * 70)
                print("RUNTIME STATUS")
                print("-" * 70)
                print(f"UPTIME       {uptime}s")
                print(f"SCANS        {stats['scan_count']}")
                print(f"EVENTS       {stats['events']}")
                print(f"RUNNING      {stats['running']}")
                print(f"ERRORS       {self.runtime_stats['errors']}")
                print("-" * 70)

                time.sleep(5)

            except Exception as e:
                logger.error(f"stats_loop_error {e}")
                self.runtime_stats["errors"] += 1

    def event_loop(self):
        while self.running:
            try:
                self.runtime_stats["loops"] += 1

                events = self.monitor.get_events()

                if events:
                    last = events[-1]
                    self.runtime_stats["events"] = len(events)

                    event_type = last[0]
                    event_name = last[1]

                    logger.debug(f"event {event_type} {event_name}")

                time.sleep(1)

            except Exception as e:
                logger.error(f"event_loop_error {e}")
                self.runtime_stats["errors"] += 1

    def shutdown(self):
        logger.warn("runtime_shutdown")

        self.running = False

        if self.monitor:
            self.monitor.stop()

        logger.success("runtime_stopped")

    def signal_handler(self, sig, frame):
        self.shutdown()
        sys.exit(0)

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        self.initialize()

        self.banner()

        self.monitor.start()

        threading.Thread(target=self.stats_loop, daemon=True).start()
        threading.Thread(target=self.event_loop, daemon=True).start()

        logger.success("runtime_started")

        try:
            while self.running:
                time.sleep(1)

        except KeyboardInterrupt:
            self.shutdown()


if __name__ == "__main__":
    Runtime().run()