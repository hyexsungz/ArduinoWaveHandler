# ArduinoWaveHandler Console Runtime
# This module powers the terminal interface for the ArduinoWaveHandler framework.
# Hope this helps and works alot.

# Hello everybody and fellow programmers. I'm Drautumnz under the alias of Hyexsungz.
# I put my time into making this awesome and large project, just to check and manage my ArduinoUnoR3.
# I've recently been struggling into keep checking stuff on does it work?
# So i programmed this so it detects Arduino chips doesnt matter if its a copy or replica.
# Before you proceed please add starts into my projects in order to grow. Thank you

import os
import time
import subprocess
import datetime
import shutil


class Console:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    def __init__(self):
        self.width = shutil.get_terminal_size((120, 30)).columns
        self.prev = {}
        self.curr = {}
        self.iteration = 0
        self.start = time.time()
        self.last_event = ""
        self.logs = []
        self.max_logs = 200
        self.stable = 0
        self.connected = 0
        self.disconnected = 0

        self.chips = {
            "VID_1A86": "CH340 / CH341 (WCH)",
            "VID_10C4": "CP210x (Silicon Labs)",
            "VID_0403": "FTDI FT232",
            "VID_067B": "Prolific PL2303"
        }

    def c(self, t, col):
        return f"{col}{t}{self.RESET}"

    def ts(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def uptime(self):
        return int(time.time() - self.start)

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def log(self, m):
        self.logs.append(f"{self.ts()} | {m}")
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)

    def scan(self):
        devices = {}

        try:
            out = subprocess.check_output(
                "wmic path Win32_PnPEntity get Name,DeviceID",
                shell=True
            ).decode(errors="ignore").splitlines()

            for line in out:
                line = line.strip()
                if not line:
                    continue

                vid = None
                chip = "UNKNOWN"

                for k, v in self.chips.items():
                    if k in line:
                        vid = k
                        chip = v

                if "COM" in line:
                    try:
                        port = "COM" + line.split("COM")[-1].split()[0]
                        name = line[:80]
                        devices[port] = {"name": name, "chip": chip, "vid": vid}
                    except:
                        pass

        except:
            pass

        return devices

    def diff(self):
        added = set(self.curr) - set(self.prev)
        removed = set(self.prev) - set(self.curr)

        for a in added:
            self.connected += 1
            self.last_event = f"CONNECTED {a} | {self.curr[a]['chip']}"
            self.log(f"CONNECT {a}")

        for r in removed:
            self.disconnected += 1
            self.last_event = f"DISCONNECTED {r}"
            self.log(f"DISCONNECT {r}")

        if not added and not removed:
            if self.curr:
                self.stable += 1
                self.last_event = "STABLE LINK"
            else:
                self.last_event = "NO DEVICES"
                self.stable = 0

    def render(self):
        self.clear()

        print(self.c("ArduinoWaveHandler LIVE DEVICE ENGINE", self.CYAN))
        print(self.c(f"TIME {self.ts()}", self.WHITE))
        print(self.c(f"UPTIME {self.uptime()}s", self.WHITE))
        print(self.c(f"SCAN {self.iteration}", self.BLUE))
        print(self.c(f"EVENT {self.last_event}", self.YELLOW))
        print(self.c(f"CONNECTED {self.connected} DISCONNECTED {self.disconnected}", self.GREEN))
        print("")

        print(self.c("DEVICES", self.CYAN))

        if not self.curr:
            print(self.c("NONE", self.RED))
        else:
            for p, i in self.curr.items():
                print(self.c(p, self.GREEN))
                print(self.c(i["name"], self.WHITE))
                print(self.c(i["chip"], self.YELLOW))
                print("")

        print(self.c("LOG", self.BLUE))
        for l in self.logs[-10:]:
            print(self.c(l, self.WHITE))

        print("")
        print(self.c("RUNNING LIVE SCAN", self.MAGENTA))

    def run(self):
        try:
            while True:
                self.iteration += 1
                self.prev = self.curr
                self.curr = self.scan()
                self.diff()
                self.render()
                time.sleep(1)
        except KeyboardInterrupt:
            self.clear()
            print(self.c("STOPPED", self.RED))


if __name__ == "__main__":
    Console().run()