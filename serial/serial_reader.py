import threading
import time

try:
    import serial
except:
    serial = None

class SerialReader:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.conn = None
        self.buffer = []
        self.running = False
        self.thread = None
        self.errors = 0
        self.read_count = 0

    def open(self):
        if not serial:
            return {"status": "error", "reason": "pyserial_missing"}

        try:
            self.conn = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.running = True
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()
            return {"status": "opened", "port": self.port}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def _loop(self):
        while self.running and self.conn and self.conn.is_open:
            try:
                data = self.conn.readline()
                if data:
                    self.buffer.append({
                        "data": data,
                        "timestamp": time.time()
                    })
                    self.read_count += 1
            except:
                self.errors += 1
                time.sleep(0.1)

    def read(self):
        data = self.buffer[:]
        self.buffer.clear()
        return data

    def available(self):
        return len(self.buffer)

    def write(self, data):
        try:
            if isinstance(data, str):
                data = data.encode()
            self.conn.write(data)
            return True
        except:
            self.errors += 1
            return False

    def close(self):
        self.running = False
        try:
            if self.conn:
                self.conn.close()
        except:
            pass

    def status(self):
        return {
            "port": self.port,
            "running": self.running,
            "available": self.available(),
            "read_count": self.read_count,
            "errors": self.errors
        }

    def flush(self):
        self.buffer.clear()


if __name__ == "__main__":
    reader = SerialReader("COM3")
    print(reader.open())
    time.sleep(2)
    print(reader.status())