import time
import threading
import hashlib
import platform

try:
    import serial
    import serial.tools.list_ports
except:
    serial = None

class DeviceWatcher:
    def __init__(self):
        self.running = False
        self.thread = None

        self.connected = {}
        self.history = []

        self.detected_count = 0
        self.removed_count = 0
        self.errors = 0
        self.scans = 0

        self.keywords = [
            "arduino",
            "usb serial",
            "ch340",
            "cp210",
            "ftdi",
            "ttyusb",
            "ttyacm",
            "uno",
            "nano",
            "mega",
            "leonardo",
            "esp32",
            "esp8266",
            "stm32",
            "teensy"
        ]

    def _normalize(self, text):
        return str(text).lower()

    def _fingerprint(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def _valid(self, port):
        combined = " ".join([
            str(port.device),
            str(port.description),
            str(port.hwid),
            str(getattr(port, "manufacturer", "")),
            str(getattr(port, "product", ""))
        ]).lower()

        for keyword in self.keywords:
            if keyword in combined:
                return True

        return False

    def scan(self):
        self.scans += 1

        devices = {}

        if not serial:
            return devices

        try:
            ports = serial.tools.list_ports.comports()

            for port in ports:
                if not self._valid(port):
                    continue

                device = str(port.device)
                description = str(port.description)
                hwid = str(port.hwid)
                manufacturer = str(getattr(port, "manufacturer", ""))
                product = str(getattr(port, "product", ""))

                fingerprint = self._fingerprint(
                    device +
                    description +
                    hwid
                )

                devices[device] = {
                    "device": device,
                    "description": description,
                    "hwid": hwid,
                    "manufacturer": manufacturer,
                    "product": product,
                    "fingerprint": fingerprint,
                    "timestamp": int(time.time())
                }

        except:
            self.errors += 1

        return devices

    def watch_loop(self, delay=1):
        previous = {}

        while self.running:
            current = self.scan()

            current_keys = set(current.keys())
            previous_keys = set(previous.keys())

            added = current_keys - previous_keys
            removed = previous_keys - current_keys

            for port in added:
                info = current[port]

                self.connected[port] = info
                self.history.append({
                    "event": "connected",
                    "device": port,
                    "timestamp": int(time.time())
                })

                self.detected_count += 1

                print("")
                print("============================================================")
                print("[+] DEVICE CONNECTED")
                print("PORT         :", info["device"])
                print("DESCRIPTION  :", info["description"])
                print("MANUFACTURER :", info["manufacturer"])
                print("PRODUCT      :", info["product"])
                print("============================================================")
                print("")

            for port in removed:
                if port in self.connected:
                    del self.connected[port]

                self.history.append({
                    "event": "removed",
                    "device": port,
                    "timestamp": int(time.time())
                })

                self.removed_count += 1

                print("")
                print("============================================================")
                print("[-] DEVICE REMOVED")
                print("PORT :", port)
                print("============================================================")
                print("")

            previous = current

            time.sleep(delay)

    def start(self):
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.watch_loop,
            daemon=True
        )

        self.thread.start()

    def stop(self):
        self.running = False

    def active_devices(self):
        return list(self.connected.values())

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []

    def status(self):
        return {
            "platform": platform.system(),
            "running": self.running,
            "active_devices": len(self.connected),
            "detected_count": self.detected_count,
            "removed_count": self.removed_count,
            "errors": self.errors,
            "scans": self.scans
        }

    def pretty_print(self):
        print("============================================================")
        print("               ARDUINOWAVEHANDLER WATCHER")
        print("============================================================")
        print("RUNNING        :", self.running)
        print("ACTIVE DEVICES :", len(self.connected))
        print("DETECTED       :", self.detected_count)
        print("REMOVED        :", self.removed_count)
        print("ERRORS         :", self.errors)
        print("SCANS          :", self.scans)
        print("============================================================")

        if self.connected:
            print("")

            for device in self.connected.values():
                print("PORT         :", device["device"])
                print("DESCRIPTION  :", device["description"])
                print("MANUFACTURER :", device["manufacturer"])
                print("PRODUCT      :", device["product"])
                print("------------------------------------------------------------")


if __name__ == "__main__":
    watcher = DeviceWatcher()

    watcher.start()

    try:
        while True:
            time.sleep(5)
            watcher.pretty_print()

    except KeyboardInterrupt:
        watcher.stop()
        print("")
        print("[INFO] Watcher stopped")