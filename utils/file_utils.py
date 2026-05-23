import os
import shutil
import json
import time
import hashlib
import tempfile
import pathlib
import uuid
import random


class FileUtils:
    def __init__(self):
        self.cwd = os.getcwd()
        self.log_path = os.path.join(self.cwd, "fileutils_runtime.log")
        self.ensure_log()
        self.session_id = str(uuid.uuid4())
        self.ops = 0
        self.errors = 0

    def ensure_log(self):
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8") as f:
                f.write("FILEUTILS LOG START\n")

    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        line = f"{ts} | {msg}\n"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line)

    def _safe(self, path):
        try:
            return os.path.abspath(path)
        except:
            return path

    def exists(self, path):
        return os.path.exists(path)

    def is_file(self, path):
        return os.path.isfile(path)

    def is_dir(self, path):
        return os.path.isdir(path)

    def mkdir(self, path):
        try:
            os.makedirs(path, exist_ok=True)
            self.ops += 1
            self.log(f"MKDIR {path}")
            return True
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR MKDIR {path} {e}")
            return False

    def write(self, path, data):
        try:
            folder = os.path.dirname(path)
            if folder:
                os.makedirs(folder, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(str(data))
            self.ops += 1
            self.log(f"WRITE {path} {len(str(data))}")
            return True
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR WRITE {path} {e}")
            return False

    def append(self, path, data):
        try:
            folder = os.path.dirname(path)
            if folder:
                os.makedirs(folder, exist_ok=True)
            with open(path, "a", encoding="utf-8") as f:
                f.write(str(data))
            self.ops += 1
            self.log(f"APPEND {path} {len(str(data))}")
            return True
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR APPEND {path} {e}")
            return False

    def read(self, path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()
            self.ops += 1
            self.log(f"READ {path}")
            return data
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR READ {path} {e}")
            return None

    def delete(self, path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.exists(path):
                os.remove(path)
            self.ops += 1
            self.log(f"DELETE {path}")
            return True
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR DELETE {path} {e}")
            return False

    def move(self, src, dst):
        try:
            shutil.move(src, dst)
            self.ops += 1
            self.log(f"MOVE {src} -> {dst}")
            return True
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR MOVE {src} {dst} {e}")
            return False

    def copy(self, src, dst):
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            self.ops += 1
            self.log(f"COPY {src} -> {dst}")
            return True
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR COPY {src} {dst} {e}")
            return False

    def list_dir(self, path):
        try:
            items = os.listdir(path)
            self.ops += 1
            self.log(f"LIST {path}")
            return items
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR LIST {path} {e}")
            return []

    def tree(self, path, depth=5):
        result = []

        def walk(p, d):
            if d > depth:
                return
            try:
                items = os.listdir(p)
            except:
                return
            for i in items:
                fp = os.path.join(p, i)
                result.append((d, fp))
                if os.path.isdir(fp):
                    walk(fp, d + 1)

        walk(path, 0)
        self.log(f"TREE {path}")
        return result

    def size(self, path):
        try:
            if os.path.isfile(path):
                return os.path.getsize(path)

            total = 0
            for root, _, files in os.walk(path):
                for f in files:
                    fp = os.path.join(root, f)
                    if os.path.exists(fp):
                        total += os.path.getsize(fp)

            self.ops += 1
            self.log(f"SIZE {path}")
            return total
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR SIZE {path} {e}")
            return 0

    def hash_file(self, path, algo="sha256"):
        try:
            h = hashlib.new(algo)
            with open(path, "rb") as f:
                while True:
                    b = f.read(8192)
                    if not b:
                        break
                    h.update(b)
            self.ops += 1
            digest = h.hexdigest()
            self.log(f"HASH {path} {algo}")
            return digest
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR HASH {path} {e}")
            return None

    def touch(self, path):
        try:
            pathlib.Path(path).touch()
            self.ops += 1
            self.log(f"TOUCH {path}")
            return True
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR TOUCH {path} {e}")
            return False

    def temp_file(self, data=""):
        try:
            fd, path = tempfile.mkstemp()
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(str(data))
            self.ops += 1
            self.log(f"TEMPFILE {path}")
            return path
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR TEMPFILE {e}")
            return None

    def random_file(self, folder, size=128):
        try:
            self.mkdir(folder)
            name = f"file_{random.randint(10000,99999)}.bin"
            path = os.path.join(folder, name)
            data = os.urandom(size)
            with open(path, "wb") as f:
                f.write(data)
            self.ops += 1
            self.log(f"RANDOM FILE {path}")
            return path
        except Exception as e:
            self.errors += 1
            self.log(f"ERROR RANDOM {e}")
            return None

    def stats(self):
        return {
            "session": self.session_id,
            "ops": self.ops,
            "errors": self.errors,
            "cwd": self.cwd
        }


file_utils = FileUtils()