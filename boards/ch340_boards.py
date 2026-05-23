import serial.tools.list_ports

CH340_VID = 0x1A86
WCH_VID = 0x1A86

class CH340Boards:
    def __init__(self):
        self.ports = []
        self.devices = []

    def scan_ports(self):
        self.ports = list(serial.tools.list_ports.comports())
        return self.ports

    def is_ch340(self, port):
        try:
            vid = getattr(port, "vid", None)
            pid = getattr(port, "pid", None)
            desc = (port.description or "").lower()
            hwid = (port.hwid or "").lower()

            if vid == CH340_VID or vid == WCH_VID:
                return True
            if "ch340" in desc:
                return True
            if "wch" in desc:
                return True
            if "1a86" in hwid:
                return True
            if pid in [0x7523, 0x5523]:
                return True
        except:
            return False

        return False

    def is_arduino(self, port):
        try:
            desc = (port.description or "").lower()
            hwid = (port.hwid or "").lower()

            if "arduino" in desc:
                return True
            if "uno" in desc:
                return True
            if "nano" in desc:
                return True
            if "mega" in desc:
                return True
            if "usb serial" in desc:
                return True
            if "wch" in desc:
                return True
            if "ch340" in desc:
                return True
            if "1a86" in hwid:
                return True
        except:
            return False

        return False

    def get_ch340_devices(self):
        self.devices = []
        for p in self.scan_ports():
            if self.is_ch340(p):
                self.devices.append({
                    "port": p.device,
                    "description": p.description,
                    "hwid": p.hwid,
                    "vid": getattr(p, "vid", None),
                    "pid": getattr(p, "pid", None)
                })
        return self.devices

    def get_arduino_devices(self):
        result = []
        for p in self.scan_ports():
            if self.is_arduino(p):
                result.append({
                    "port": p.device,
                    "description": p.description,
                    "hwid": p.hwid,
                    "vid": getattr(p, "vid", None),
                    "pid": getattr(p, "pid", None)
                })
        return result

    def get_all(self):
        result = []
        for p in self.scan_ports():
            result.append({
                "port": p.device,
                "description": p.description,
                "hwid": p.hwid,
                "vid": getattr(p, "vid", None),
                "pid": getattr(p, "pid", None),
                "ch340": self.is_ch340(p),
                "arduino": self.is_arduino(p)
            })
        return result

    def detect(self):
        self.scan_ports()
        return {
            "total_ports": len(self.ports),
            "ch340_devices": self.get_ch340_devices(),
            "arduino_devices": self.get_arduino_devices(),
            "all_devices": self.get_all()
        }