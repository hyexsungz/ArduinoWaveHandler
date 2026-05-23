import time
import threading

try:
    import serial
except:
    serial = None

class SerialWriter:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.conn = None
        self.queue = []
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
        self.sent = 0
        self.failed = 0

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
                packet = None

                with self.lock:
                    if self.queue:
                        packet = self.queue.pop(0)

                if packet is not None:
                    self.conn.write(packet)
                    self.sent += 1
                else:
                    time.sleep(0.01)

            except:
                self.failed += 1
                time.sleep(0.1)

    def send(self, data):
        try:
            if isinstance(data, str):
                data = data.encode()

            with self.lock:
                self.queue.append(data)

            return True
        except:
            self.failed += 1
            return False

    def send_line(self, text):
        return self.send(text + "\n")

    def send_packet(self, packet):
        return self.send(packet)

    def flush(self):
        with self.lock:
            self.queue.clear()

    def pending(self):
        return len(self.queue)

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
            "pending": self.pending(),
            "sent": self.sent,
            "failed": self.failed
        }


if __name__ == "__main__":
    writer = SerialWriter("COM3")
    print(writer.open())
    writer.send_line("BOARD CONNECTED")
    time.sleep(1)
    print(writer.status())