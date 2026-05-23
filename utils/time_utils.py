import time
import datetime
import calendar
import threading


class TimeUtils:
    def __init__(self):
        self.start_time = time.time()
        self.operations = 0
        self.errors = 0
        self.history = []
        self.timers = {}
        self.stopwatch_data = {}
        self.lock = threading.Lock()

    def log(self, action, value=""):
        self.history.append({
            "time": self.now_time(),
            "action": action,
            "value": str(value)[:100]
        })

        if len(self.history) > 1000:
            self.history.pop(0)

    def now(self):
        try:
            self.operations += 1
            value = datetime.datetime.now()
            self.log("NOW", value)
            return value
        except:
            self.errors += 1
            return None

    def now_time(self):
        try:
            self.operations += 1
            value = datetime.datetime.now().strftime("%H:%M:%S")
            self.log("NOW_TIME", value)
            return value
        except:
            self.errors += 1
            return "00:00:00"

    def now_date(self):
        try:
            self.operations += 1
            value = datetime.datetime.now().strftime("%Y-%m-%d")
            self.log("NOW_DATE", value)
            return value
        except:
            self.errors += 1
            return "0000-00-00"

    def timestamp(self):
        try:
            self.operations += 1
            value = int(time.time())
            self.log("TIMESTAMP", value)
            return value
        except:
            self.errors += 1
            return 0

    def unix_ms(self):
        try:
            self.operations += 1
            value = int(time.time() * 1000)
            self.log("UNIX_MS", value)
            return value
        except:
            self.errors += 1
            return 0

    def sleep(self, seconds):
        try:
            self.operations += 1
            self.log("SLEEP", seconds)
            time.sleep(seconds)
            return True
        except:
            self.errors += 1
            return False

    def format_time(self, fmt="%H:%M:%S"):
        try:
            self.operations += 1
            value = datetime.datetime.now().strftime(fmt)
            self.log("FORMAT_TIME", value)
            return value
        except:
            self.errors += 1
            return ""

    def year(self):
        try:
            self.operations += 1
            value = datetime.datetime.now().year
            self.log("YEAR", value)
            return value
        except:
            self.errors += 1
            return 0

    def month(self):
        try:
            self.operations += 1
            value = datetime.datetime.now().month
            self.log("MONTH", value)
            return value
        except:
            self.errors += 1
            return 0

    def day(self):
        try:
            self.operations += 1
            value = datetime.datetime.now().day
            self.log("DAY", value)
            return value
        except:
            self.errors += 1
            return 0

    def hour(self):
        try:
            self.operations += 1
            value = datetime.datetime.now().hour
            self.log("HOUR", value)
            return value
        except:
            self.errors += 1
            return 0

    def minute(self):
        try:
            self.operations += 1
            value = datetime.datetime.now().minute
            self.log("MINUTE", value)
            return value
        except:
            self.errors += 1
            return 0

    def second(self):
        try:
            self.operations += 1
            value = datetime.datetime.now().second
            self.log("SECOND", value)
            return value
        except:
            self.errors += 1
            return 0

    def weekday(self):
        try:
            self.operations += 1
            value = calendar.day_name[datetime.datetime.now().weekday()]
            self.log("WEEKDAY", value)
            return value
        except:
            self.errors += 1
            return ""

    def month_name(self):
        try:
            self.operations += 1
            value = calendar.month_name[datetime.datetime.now().month]
            self.log("MONTH_NAME", value)
            return value
        except:
            self.errors += 1
            return ""

    def uptime(self):
        try:
            self.operations += 1
            value = int(time.time() - self.start_time)
            self.log("UPTIME", value)
            return value
        except:
            self.errors += 1
            return 0

    def countdown(self, seconds):
        try:
            self.operations += 1
            result = []

            for i in range(seconds, -1, -1):
                result.append(i)

            self.log("COUNTDOWN", seconds)
            return result

        except:
            self.errors += 1
            return []

    def create_timer(self, name):
        try:
            self.operations += 1
            self.timers[name] = time.time()
            self.log("CREATE_TIMER", name)
            return True
        except:
            self.errors += 1
            return False

    def timer_elapsed(self, name):
        try:
            if name not in self.timers:
                return None

            self.operations += 1
            value = time.time() - self.timers[name]
            self.log("TIMER_ELAPSED", name)
            return value

        except:
            self.errors += 1
            return None

    def remove_timer(self, name):
        try:
            if name in self.timers:
                del self.timers[name]

            self.operations += 1
            self.log("REMOVE_TIMER", name)
            return True

        except:
            self.errors += 1
            return False

    def start_stopwatch(self, name):
        try:
            self.operations += 1
            self.stopwatch_data[name] = {
                "start": time.time(),
                "running": True
            }
            self.log("START_STOPWATCH", name)
            return True
        except:
            self.errors += 1
            return False

    def stop_stopwatch(self, name):
        try:
            if name not in self.stopwatch_data:
                return None

            elapsed = time.time() - self.stopwatch_data[name]["start"]
            self.stopwatch_data[name]["running"] = False

            self.operations += 1
            self.log("STOP_STOPWATCH", name)

            return elapsed

        except:
            self.errors += 1
            return None

    def stopwatch_elapsed(self, name):
        try:
            if name not in self.stopwatch_data:
                return None

            elapsed = time.time() - self.stopwatch_data[name]["start"]

            self.operations += 1
            self.log("STOPWATCH_ELAPSED", name)

            return elapsed

        except:
            self.errors += 1
            return None

    def parse_date(self, value, fmt="%Y-%m-%d"):
        try:
            self.operations += 1
            parsed = datetime.datetime.strptime(value, fmt)
            self.log("PARSE_DATE", value)
            return parsed
        except:
            self.errors += 1
            return None

    def future_timestamp(self, seconds):
        try:
            self.operations += 1
            value = int(time.time() + seconds)
            self.log("FUTURE_TIMESTAMP", seconds)
            return value
        except:
            self.errors += 1
            return 0

    def past_timestamp(self, seconds):
        try:
            self.operations += 1
            value = int(time.time() - seconds)
            self.log("PAST_TIMESTAMP", seconds)
            return value
        except:
            self.errors += 1
            return 0

    def stats(self):
        return {
            "operations": self.operations,
            "errors": self.errors,
            "uptime": self.uptime(),
            "history": len(self.history),
            "timers": len(self.timers),
            "stopwatches": len(self.stopwatch_data)
        }

    def get_history(self):
        return self.history


time_utils = TimeUtils()