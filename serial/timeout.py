import time
import threading

class TimeoutManager:
    def __init__(self):
        self.tasks = {}
        self.results = {}
        self.lock = threading.Lock()
        self.counter = 0

    def _gen_id(self):
        self.counter += 1
        return self.counter

    def run(self, func, timeout=5, *args, **kwargs):
        task_id = self._gen_id()
        result = {"done": False, "value": None, "error": None}

        def wrapper():
            try:
                value = func(*args, **kwargs)
                with self.lock:
                    result["done"] = True
                    result["value"] = value
            except Exception as e:
                with self.lock:
                    result["done"] = True
                    result["error"] = str(e)

        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()

        start = time.time()
        while time.time() - start < timeout:
            with self.lock:
                if result["done"]:
                    return result
            time.sleep(0.01)

        return {
            "done": False,
            "timeout": True,
            "value": None
        }

    def run_async(self, func, *args, **kwargs):
        task_id = self._gen_id()
        result = {"done": False, "value": None, "error": None}

        def wrapper():
            try:
                value = func(*args, **kwargs)
                with self.lock:
                    result["done"] = True
                    result["value"] = value
            except Exception as e:
                with self.lock:
                    result["done"] = True
                    result["error"] = str(e)

        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()

        return task_id, result

    def sleep_timeout(self, seconds):
        start = time.time()
        while time.time() - start < seconds:
            time.sleep(0.01)

    def delayed_call(self, func, delay, *args, **kwargs):
        def wrapper():
            time.sleep(delay)
            func(*args, **kwargs)

        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()
        return True

    def kill_switch(self, flag):
        return not flag


if __name__ == "__main__":
    tm = TimeoutManager()

    def test():
        time.sleep(1)
        return "DONE"

    print(tm.run(test, timeout=2))
    print(tm.run(test, timeout=0.5))