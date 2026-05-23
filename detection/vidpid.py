import time
import hashlib
import platform

try:
    import serial.tools.list_ports
except:
    serial = None


class VIDPIDScanner:
    def __init__(self):
        self.system = platform.system()

        self.devices = []
        self.history = []

        self.total_scans = 0
        self.total_matched = 0
        self.errors = 0

        self.known_vendors = {
            "1a86": "CH340 / WCH",
            "10c4": "Silicon Labs (CP210x)",
            "0403": "FTDI",
            "2341": "Arduino LLC",
            "2a03": "Arduino SA",
            "303a": "Espressif (ESP32/ESP8266)",
            "0483": "STMicroelectronics (STM32)",
            "16c0": "Teensy / PJRC"
        }

    def _normalize(self, text):
        return str(text).lower()

    def _fingerprint(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def _extract_vid_pid(self, hwid):
        hwid = hwid.lower()

        vid = None
        pid = None

        if "vid:" in hwid:
            try:
                vid = hwid.split("vid:")[1].split()[0].replace("0x", "").strip()
            except:
                pass

        if "pid:" in hwid:
            try:
                pid = hwid.split("pid:")[1].split()[0].replace("0x", "").strip()
            except:
                pass

        return vid, pid

    def identify(self, vid, pid):
        if not vid:
            return "Unknown Vendor"

        return self.known_vendors.get(vid, "Unknown Vendor")

    def scan(self):
        self.total_scans += 1
        self.devices = []

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

                vid, pid = self._extract_vid_pid(hwid)
                vendor = self.identify(vid, pid)

                fingerprint = self._fingerprint(
                    device +
                    description +
                    hwid
                )

                info = {
                    "device": device,
                    "description": description,
                    "hwid": hwid,
                    "manufacturer": manufacturer,
                    "product": product,
                    "vid": vid,
                    "pid": pid,
                    "vendor": vendor,
                    "fingerprint": fingerprint,
                    "timestamp": int(time.time())
                }

                self.devices.append(info)
                self.history.append(info)

                self.total_matched += 1

        except:
            self.errors += 1

        return self.devices

    def get_devices(self):
        return self.devices

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []

    def monitor(self, delay=2):
        previous = set()

        while True:
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
                    print("[+] VID/PID DEVICE DETECTED")
                    print("PORT          :", dev["device"])
                    print("VENDOR        :", dev["vendor"])
                    print("VID           :", dev["vid"])
                    print("PID           :", dev["pid"])
                    print("DESCRIPTION   :", dev["description"])
                    print("MANUFACTURER  :", dev["manufacturer"])
                    print("============================================================")
                    print("")

            for port in removed:
                print("")
                print("============================================================")
                print("[-] DEVICE REMOVED")
                print("PORT :", port)
                print("============================================================")
                print("")

            previous = current

            time.sleep(delay)

    def summary(self):
        return {
            "platform": self.system,
            "total_scans": self.total_scans,
            "matched": self.total_matched,
            "active_devices": len(self.devices),
            "history_size": len(self.history),
            "errors": self.errors
        }

    def pretty_print(self):
        devices = self.scan()

        print("============================================================")
        print("              ARDUINOWAVEHANDLER VID/PID SCANNER")
        print("============================================================")

        if not devices:
            print("[INFO] No VID/PID devices detected")
            print("============================================================")
            return

        for index, dev in enumerate(devices, start=1):
            print("")
            print(f"[DEVICE {index}]")
            print("PORT          :", dev["device"])
            print("VENDOR        :", dev["vendor"])
            print("VID           :", dev["vid"])
            print("PID           :", dev["pid"])
            print("DESCRIPTION   :", dev["description"])
            print("MANUFACTURER  :", dev["manufacturer"])
            print("HWID          :", dev["hwid"])
            print("FINGERPRINT   :", dev["fingerprint"][:32])

        print("")
        print("============================================================")
        print("TOTAL DEVICES :", len(devices))
        print("============================================================")


if __name__ == "__main__":
    scanner = VIDPIDScanner()
    scanner.pretty_print()