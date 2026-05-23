import re
import random
import string
import hashlib
import base64
import time


class StringUtils:
    def __init__(self):
        self.operations = 0
        self.errors = 0
        self.history = []
        self.start_time = time.time()

    def log(self, action, value=""):
        self.history.append({
            "time": time.strftime("%H:%M:%S"),
            "action": action,
            "value": str(value)[:100]
        })

        if len(self.history) > 1000:
            self.history.pop(0)

    def upper(self, text):
        try:
            self.operations += 1
            self.log("UPPER", text)
            return text.upper()
        except:
            self.errors += 1
            return text

    def lower(self, text):
        try:
            self.operations += 1
            self.log("LOWER", text)
            return text.lower()
        except:
            self.errors += 1
            return text

    def reverse(self, text):
        try:
            self.operations += 1
            self.log("REVERSE", text)
            return text[::-1]
        except:
            self.errors += 1
            return text

    def capitalize(self, text):
        try:
            self.operations += 1
            self.log("CAPITALIZE", text)
            return text.capitalize()
        except:
            self.errors += 1
            return text

    def title(self, text):
        try:
            self.operations += 1
            self.log("TITLE", text)
            return text.title()
        except:
            self.errors += 1
            return text

    def strip(self, text):
        try:
            self.operations += 1
            self.log("STRIP", text)
            return text.strip()
        except:
            self.errors += 1
            return text

    def replace(self, text, old, new):
        try:
            self.operations += 1
            self.log("REPLACE", old)
            return text.replace(old, new)
        except:
            self.errors += 1
            return text

    def remove_spaces(self, text):
        try:
            self.operations += 1
            self.log("REMOVE_SPACES", text)
            return text.replace(" ", "")
        except:
            self.errors += 1
            return text

    def count_words(self, text):
        try:
            self.operations += 1
            self.log("COUNT_WORDS", len(text))
            return len(text.split())
        except:
            self.errors += 1
            return 0

    def count_chars(self, text):
        try:
            self.operations += 1
            self.log("COUNT_CHARS", len(text))
            return len(text)
        except:
            self.errors += 1
            return 0

    def contains(self, text, value):
        try:
            self.operations += 1
            self.log("CONTAINS", value)
            return value in text
        except:
            self.errors += 1
            return False

    def starts_with(self, text, value):
        try:
            self.operations += 1
            self.log("STARTS_WITH", value)
            return text.startswith(value)
        except:
            self.errors += 1
            return False

    def ends_with(self, text, value):
        try:
            self.operations += 1
            self.log("ENDS_WITH", value)
            return text.endswith(value)
        except:
            self.errors += 1
            return False

    def split(self, text, sep=None):
        try:
            self.operations += 1
            self.log("SPLIT", sep)
            return text.split(sep)
        except:
            self.errors += 1
            return []

    def join(self, items, sep=" "):
        try:
            self.operations += 1
            self.log("JOIN", len(items))
            return sep.join(items)
        except:
            self.errors += 1
            return ""

    def random_string(self, length=16):
        try:
            chars = string.ascii_letters + string.digits
            result = ''.join(random.choice(chars) for _ in range(length))
            self.operations += 1
            self.log("RANDOM_STRING", length)
            return result
        except:
            self.errors += 1
            return ""

    def random_hex(self, length=16):
        try:
            chars = "abcdef0123456789"
            result = ''.join(random.choice(chars) for _ in range(length))
            self.operations += 1
            self.log("RANDOM_HEX", length)
            return result
        except:
            self.errors += 1
            return ""

    def sha256(self, text):
        try:
            result = hashlib.sha256(text.encode()).hexdigest()
            self.operations += 1
            self.log("SHA256", result[:16])
            return result
        except:
            self.errors += 1
            return None

    def md5(self, text):
        try:
            result = hashlib.md5(text.encode()).hexdigest()
            self.operations += 1
            self.log("MD5", result[:16])
            return result
        except:
            self.errors += 1
            return None

    def b64_encode(self, text):
        try:
            result = base64.b64encode(text.encode()).decode()
            self.operations += 1
            self.log("B64_ENCODE", len(result))
            return result
        except:
            self.errors += 1
            return None

    def b64_decode(self, text):
        try:
            result = base64.b64decode(text.encode()).decode(errors="ignore")
            self.operations += 1
            self.log("B64_DECODE", len(result))
            return result
        except:
            self.errors += 1
            return None

    def regex(self, pattern, text):
        try:
            result = re.findall(pattern, text)
            self.operations += 1
            self.log("REGEX", pattern)
            return result
        except:
            self.errors += 1
            return []

    def regex_replace(self, pattern, repl, text):
        try:
            result = re.sub(pattern, repl, text)
            self.operations += 1
            self.log("REGEX_REPLACE", pattern)
            return result
        except:
            self.errors += 1
            return text

    def clean(self, text):
        try:
            result = re.sub(r"\s+", " ", text).strip()
            self.operations += 1
            self.log("CLEAN", len(result))
            return result
        except:
            self.errors += 1
            return text

    def remove_special(self, text):
        try:
            result = re.sub(r"[^a-zA-Z0-9 ]", "", text)
            self.operations += 1
            self.log("REMOVE_SPECIAL", len(result))
            return result
        except:
            self.errors += 1
            return text

    def only_numbers(self, text):
        try:
            result = ''.join(filter(str.isdigit, text))
            self.operations += 1
            self.log("ONLY_NUMBERS", result)
            return result
        except:
            self.errors += 1
            return ""

    def only_letters(self, text):
        try:
            result = ''.join(filter(str.isalpha, text))
            self.operations += 1
            self.log("ONLY_LETTERS", result)
            return result
        except:
            self.errors += 1
            return ""

    def pad_left(self, text, size, char=" "):
        try:
            result = text.rjust(size, char)
            self.operations += 1
            self.log("PAD_LEFT", size)
            return result
        except:
            self.errors += 1
            return text

    def pad_right(self, text, size, char=" "):
        try:
            result = text.ljust(size, char)
            self.operations += 1
            self.log("PAD_RIGHT", size)
            return result
        except:
            self.errors += 1
            return text

    def repeat(self, text, count):
        try:
            result = text * count
            self.operations += 1
            self.log("REPEAT", count)
            return result
        except:
            self.errors += 1
            return text

    def uptime(self):
        return int(time.time() - self.start_time)

    def stats(self):
        return {
            "operations": self.operations,
            "errors": self.errors,
            "uptime": self.uptime(),
            "history": len(self.history)
        }

    def get_history(self):
        return self.history


string_utils = StringUtils()