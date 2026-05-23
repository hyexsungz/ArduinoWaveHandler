import time
import threading
import hashlib
import platform

try:
    import serial
    import serial.tools.list_ports
except:
    serial = None

class USBScanner:
    def __init__(self):
        self.system = platform.system()

        self.running = False
        self.thread = None

        self.devices = []
        self.history = []

        self.total_scans = 0
        self.total_detected = 0
        self.total_removed = 0
        self.errors = 0

        self.filters = [
            "usb",
            "serial",
            "arduino",
            "ch340",
            "cp210",
            "ftdi",
            "ttyusb",
            "ttyacm",
            "silicon labs",
            "wch",
            "esp32",
            "esp8266",
            "stm32",
            "teensy",
            "mega",
            "uno",
            "nano",
            "micro",
            "leonardo"
        ]

    def _normalize(self, text):
        return str(text).lower()

    def _fingerprint(self, text):
        return hashlib.sha256(
            text.encode()
        ).hexdigest()

    def _match(self, port):
        combined = " ".join([
            str(port.device),
            str(port.description),
            str(port.hwid),
            str(getattr(port, "manufacturer", "")),
            str(getattr(port, "product", ""))
        ]).lower()

        for keyword in self.filters:
            if keyword in combined:
                return True

        return False

    def scan(self):
        self.total_scans += 1

        current = []

        if not serial:
            return current

        try:
            ports = serial.tools.list_ports.comports()

            for port in ports:
                if not self._match(port):
                    continue

                device = str(port.device)
                description = str(port.description)
                manufacturer = str(getattr(port, "manufacturer", ""))
                product = str(getattr(port, "product", ""))
                hwid = str(port.hwid)

                fingerprint = self._fingerprint(
                    device +
                    description +
                    hwid
                )

                info = {
                    "device": device,
                    "description": description,
                    "manufacturer": manufacturer,
                    "product": product,
                    "hwid": hwid,
                    "fingerprint": fingerprint,
                    "timestamp": int(time.time())
                }

                current.append(info)

        except:
            self.errors += 1

        self.devices = current

        return current

    def watch_loop(self, delay=2):
        previous = {}

        while self.running:
            current_scan = self.scan()

            current = {
                x["device"]: x
                for x in current_scan
            }

            current_keys = set(current.keys())
            previous_keys = set(previous.keys())

            added = current_keys - previous_keys
            removed = previous_keys - current_keys

            for port in added:
                info = current[port]

                self.total_detected += 1

                self.history.append({
                    "event": "connected",
                    "device": port,
                    "timestamp": int(time.time())
                })

                print("")
                print("============================================================")
                print("[+] USB DEVICE CONNECTED")
                print("PORT          :", info["device"])
                print("DESCRIPTION   :", info["description"])
                print("MANUFACTURER  :", info["manufacturer"])
                print("PRODUCT       :", info["product"])
                print("HWID          :", info["hwid"])
                print("============================================================")
                print("")

            for port in removed:
                self.total_removed += 1

                self.history.append({
                    "event": "removed",
                    "device": port,
                    "timestamp": int(time.time())
                })

                print("")
                print("============================================================")
                print("[-] USB DEVICE REMOVED")
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

    def get_devices(self):
        return self.devices

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []

    def count(self):
        return len(self.devices)

    def summary(self):
        return {
            "platform": self.system,
            "running": self.running,
            "devices": len(self.devices),
            "history": len(self.history),
            "total_scans": self.total_scans,
            "detected": self.total_detected,
            "removed": self.total_removed,
            "errors": self.errors
        }

    def pretty_print(self):
        devices = self.scan()

        print("============================================================")
        print("                ARDUINOWAVEHANDLER USB SCANNER")
        print("============================================================")

        if not devices:
            print("[INFO] No USB serial devices detected")
            print("============================================================")
            return

        for index, dev in enumerate(devices, start=1):
            print("")
            print(f"[USB DEVICE {index}]")
            print("PORT          :", dev["device"])
            print("DESCRIPTION   :", dev["description"])
            print("MANUFACTURER  :", dev["manufacturer"])
            print("PRODUCT       :", dev["product"])
            print("HWID          :", dev["hwid"])
            print("FINGERPRINT   :", dev["fingerprint"][:32])

        print("")
        print("============================================================")
        print("TOTAL DEVICES :", len(devices))
        print("============================================================")


if __name__ == "__main__":
    scanner = USBScanner()

    scanner.pretty_print()