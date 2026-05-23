import time
import threading
import os
from datetime import datetime


class Logger:
    def __init__(self, file_path="logs/runtime.log"):
        self.file_path = file_path
        self.lock = threading.Lock()
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def _write(self, level, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"{ts} | {level} | {msg}"

        with self.lock:
            print(line)
            try:
                with open(self.file_path, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
            except:
                pass

    def info(self, msg):
        self._write("INFO", msg)

    def warn(self, msg):
        self._write("WARN", msg)

    def error(self, msg):
        self._write("ERROR", msg)

    def debug(self, msg):
        self._write("DEBUG", msg)

    def success(self, msg):
        self._write("SUCCESS", msg)


logger = Logger()