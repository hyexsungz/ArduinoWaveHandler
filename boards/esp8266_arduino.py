import serial.tools.list_ports
import time
import platform

class Arduino8266Arduino:
    def __init__(self):
        self.ports = []
        self.devices = []
        self.system = platform.system()
        self.arch = platform.machine()

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

    def is_esp8266(self, p):
        try:
            desc = (p.description or "").lower()
            hwid = (p.hwid or "").lower()

            if "esp8266" in desc:
                return True
            if "nodemcu" in desc:
                return True
            if "wemos" in desc:
                return True
            if "cp210" in desc:
                return True
            if "ch340" in desc:
                return True
            if "1a86" in hwid:
                return True
            if "10c4" in hwid:
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
            if "2341" in hwid:
                return True
        except:
            return False
        return False

    def classify(self, p):
        if self.is_esp8266(p):
            return "ESP8266_DEVICE"
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

    def get_esp8266_devices(self):
        return [d for d in self.scan() if d["type"] == "ESP8266_DEVICE"]

    def get_arduino_devices(self):
        return [d for d in self.scan() if d["type"] == "ARDUINO_DEVICE"]

    def detect(self):
        self.scan()
        return {
            "system": self.system,
            "arch": self.arch,
            "total_ports": len(self.ports),
            "esp8266_devices": self.get_esp8266_devices(),
            "arduino_devices": self.get_arduino_devices(),
            "all_devices": self.devices
        }

    def print_box(self):
        data = self.detect()
        print("╔══════════════════════════════════════════════════════════╗")
        print("║             ESP8266 / ARDUINO DETECTOR                  ║")
        print("╠══════════════════════════════════════════════════════════╣")
        print(f"║ SYSTEM : {data['system']} {data['arch']}                  ║")
        print(f"║ TOTAL PORTS : {data['total_ports']}                           ║")
        print(f"║ ESP8266 DEVICES : {len(data['esp8266_devices'])}                 ║")
        print(f"║ ARDUINO DEVICES : {len(data['arduino_devices'])}                ║")
        print("╚══════════════════════════════════════════════════════════╝")

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

    def run(self):
        self.print_box()
        self.live()


if __name__ == "__main__":
    Arduino8266Arduino().run()