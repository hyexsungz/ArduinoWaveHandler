import time
import threading
import queue

class Stream:
    def __init__(self, max_size=10000):
        self.q = queue.Queue(maxsize=max_size)
        self.lock = threading.Lock()
        self.running = False
        self.reader_threads = []
        self.writer_threads = []
        self.stats_data = {
            "written": 0,
            "read": 0,
            "dropped": 0
        }

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def write(self, data):
        try:
            if isinstance(data, str):
                data = data.encode()

            self.q.put_nowait(data)
            self.stats_data["written"] += 1
            return True
        except:
            self.stats_data["dropped"] += 1
            return False

    def read(self, timeout=0.1):
        try:
            data = self.q.get(timeout=timeout)
            self.stats_data["read"] += 1
            return data
        except:
            return None

    def available(self):
        return self.q.qsize()

    def clear(self):
        with self.lock:
            while not self.q.empty():
                try:
                    self.q.get_nowait()
                except:
                    break

    def bulk_write(self, data_list):
        results = []
        for d in data_list:
            results.append(self.write(d))
        return results

    def bulk_read(self, count=10):
        out = []
        for _ in range(count):
            d = self.read(timeout=0.01)
            if d is None:
                break
            out.append(d)
        return out

    def stats(self):
        return {
            "queue_size": self.available(),
            "written": self.stats_data["written"],
            "read": self.stats_data["read"],
            "dropped": self.stats_data["dropped"]
        }

    def wait_for_data(self, timeout=5):
        start = time.time()
        while self.available() == 0:
            if time.time() - start > timeout:
                return False
            time.sleep(0.01)
        return True


if __name__ == "__main__":
    s = Stream()
    s.start()

    s.write("HELLO")
    s.write("WORLD")

    print(s.bulk_read(5))
    print(s.stats())