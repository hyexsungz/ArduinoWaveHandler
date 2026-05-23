import time
import hashlib
import platform

try:
    import serial
    import serial.tools.list_ports
except:
    serial = None

class PortIdentifier:
    def __init__(self):
        self.system = platform.system()

        self.detected_ports = []
        self.history = []

        self.total_scans = 0
        self.total_identified = 0
        self.errors = 0

        self.board_map = {
            "uno": "Arduino Uno",
            "mega": "Arduino Mega",
            "nano": "Arduino Nano",
            "leonardo": "Arduino Leonardo",
            "micro": "Arduino Micro",
            "pro mini": "Arduino Pro Mini",
            "esp32": "ESP32",
            "esp8266": "ESP8266",
            "stm32": "STM32",
            "teensy": "Teensy",
            "ch340": "CH340 USB Serial",
            "cp210": "CP210x USB Serial",
            "ftdi": "FTDI USB Serial"
        }

    def _normalize(self, text):
        return str(text).lower()

    def _fingerprint(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def identify_board(self, text):
        lower = self._normalize(text)

        for keyword, board in self.board_map.items():
            if keyword in lower:
                return board

        return "Unknown Device"

    def scan(self):
        self.detected_ports = []
        self.total_scans += 1

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

                combined = " ".join([
                    device,
                    description,
                    hwid,
                    manufacturer,
                    product
                ])

                identified = self.identify_board(combined)

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
                    "identified_as": identified,
                    "fingerprint": fingerprint,
                    "timestamp": int(time.time())
                }

                self.detected_ports.append(info)
                self.history.append(info)

                self.total_identified += 1

        except:
            self.errors += 1

        return self.detected_ports

    def get_ports(self):
        return self.detected_ports

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []

    def monitor(self, delay=2):
        last = set()

        while True:
            devices = self.scan()

            current = set(
                x["device"]
                for x in devices
            )

            added = current - last
            removed = last - current

            for dev in devices:
                if dev["device"] in added:
                    print("")
                    print("============================================================")
                    print("[+] DEVICE IDENTIFIED")
                    print("PORT          :", dev["device"])
                    print("BOARD         :", dev["identified_as"])
                    print("DESCRIPTION   :", dev["description"])
                    print("MANUFACTURER  :", dev["manufacturer"])
                    print("PRODUCT       :", dev["product"])
                    print("============================================================")
                    print("")

            for port in removed:
                print("")
                print("============================================================")
                print("[-] DEVICE REMOVED")
                print("PORT :", port)
                print("============================================================")
                print("")

            last = current

            time.sleep(delay)

    def summary(self):
        return {
            "platform": self.system,
            "total_scans": self.total_scans,
            "identified": self.total_identified,
            "active_ports": len(self.detected_ports),
            "history_size": len(self.history),
            "errors": self.errors
        }

    def pretty_print(self):
        devices = self.scan()

        print("============================================================")
        print("             ARDUINOWAVEHANDLER PORT IDENTIFIER")
        print("============================================================")

        if not devices:
            print("[INFO] No compatible devices detected")
            print("============================================================")
            return

        for index, dev in enumerate(devices, start=1):
            print("")
            print(f"[DEVICE {index}]")
            print("PORT          :", dev["device"])
            print("BOARD         :", dev["identified_as"])
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
    identifier = PortIdentifier()

    identifier.pretty_print()