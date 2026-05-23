import time
import hashlib
import platform
import threading

try:
    import serial
    import serial.tools.list_ports
except:
    serial = None

class SerialScanner:
    def __init__(self):
        self.platform_name = platform.system()

        self.detected = []
        self.history = []

        self.running = False
        self.thread = None

        self.total_scans = 0
        self.total_detected = 0
        self.errors = 0

        self.keywords = [
            "arduino",
            "usb serial",
            "ch340",
            "cp210",
            "ftdi",
            "ttyusb",
            "ttyacm",
            "uno",
            "mega",
            "nano",
            "micro",
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

    def _is_serial_device(self, port):
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
        self.total_scans += 1
        self.detected = []

        if not serial:
            return []

        try:
            ports = serial.tools.list_ports.comports()

            for port in ports:
                if not self._is_serial_device(port):
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

                info = {
                    "device": device,
                    "description": description,
                    "manufacturer": manufacturer,
                    "product": product,
                    "hwid": hwid,
                    "fingerprint": fingerprint,
                    "timestamp": int(time.time())
                }

                self.detected.append(info)
                self.history.append(info)

                self.total_detected += 1

        except:
            self.errors += 1

        return self.detected

    def monitor_loop(self, delay=2):
        previous = set()

        while self.running:
            current_scan = self.scan()

            current = set(
                x["device"]
                for x in current_scan
            )

            added = current - previous
            removed = previous - current

            for dev in current_scan:
                if dev["device"] in added:
                    print("")
                    print("============================================================")
                    print("[+] SERIAL DEVICE DETECTED")
                    print("PORT          :", dev["device"])
                    print("DESCRIPTION   :", dev["description"])
                    print("MANUFACTURER  :", dev["manufacturer"])
                    print("PRODUCT       :", dev["product"])
                    print("HWID          :", dev["hwid"])
                    print("============================================================")
                    print("")

            for port in removed:
                print("")
                print("============================================================")
                print("[-] SERIAL DEVICE REMOVED")
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
            target=self.monitor_loop,
            daemon=True
        )

        self.thread.start()

    def stop(self):
        self.running = False

    def get_devices(self):
        return self.detected

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []

    def count(self):
        return len(self.detected)

    def summary(self):
        return {
            "platform": self.platform_name,
            "running": self.running,
            "detected": len(self.detected),
            "history_size": len(self.history),
            "total_scans": self.total_scans,
            "total_detected": self.total_detected,
            "errors": self.errors
        }

    def pretty_print(self):
        devices = self.scan()

        print("============================================================")
        print("              ARDUINOWAVEHANDLER SERIAL SCANNER")
        print("============================================================")

        if not devices:
            print("[INFO] No serial devices detected")
            print("============================================================")
            return

        for index, dev in enumerate(devices, start=1):
            print("")
            print(f"[SERIAL DEVICE {index}]")
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
    scanner = SerialScanner()

    scanner.pretty_print()