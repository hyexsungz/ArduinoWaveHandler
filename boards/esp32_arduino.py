import serial.tools.list_ports
import time
import platform
import json

class ESP32Arduino:
    def __init__(self):
        self.ports = []
        self.devices = []
        self.system = platform.system()
        self.arch = platform.machine()
        self.vendor_ids = [0x10C4, 0x1A86, 0x0403, 0x2341, 0x303A]
        self.chips = {
            "cp210x": 0x10C4,
            "ch340": 0x1A86,
            "ftdi": 0x0403,
            "arduino": 0x2341,
            "espressif": 0x303A
        }

    def scan_ports(self):
        self.ports = list(serial.tools.list_ports.comports())
        return self.ports

    def get_signature(self, p):
        try:
            return {
                "port": p.device,
                "description": p.description,
                "hwid": p.hwid,
                "vid": getattr(p, "vid", None),
                "pid": getattr(p, "pid", None)
            }
        except:
            return {
                "port": None,
                "description": None,
                "hwid": None,
                "vid": None,
                "pid": None
            }

    def is_esp32(self, p):
        try:
            desc = (p.description or "").lower()
            hwid = (p.hwid or "").lower()
            vid = getattr(p, "vid", None)
            pid = getattr(p, "pid", None)

            if vid == self.chips["espressif"]:
                return True

            if "esp32" in desc:
                return True
            if "espressif" in desc:
                return True
            if "cp210" in desc and "usb" in desc:
                return True
            if "wch" in desc and "usb" in desc:
                return True
            if "1a86" in hwid:
                return True

            if "ttyusb" in desc:
                if "esp" in desc:
                    return True

        except:
            return False

        return False

    def is_arduino(self, p):
        try:
            desc = (p.description or "").lower()
            hwid = (p.hwid or "").lower()

            if "arduino" in desc:
                return True
            if "uno" in desc:
                return True
            if "nano" in desc:
                return True
            if "mega" in desc:
                return True
            if "due" in desc:
                return True
            if "2341" in hwid:
                return True

        except:
            return False

        return False

    def classify(self, p):
        if self.is_esp32(p):
            return "ESP32_DEVICE"
        if self.is_arduino(p):
            return "ARDUINO_DEVICE"
        return "UNKNOWN"

    def scan(self):
        self.devices = []
        for p in self.scan_ports():
            self.devices.append({
                "port": p.device,
                "description": p.description,
                "hwid": p.hwid,
                "vid": getattr(p, "vid", None),
                "pid": getattr(p, "pid", None),
                "type": self.classify(p)
            })
        return self.devices

    def get_esp32_devices(self):
        return [d for d in self.scan() if d["type"] == "ESP32_DEVICE"]

    def get_arduino_devices(self):
        return [d for d in self.scan() if d["type"] == "ARDUINO_DEVICE"]

    def detect(self):
        self.scan()
        return {
            "system": self.system,
            "arch": self.arch,
            "total_ports": len(self.ports),
            "esp32_devices": self.get_esp32_devices(),
            "arduino_devices": self.get_arduino_devices(),
            "all_devices": self.devices
        }

    def live(self, interval=2):
        last = set()
        while True:
            self.scan_ports()
            current = set(p.device for p in self.ports)

            added = current - last
            removed = last - current

            if added or removed:
                print("DEVICE CHANGE DETECTED")
                for a in added:
                    print("CONNECTED:", a)
                for r in removed:
                    print("DISCONNECTED:", r)

            last = current
            time.sleep(interval)

    def print_box(self):
        data = self.detect()
        print("╔══════════════════════════════════════════════════════════╗")
        print("║                    ESP32 / ARDUINO MONITOR              ║")
        print("╠══════════════════════════════════════════════════════════╣")
        print(f"║ SYSTEM : {data['system']} {data['arch']}                  ║")
        print(f"║ TOTAL PORTS : {data['total_ports']}                           ║")
        print(f"║ ESP32 DEVICES : {len(data['esp32_devices'])}                    ║")
        print(f"║ ARDUINO DEVICES : {len(data['arduino_devices'])}               ║")
        print("╚══════════════════════════════════════════════════════════╝")

    def run(self):
        self.print_box()
        self.live()


if __name__ == "__main__":
    ESP32Arduino().run()