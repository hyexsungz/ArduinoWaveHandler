import time
import threading
import platform

try:
    import serial
    import serial.tools.list_ports
except:
    serial = None

class SerialManager:
    def __init__(self):
        self.system = platform.system()
        self.ports = []
        self.connections = {}
        self.read_threads = {}
        self.buffers = {}
        self.running = True

    def scan_ports(self):
        if not serial:
            return []

        self.ports = list(serial.tools.list_ports.comports())
        return self.ports

    def list_ports(self):
        return [{
            "port": p.device,
            "desc": p.description,
            "hwid": p.hwid
        } for p in self.scan_ports()]

    def connect(self, port, baudrate=9600, timeout=1):
        if not serial:
            return {"status": "error", "reason": "pyserial_missing"}

        try:
            conn = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            self.connections[port] = conn
            self.buffers[port] = []

            t = threading.Thread(target=self._reader, args=(port,), daemon=True)
            self.read_threads[port] = t
            t.start()

            return {"status": "connected", "port": port}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def _reader(self, port):
        conn = self.connections.get(port)
        while self.running and conn and conn.is_open:
            try:
                data = conn.readline()
                if data:
                    self.buffers[port].append(data)
            except:
                break

    def write(self, port, data):
        if port not in self.connections:
            return False

        conn = self.connections[port]

        try:
            if isinstance(data, str):
                data = data.encode()

            conn.write(data)
            return True
        except:
            return False

    def read(self, port):
        if port not in self.buffers:
            return []

        data = self.buffers[port][:]
        self.buffers[port] = []
        return data

    def available(self, port):
        return len(self.buffers.get(port, []))

    def disconnect(self, port):
        try:
            if port in self.connections:
                self.connections[port].close()
                del self.connections[port]

            if port in self.buffers:
                del self.buffers[port]

            return True
        except:
            return False

    def disconnect_all(self):
        for p in list(self.connections.keys()):
            self.disconnect(p)

    def is_connected(self, port):
        return port in self.connections

    def stop(self):
        self.running = False
        self.disconnect_all()

    def stats(self):
        return {
            "system": self.system,
            "connected_ports": list(self.connections.keys()),
            "total_connections": len(self.connections)
        }


if __name__ == "__main__":
    sm = SerialManager()
    print(sm.list_ports())