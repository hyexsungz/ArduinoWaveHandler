import json
import re
import time
import hashlib
import base64
import urllib.parse
import xml.etree.ElementTree as ET


class Parser:
    def __init__(self):
        self.history = []
        self.errors = 0
        self.parsed = 0
        self.start_time = time.time()

    def log(self, action, value=""):
        self.history.append({
            "time": time.strftime("%H:%M:%S"),
            "action": action,
            "value": str(value)[:120]
        })

        if len(self.history) > 1000:
            self.history.pop(0)

    def parse_json(self, data):
        try:
            obj = json.loads(data)
            self.parsed += 1
            self.log("JSON_PARSE", "SUCCESS")
            return obj
        except Exception as e:
            self.errors += 1
            self.log("JSON_PARSE_ERROR", e)
            return None

    def dump_json(self, obj, indent=4):
        try:
            data = json.dumps(obj, indent=indent)
            self.parsed += 1
            self.log("JSON_DUMP", "SUCCESS")
            return data
        except Exception as e:
            self.errors += 1
            self.log("JSON_DUMP_ERROR", e)
            return None

    def parse_xml(self, data):
        try:
            root = ET.fromstring(data)
            self.parsed += 1
            self.log("XML_PARSE", root.tag)
            return root
        except Exception as e:
            self.errors += 1
            self.log("XML_PARSE_ERROR", e)
            return None

    def regex(self, pattern, data):
        try:
            result = re.findall(pattern, data)
            self.parsed += 1
            self.log("REGEX", pattern)
            return result
        except Exception as e:
            self.errors += 1
            self.log("REGEX_ERROR", e)
            return []

    def split_lines(self, data):
        self.parsed += 1
        self.log("SPLIT_LINES", len(data))
        return data.splitlines()

    def split_words(self, data):
        self.parsed += 1
        self.log("SPLIT_WORDS", len(data))
        return data.split()

    def clean(self, data):
        self.parsed += 1
        cleaned = re.sub(r"\s+", " ", data).strip()
        self.log("CLEAN", len(cleaned))
        return cleaned

    def extract_numbers(self, data):
        try:
            nums = re.findall(r"\d+", data)
            self.parsed += 1
            self.log("EXTRACT_NUMBERS", len(nums))
            return nums
        except Exception as e:
            self.errors += 1
            self.log("EXTRACT_NUMBERS_ERROR", e)
            return []

    def extract_hex(self, data):
        try:
            vals = re.findall(r"0x[a-fA-F0-9]+", data)
            self.parsed += 1
            self.log("EXTRACT_HEX", len(vals))
            return vals
        except Exception as e:
            self.errors += 1
            self.log("EXTRACT_HEX_ERROR", e)
            return []

    def parse_key_value(self, data, sep="="):
        result = {}

        try:
            lines = data.splitlines()

            for line in lines:
                if sep in line:
                    k, v = line.split(sep, 1)
                    result[k.strip()] = v.strip()

            self.parsed += 1
            self.log("KEY_VALUE_PARSE", len(result))
            return result

        except Exception as e:
            self.errors += 1
            self.log("KEY_VALUE_ERROR", e)
            return {}

    def sha256(self, data):
        try:
            digest = hashlib.sha256(data.encode()).hexdigest()
            self.parsed += 1
            self.log("SHA256", digest[:16])
            return digest
        except Exception as e:
            self.errors += 1
            self.log("SHA256_ERROR", e)
            return None

    def md5(self, data):
        try:
            digest = hashlib.md5(data.encode()).hexdigest()
            self.parsed += 1
            self.log("MD5", digest[:16])
            return digest
        except Exception as e:
            self.errors += 1
            self.log("MD5_ERROR", e)
            return None

    def b64_encode(self, data):
        try:
            out = base64.b64encode(data.encode()).decode()
            self.parsed += 1
            self.log("B64_ENCODE", len(out))
            return out
        except Exception as e:
            self.errors += 1
            self.log("B64_ENCODE_ERROR", e)
            return None

    def b64_decode(self, data):
        try:
            out = base64.b64decode(data.encode()).decode(errors="ignore")
            self.parsed += 1
            self.log("B64_DECODE", len(out))
            return out
        except Exception as e:
            self.errors += 1
            self.log("B64_DECODE_ERROR", e)
            return None

    def url_encode(self, data):
        try:
            out = urllib.parse.quote(data)
            self.parsed += 1
            self.log("URL_ENCODE", len(out))
            return out
        except Exception as e:
            self.errors += 1
            self.log("URL_ENCODE_ERROR", e)
            return None

    def url_decode(self, data):
        try:
            out = urllib.parse.unquote(data)
            self.parsed += 1
            self.log("URL_DECODE", len(out))
            return out
        except Exception as e:
            self.errors += 1
            self.log("URL_DECODE_ERROR", e)
            return None

    def between(self, data, start, end):
        try:
            result = []
            pattern = re.escape(start) + "(.*?)" + re.escape(end)
            matches = re.findall(pattern, data, re.DOTALL)

            for m in matches:
                result.append(m)

            self.parsed += 1
            self.log("BETWEEN", len(result))
            return result

        except Exception as e:
            self.errors += 1
            self.log("BETWEEN_ERROR", e)
            return []

    def uptime(self):
        return int(time.time() - self.start_time)

    def stats(self):
        return {
            "parsed": self.parsed,
            "errors": self.errors,
            "uptime": self.uptime(),
            "history": len(self.history)
        }

    def get_history(self):
        return self.history


parser = Parser()