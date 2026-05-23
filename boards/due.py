import serial.tools.list_ports
import time
import platform
import socket
import uuid
import json

class DUEBoard:
    def __init__(self):
        self.ports = []
        self.devices = []
        self.system = platform.system()
        self.node = platform.node()
        self.arch = platform.machine()
        self.chip = "ATSAM3X8E"
        self.board = "Arduino Due"
        self.vendor_id = 0x2341
        self.expected_keywords = ["due", "sam3x", "atsam3x8e", "arduino due"]
        self.last_scan = None
        self.session_id = str(uuid.uuid4())

    def scan_ports(self):
        self.ports = list(serial.tools.list_ports.comports())
        self.last_scan = time.time()
        return self.ports

    def port_signature(self, port):
        try:
            return {
                "device": port.device,
                "description": port.description,
                "hwid": port.hwid,
                "vid": getattr(port, "vid", None),
                "pid": getattr(port, "pid", None)
            }
        except:
            return {
                "device": None,
                "description": None,
                "hwid": None,
                "vid": None,
                "pid": None
            }

    def is_due(self, port):
        try:
            desc = (port.description or "").lower()
            hwid = (port.hwid or "").lower()
            vid = getattr(port, "vid", None)
            pid = getattr(port, "pid", None)

            if vid == self.vendor_id:
                if any(k in desc for k in self.expected_keywords):
                    return True
                if any(k in hwid for k in self.expected_keywords):
                    return True

            if "arduino due" in desc:
                return True
            if "sam3x" in desc:
                return True
            if "atsam3x" in desc:
                return True
            if "3x8e" in desc:
                return True

            if "2341" in hwid:
                if "due" in desc or "sam3x" in hwid:
                    return True

            if "usb serial" in desc and "arduino" in desc:
                return True

        except:
            return False

        return False

    def classify_port(self, port):
        desc = (port.description or "").lower()
        hwid = (port.hwid or "").lower()

        if self.is_due(port):
            return "ARDUINO_DUE"

        if "ch340" in desc or "1a86" in hwid:
            return "CH340_SERIAL"

        if "cp210" in desc or "10c4" in hwid:
            return "CP210X_SERIAL"

        if "ftdi" in desc or "0403" in hwid:
            return "FTDI_SERIAL"

        if "usb serial" in desc:
            return "USB_SERIAL_GENERIC"

        return "UNKNOWN"

    def get_due_devices(self):
        self.devices = []
        for p in self.scan_ports():
            if self.is_due(p):
                self.devices.append({
                    "port": p.device,
                    "description": p.description,
                    "hwid": p.hwid,
                    "vid": getattr(p, "vid", None),
                    "pid": getattr(p, "pid", None),
                    "chip": self.chip,
                    "board": self.board,
                    "class": "DUE",
                    "signature": self.port_signature(p)
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
                "class": self.classify_port(p)
            })
        return result

    def system_info(self):
        return {
            "system": self.system,
            "node": self.node,
            "arch": self.arch,
            "session": self.session_id,
            "timestamp": time.time()
        }

    def detect(self):
        self.scan_ports()
        return {
            "board": self.board,
            "chip": self.chip,
            "system": self.system_info(),
            "total_ports": len(self.ports),
            "due_devices": self.get_due_devices(),
            "all_devices": self.get_all_devices()
        }

    def live_monitor(self, interval=2):
        last = set()
        while True:
            self.scan_ports()
            current = set(p.device for p in self.ports)

            added = current - last
            removed = last - current

            if added or removed:
                print("PORT CHANGE DETECTED")
                for a in added:
                    print("CONNECTED:", a)
                for r in removed:
                    print("DISCONNECTED:", r)

            last = current
            time.sleep(interval)

    def export_json(self):
        return json.dumps(self.detect(), indent=2)

    def print_status(self):
        data = self.detect()
        print("ARDUINO DUE MONITOR")
        print("BOARD:", data["board"])
        print("CHIP:", data["chip"])
        print("TOTAL PORTS:", data["total_ports"])
        print("DUE DEVICES:", len(data["due_devices"]))
        print("SYSTEM:", data["system"]["system"], data["system"]["arch"])

    def run_cli(self):
        self.print_status()
        self.live_monitor()


if __name__ == "__main__":
    DUEBoard().run_cli()