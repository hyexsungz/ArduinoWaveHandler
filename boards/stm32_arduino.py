import serial.tools.list_ports
import time
import platform

class STM32Arduino:
    def __init__(self):
        self.ports = []
        self.devices = []
        self.system = platform.system()
        self.arch = platform.machine()
        self.board_name = "STM32 Arduino"
        self.chips = ["stm32", "bluepill", "blackpill", "maple", "dfu"]
        self.usb_vids = [0x0483, 0x1EAF, 0x1209]

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

    def is_stm32(self, p):
        try:
            desc = (p.description or "").lower()
            hwid = (p.hwid or "").lower()
            vid = getattr(p, "vid", None)
            pid = getattr(p, "pid", None)

            if any(k in desc for k in self.chips):
                return True

            if vid in self.usb_vids:
                return True

            if "stm32" in hwid:
                return True

            if "0483" in hwid:
                return True

            if "dfu" in desc:
                return True

            if "maple" in desc:
                return True

        except:
            return False

        return False

    def classify(self, p):
        if self.is_stm32(p):
            return "STM32_DEVICE"
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
                "board": self.board_name
            })
        return self.devices

    def get_stm32_devices(self):
        return [d for d in self.scan() if d["type"] == "STM32_DEVICE"]

    def detect(self):
        self.scan()
        return {
            "system": self.system,
            "arch": self.arch,
            "board": self.board_name,
            "total_ports": len(self.ports),
            "stm32_devices": self.get_stm32_devices(),
            "all_devices": self.devices
        }

    def print_box(self):
        data = self.detect()
        print("╔══════════════════════════════════════════════════════════╗")
        print("║                 STM32 ARDUINO SCANNER                  ║")
        print("╠══════════════════════════════════════════════════════════╣")
        print(f"║ SYSTEM : {data['system']} {data['arch']}                  ║")
        print(f"║ BOARD : {data['board']}                                   ║")
        print(f"║ TOTAL PORTS : {data['total_ports']}                           ║")
        print(f"║ STM32 DEVICES : {len(data['stm32_devices'])}                 ║")
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
    STM32Arduino().run()