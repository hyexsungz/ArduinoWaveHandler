import time
import hashlib
import platform

try:
    import serial
    import serial.tools.list_ports
except:
    serial = None

class DeviceVerifier:
    def __init__(self):
        self.verified = []
        self.failed = []
        self.history = []

        self.total_scans = 0
        self.total_verified = 0
        self.total_failed = 0

        self.allowed_keywords = [
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

    def _hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def _normalize(self, text):
        return str(text).lower().strip()

    def _valid(self, port):
        combined = " ".join([
            str(port.device),
            str(port.description),
            str(port.hwid),
            str(getattr(port, "manufacturer", "")),
            str(getattr(port, "product", ""))
        ]).lower()

        for keyword in self.allowed_keywords:
            if keyword in combined:
                return True

        return False

    def scan(self):
        self.total_scans += 1

        self.verified = []
        self.failed = []

        if not serial:
            return []

        try:
            ports = serial.tools.list_ports.comports()

            for port in ports:
                device = str(port.device)
                description = str(port.description)
                hwid = str(port.hwid)
                manufacturer = str(getattr(port, "manufacturer", ""))
                product = str(getattr(port, "product", ""))

                verified = self._valid(port)

                fingerprint = self._hash(
                    device +
                    description +
                    hwid +
                    manufacturer +
                    product
                )

                info = {
                    "device": device,
                    "description": description,
                    "hwid": hwid,
                    "manufacturer": manufacturer,
                    "product": product,
                    "fingerprint": fingerprint,
                    "verified": verified,
                    "timestamp": int(time.time())
                }

                self.history.append(info)

                if verified:
                    self.verified.append(info)
                    self.total_verified += 1
                else:
                    self.failed.append(info)
                    self.total_failed += 1

        except:
            pass

        return self.verified

    def verify_port(self, port_name):
        devices = self.scan()

        for device in devices:
            if device["device"] == port_name:
                return True

        return False

    def verify_all(self):
        return self.scan()

    def count_verified(self):
        return len(self.verified)

    def count_failed(self):
        return len(self.failed)

    def get_verified(self):
        return self.verified

    def get_failed(self):
        return self.failed

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []

    def monitor(self, delay=2):
        last_verified = set()

        while True:
            devices = self.scan()

            current = set(
                x["device"]
                for x in devices
            )

            added = current - last_verified
            removed = last_verified - current

            for dev in added:
                print("[+] VERIFIED DEVICE:", dev)

            for dev in removed:
                print("[-] REMOVED DEVICE:", dev)

            last_verified = current

            time.sleep(delay)

    def summary(self):
        return {
            "platform": platform.system(),
            "verified": len(self.verified),
            "failed": len(self.failed),
            "history": len(self.history),
            "total_scans": self.total_scans,
            "total_verified": self.total_verified,
            "total_failed": self.total_failed
        }

    def pretty_print(self):
        verified = self.scan()

        print("============================================================")
        print("              ARDUINOWAVEHANDLER DEVICE VERIFY")
        print("============================================================")

        if not verified:
            print("[INFO] No verified devices detected")
            print("============================================================")
            return

        for index, device in enumerate(verified, start=1):
            print("")
            print(f"[VERIFIED DEVICE {index}]")
            print("PORT          :", device["device"])
            print("DESCRIPTION   :", device["description"])
            print("MANUFACTURER  :", device["manufacturer"])
            print("PRODUCT       :", device["product"])
            print("HWID          :", device["hwid"])
            print("FINGERPRINT   :", device["fingerprint"][:32])

        print("")
        print("============================================================")
        print("TOTAL VERIFIED:", len(verified))
        print("============================================================")


if __name__ == "__main__":
    verifier = DeviceVerifier()
    verifier.pretty_print()