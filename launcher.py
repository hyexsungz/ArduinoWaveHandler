import os
import sys
import time
import json
import subprocess
from pathlib import Path


class Launcher:
    def __init__(self):
        self.root = Path.cwd()
        self.config_path = self.root / "config.json"
        self.project_name = "ArduinoWaveHandler"
        self.start_time = time.time()
        self.errors = 0

    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        print(f"{ts} | LAUNCHER | {msg}")

    def load_config(self):
        try:
            if not self.config_path.exists():
                self.log("CONFIG NOT FOUND")
                return {}

            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.log("CONFIG LOADED")
            return data

        except Exception as e:
            self.errors += 1
            self.log(f"CONFIG ERROR {e}")
            return {}

    def check_python(self):
        try:
            version = sys.version
            self.log(f"PYTHON {version}")
            return True
        except Exception as e:
            self.errors += 1
            self.log(f"PYTHON CHECK ERROR {e}")
            return False

    def check_files(self):
        required = [
            "main.py",
            "build.py",
            "config.json"
        ]

        missing = []

        for f in required:
            if not (self.root / f).exists():
                missing.append(f)

        if missing:
            self.log(f"MISSING FILES {missing}")
            return False

        self.log("FILES OK")
        return True

    def run_main(self):
        try:
            self.log("STARTING MAIN SYSTEM")

            if not (self.root / "main.py").exists():
                self.log("main.py NOT FOUND")
                return False

            subprocess.run([sys.executable, "main.py"])
            return True

        except Exception as e:
            self.errors += 1
            self.log(f"MAIN ERROR {e}")
            return False

    def run_build(self):
        try:
            self.log("RUNNING BUILD SYSTEM")

            if not (self.root / "build.py").exists():
                self.log("build.py NOT FOUND")
                return False

            subprocess.run([sys.executable, "build.py"])
            return True

        except Exception as e:
            self.errors += 1
            self.log(f"BUILD ERROR {e}")
            return False

    def menu(self):
        while True:
            print("\n==============================")
            print(" ArduinoWaveHandler Launcher ")
            print("==============================")
            print("1. Run Main System")
            print("2. Run Build System")
            print("3. Check Config")
            print("4. Check Environment")
            print("5. Exit")
            print("==============================")

            choice = input("Select > ")

            if choice == "1":
                self.run_main()

            elif choice == "2":
                self.run_build()

            elif choice == "3":
                cfg = self.load_config()
                print(json.dumps(cfg, indent=2))

            elif choice == "4":
                self.check_python()
                self.check_files()

            elif choice == "5":
                self.log("EXITING")
                break

            else:
                self.log("INVALID OPTION")

    def run(self):
        self.log("LAUNCHER START")

        self.load_config()
        self.check_python()
        self.check_files()

        self.menu()

        self.log(f"LAUNCHER CLOSED | ERRORS={self.errors}")


if __name__ == "__main__":
    Launcher().run()