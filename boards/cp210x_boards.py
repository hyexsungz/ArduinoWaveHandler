import serial.tools.list_ports

CP210X_VID = 0x10C4

class CP210XBoards:
    def __init__(self):
        self.ports = []
        self.devices = []

    def scan_ports(self):
        self.ports = list(serial.tools.list_ports.comports())
        return self.ports

    def is_cp210x(self, port):
        try:
            vid = getattr(port, "vid", None)
            pid = getattr(port, "pid", None)
            desc = (port.description or "").lower()
            hwid = (port.hwid or "").lower()

            if vid == CP210X_VID:
                return True
            if "cp210" in desc:
                return True
            if "silicon labs" in desc:
                return True
            if "10c4" in hwid:
                return True
            if pid in [0xea60, 0xea61]:
                return True
        except:
            return False

        return False

    def is_serial_device(self, port):
        try:
            desc = (port.description or "").lower()
            hwid = (port.hwid or "").lower()

            if "usb serial" in desc:
                return True
            if "serial" in desc:
                return True
            if "cp210" in desc:
                return True
            if "silicon" in desc:
                return True
            if "10c4" in hwid:
                return True
        except:
            return False

        return False

    def get_cp210x_devices(self):
        self.devices = []
        for p in self.scan_ports():
            if self.is_cp210x(p):
                self.devices.append({
                    "port": p.device,
                    "description": p.description,
                    "hwid": p.hwid,
                    "vid": getattr(p, "vid", None),
                    "pid": getattr(p, "pid", None)
                })
        return self.devices

    def get_all_devices(self):
        result = []
        for p in self.scan_ports():
            result.append({
                "port": p.device,
                "description": p.description,
                "hwid": p.hwid,
                "vid": getattr(p, "vid", None),
                "pid": getattr(p, "pid", None),
                "cp210x": self.is_cp210x(p),
                "serial": self.is_serial_device(p)
            })
        return result

    def detect(self):
        self.scan_ports()
        return {
            "total_ports": len(self.ports),
            "cp210x_devices": self.get_cp210x_devices(),
            "all_devices": self.get_all_devices()
        }