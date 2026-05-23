import time
import threading
import collections

class SerialBuffer:
    def __init__(self, max_size=4096):
        self.max_size = max_size
        self.buffer = collections.deque()
        self.lock = threading.Lock()
        self.total_written = 0
        self.total_read = 0
        self.dropped = 0

    def write(self, data):
        if isinstance(data, str):
            data = data.encode()

        with self.lock:
            for b in data:
                if len(self.buffer) >= self.max_size:
                    self.buffer.popleft()
                    self.dropped += 1
                self.buffer.append(b)
                self.total_written += 1

    def write_packet(self, packet):
        length = len(packet)
        header = length.to_bytes(4, "big")
        self.write(header + packet)

    def available(self):
        with self.lock:
            return len(self.buffer)

    def read(self, size=1):
        out = bytearray()

        with self.lock:
            while self.buffer and len(out) < size:
                out.append(self.buffer.popleft())
                self.total_read += 1

        return bytes(out)

    def peek(self, size=1):
        with self.lock:
            return bytes(list(self.buffer)[:size])

    def clear(self):
        with self.lock:
            self.buffer.clear()

    def read_all(self):
        with self.lock:
            data = bytes(self.buffer)
            self.total_read += len(self.buffer)
            self.buffer.clear()
            return data

    def stats(self):
        return {
            "buffer_size": len(self.buffer),
            "max_size": self.max_size,
            "written": self.total_written,
            "read": self.total_read,
            "dropped": self.dropped
        }

    def is_empty(self):
        return self.available() == 0

    def is_full(self):
        return self.available() >= self.max_size

    def fill_ratio(self):
        return self.available() / self.max_size if self.max_size else 0

    def wait_for_data(self, timeout=5):
        start = time.time()
        while self.available() == 0:
            if time.time() - start > timeout:
                return False
            time.sleep(0.01)
        return True


if __name__ == "__main__":
    buf = SerialBuffer(128)

    buf.write("HELLO DEVICE")
    print(buf.read(5))
    print(buf.stats())