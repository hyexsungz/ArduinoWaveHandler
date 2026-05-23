import time
import threading

try:
    import serial
    import serial.tools.list_ports
except:
    serial = None

class AutoConnect:
    def __init__(self, baudrate=115200, timeout=1):
        self.baudrate = baudrate
        self.timeout = timeout

        self.connection = None
        self.connected_port = None

        self.running = False
        self.thread = None

        self.detected = []
        self.history = []

        self.connected = 0
        self.disconnected = 0
        self.errors = 0

        self.keywords = [
            "arduino",
            "ch340",
            "cp210",
            "usb serial",
            "wch",
            "ttyusb",
            "ttyacm",
            "ftdi",
            "uno",
            "mega",
            "nano",
            "leonardo",
            "esp32",
            "esp8266",
            "stm32",
            "teensy"
        ]

    def _valid(self, port):
        text = " ".join([
            str(port.device),
            str(port.description),
            str(port.hwid),
            str(getattr(port, "manufacturer", "")),
            str(getattr(port, "product", ""))
        ]).lower()

        for keyword in self.keywords:
            if keyword in text:
                return True

        return False

    def scan(self):
        self.detected = []

        if not serial:
            return []

        try:
            ports = serial.tools.list_ports.comports()

            for port in ports:
                if self._valid(port):
                    info = {
                        "device": str(port.device),
                        "description": str(port.description),
                        "hwid": str(port.hwid),
                        "manufacturer": str(getattr(port, "manufacturer", "")),
                        "product": str(getattr(port, "product", "")),
                        "timestamp": int(time.time())
                    }

                    self.detected.append(info)
                    self.history.append(info)

        except:
            self.errors += 1

        return self.detected

    def connect(self, port):
        try:
            self.connection = serial.Serial(
                port,
                self.baudrate,
                timeout=self.timeout
            )

            self.connected_port = port
            self.connected += 1

            return True

        except:
            self.errors += 1
            return False

    def disconnect(self):
        try:
            if self.connection:
                self.connection.close()

            self.connection = None
            self.connected_port = None
            self.disconnected += 1

            return True

        except:
            self.errors += 1
            return False

    def auto_connect(self):
        devices = self.scan()

        if not devices:
            return False

        for dev in devices:
            port = dev["device"]

            if self.connect(port):
                print("[+] CONNECTED:", port)
                return True

        return False

    def write(self, data):
        if not self.connection:
            return False

        try:
            if isinstance(data, str):
                data = data.encode()

            self.connection.write(data)
            return True

        except:
            self.errors += 1
            return False

    def read(self, size=1024):
        if not self.connection:
            return b""

        try:
            return self.connection.read(size)

        except:
            self.errors += 1
            return b""

    def heartbeat(self):
        while self.running:
            try:
                if self.connection:
                    self.write(b"HEARTBEAT\n")
            except:
                self.errors += 1

            time.sleep(3)

    def start(self):
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.heartbeat,
            daemon=True
        )

        self.thread.start()

    def stop(self):
        self.running = False
        self.disconnect()

    def monitor(self, delay=2):
        last = set()

        while True:
            current_scan = self.scan()

            current = set(
                x["device"]
                for x in current_scan
            )

            added = current - last
            removed = last - current

            for port in added:
                print("[+] DEVICE DETECTED:", port)

                if not self.connection:
                    self.connect(port)

            for port in removed:
                print("[-] DEVICE REMOVED:", port)

                if self.connected_port == port:
                    self.disconnect()

            last = current

            time.sleep(delay)

    def status(self):
        return {
            "connected_port": self.connected_port,
            "baudrate": self.baudrate,
            "connected_total": self.connected,
            "disconnected_total": self.disconnected,
            "errors": self.errors,
            "running": self.running
        }

    def reset(self):
        self.disconnect()

        self.detected = []
        self.history = []

        self.connected = 0
        self.disconnected = 0
        self.errors = 0


if __name__ == "__main__":
    ac = AutoConnect()

    ac.start()

    if ac.auto_connect():
        print("[INFO] Device connection established")
        print(ac.status())

        while True:
            data = ac.read(256)

            if data:
                print("[DATA]", data)

            time.sleep(1)

    else:
        print("[INFO] No compatible device found")