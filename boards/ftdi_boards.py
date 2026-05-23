import serial.tools.list_ports
import time
import platform

class FTDIBoards:
    def __init__(self):
        self.ports = []
        self.devices = []
        self.system = platform.system()
        self.arch = platform.machine()
        self.ftdi_vid = 0x0403

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

    def is_ftdi(self, p):
        try:
            desc = (p.description or "").lower()
            hwid = (p.hwid or "").lower()
            vid = getattr(p, "vid", None)
            pid = getattr(p, "pid", None)

            if vid == self.ftdi_vid:
                return True
            if "ftdi" in desc:
                return True
            if "ft232" in desc:
                return True
            if "ft2232" in desc:
                return True
            if "0403" in hwid:
                return True
            if pid in [0x6001, 0x6010, 0x6011, 0x6014, 0x6015]:
                return True
        except:
            return False

        return False

    def classify(self, p):
        if self.is_ftdi(p):
            return "FTDI_DEVICE"
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

    def get_ftdi_devices(self):
        return [d for d in self.scan() if d["type"] == "FTDI_DEVICE"]

    def detect(self):
        self.scan()
        return {
            "system": self.system,
            "arch": self.arch,
            "total_ports": len(self.ports),
            "ftdi_devices": self.get_ftdi_devices(),
            "all_devices": self.devices
        }

    def print_box(self):
        data = self.detect()
        print("╔══════════════════════════════════════════════════════════╗")
        print("║                   FTDI DEVICE SCANNER                   ║")
        print("╠══════════════════════════════════════════════════════════╣")
        print(f"║ SYSTEM : {data['system']} {data['arch']}                  ║")
        print(f"║ TOTAL PORTS : {data['total_ports']}                           ║")
        print(f"║ FTDI DEVICES : {len(data['ftdi_devices'])}                     ║")
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
    FTDIBoards().run()