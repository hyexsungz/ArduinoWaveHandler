import serial.tools.list_ports
import time
import platform

class ProMiniBoard:
    def __init__(self):
        self.ports = []
        self.devices = []
        self.system = platform.system()
        self.arch = platform.machine()
        self.vendor_id = 0x2341
        self.board_name = "Arduino Pro Mini"
        self.chip = "ATmega328P"

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

    def is_pro_mini(self, p):
        try:
            desc = (p.description or "").lower()
            hwid = (p.hwid or "").lower()
            vid = getattr(p, "vid", None)
            pid = getattr(p, "pid", None)

            if vid == self.vendor_id:
                if "pro mini" in desc:
                    return True
                if "328p" in desc:
                    return True
                if "atmega328p" in desc:
                    return True

            if "pro mini" in desc:
                return True
            if "328p" in desc:
                return True

            if "2341" in hwid:
                if "pro" in desc or "328" in hwid:
                    return True

            if "usb serial" in desc and "arduino" in desc:
                return True

            if "ch340" in desc:
                return True
            if "1a86" in hwid:
                return True

        except:
            return False

        return False

    def classify(self, p):
        if self.is_pro_mini(p):
            return "ARDUINO_PRO_MINI"
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
                "type": self.classify(p),
                "chip": self.chip,
                "board": self.board_name
            })
        return self.devices

    def get_pro_mini_devices(self):
        return [d for d in self.scan() if d["type"] == "ARDUINO_PRO_MINI"]

    def detect(self):
        self.scan()
        return {
            "system": self.system,
            "arch": self.arch,
            "board": self.board_name,
            "chip": self.chip,
            "total_ports": len(self.ports),
            "pro_mini_devices": self.get_pro_mini_devices(),
            "all_devices": self.devices
        }

    def print_box(self):
        data = self.detect()
        print("╔══════════════════════════════════════════════════════════╗")
        print("║                ARDUINO PRO MINI SCANNER                ║")
        print("╠══════════════════════════════════════════════════════════╣")
        print(f"║ SYSTEM : {data['system']} {data['arch']}                  ║")
        print(f"║ BOARD : {data['board']}                                   ║")
        print(f"║ CHIP : {data['chip']}                                     ║")
        print(f"║ TOTAL PORTS : {data['total_ports']}                           ║")
        print(f"║ PRO MINI DEVICES : {len(data['pro_mini_devices'])}             ║")
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
    ProMiniBoard().run()