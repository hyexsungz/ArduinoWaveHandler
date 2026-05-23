import time
import platform

try:
    import serial
    import serial.tools.list_ports
except:
    serial = None

class ArduinoScanner:
    def __init__(self):
        self.system = platform.system()
        self.detected = []
        self.history = []
        self.scans = 0

        self.keywords = [
            "arduino",
            "ch340",
            "cp210",
            "usb serial",
            "wch",
            "silicon labs",
            "ttyusb",
            "ttyacm",
            "ftdi",
            "mega",
            "uno",
            "nano",
            "leonardo",
            "stm32",
            "teensy",
            "esp32",
            "esp8266"
        ]

    def _normalize(self, text):
        return str(text).lower()

    def scan(self):
        self.detected = []
        self.scans += 1

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
                ]).lower()

                matched = False

                for keyword in self.keywords:
                    if keyword in combined:
                        matched = True
                        break

                if matched:
                    info = {
                        "device": device,
                        "description": description,
                        "hwid": hwid,
                        "manufacturer": manufacturer,
                        "product": product,
                        "timestamp": int(time.time())
                    }

                    self.detected.append(info)
                    self.history.append(info)

        except:
            pass

        return self.detected

    def monitor(self, delay=1):
        last = set()

        while True:
            current_scan = self.scan()

            current = set(
                x["device"]
                for x in current_scan
            )

            added = current - last
            removed = last - current

            if added:
                for dev in added:
                    print("[+] CONNECTED:", dev)

            if removed:
                for dev in removed:
                    print("[-] DISCONNECTED:", dev)

            last = current

            time.sleep(delay)

    def get_devices(self):
        return self.detected

    def get_history(self):
        return self.history

    def count(self):
        return len(self.detected)

    def clear_history(self):
        self.history = []

    def summary(self):
        return {
            "system": self.system,
            "detected": len(self.detected),
            "history": len(self.history),
            "scans": self.scans
        }

    def pretty_print(self):
        devices = self.scan()

        print("============================================================")
        print("                 ARDUINOWAVEHANDLER SCANNER")
        print("============================================================")

        if not devices:
            print("[INFO] No Arduino compatible devices found")
            return

        for index, device in enumerate(devices, start=1):
            print("")
            print(f"[DEVICE {index}]")
            print("PORT          :", device["device"])
            print("DESCRIPTION   :", device["description"])
            print("MANUFACTURER  :", device["manufacturer"])
            print("PRODUCT       :", device["product"])
            print("HWID          :", device["hwid"])

        print("")
        print("============================================================")
        print("TOTAL DEVICES :", len(devices))
        print("============================================================")


if __name__ == "__main__":
    scanner = ArduinoScanner()
    scanner.pretty_print()