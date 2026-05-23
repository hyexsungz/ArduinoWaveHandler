import time
import threading
from pathlib import Path


class Monitor:
    def __init__(self, console, logger, interval=1.0):
        self.console = console
        self.logger = logger
        self.interval = interval

        self.running = False
        self.thread = None

        self.snapshot = {}
        self.last_snapshot = {}
        self.events = []

        self.start_time = time.time()
        self.scan_count = 0

    def _capture(self):
        try:
            return self.console.scan_devices()
        except Exception as e:
            self.logger.error(f"scan_failed {e}")
            return {}

    def _detect_changes(self, old, new):
        old_keys = set(old.keys())
        new_keys = set(new.keys())

        added = new_keys - old_keys
        removed = old_keys - new_keys

        for k in added:
            self.events.append(("CONNECT", k, time.time()))
            self.logger.info(f"CONNECT {k}")

        for k in removed:
            self.events.append(("DISCONNECT", k, time.time()))
            self.logger.warn(f"DISCONNECT {k}")

    def _loop(self):
        self.logger.success("monitor_started")

        while self.running:
            try:
                self.scan_count += 1

                new_snapshot = self._capture()

                self._detect_changes(self.snapshot, new_snapshot)

                self.last_snapshot = self.snapshot
                self.snapshot = new_snapshot

                time.sleep(self.interval)

            except Exception as e:
                self.logger.error(f"monitor_error {e}")

        self.logger.warn("monitor_stopped")

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    def get_events(self):
        return self.events

    def get_snapshot(self):
        return self.snapshot

    def uptime(self):
        return int(time.time() - self.start_time)

    def stats(self):
        return {
            "running": self.running,
            "scan_count": self.scan_count,
            "uptime": self.uptime(),
            "events": len(self.events)
        }