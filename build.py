import os
import shutil
import json
import time
import subprocess
from pathlib import Path


class BuildSystem:
    def __init__(self):
        self.root = Path.cwd()
        self.build_dir = self.root / "build"
        self.dist_dir = self.root / "dist"
        self.logs_dir = self.root / "logs"
        self.errors = 0
        self.steps = 0
        self.start_time = time.time()

    def log(self, msg):
        ts = time.strftime("%H:%M:%S")
        line = f"{ts} | {msg}"
        print(line)

        self.logs_dir.mkdir(exist_ok=True)
        with open(self.logs_dir / "build.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def clean(self):
        try:
            self.log("CLEAN START")

            for folder in [self.build_dir, self.dist_dir]:
                if folder.exists():
                    shutil.rmtree(folder)

            self.build_dir.mkdir(exist_ok=True)
            self.dist_dir.mkdir(exist_ok=True)

            self.steps += 1
            self.log("CLEAN DONE")
        except Exception as e:
            self.errors += 1
            self.log(f"CLEAN ERROR {e}")

    def scan_project(self):
        try:
            self.log("SCAN PROJECT")

            files = []
            for root, _, fs in os.walk(self.root):
                for f in fs:
                    if f.endswith(".py"):
                        files.append(os.path.join(root, f))

            self.steps += 1
            self.log(f"FOUND {len(files)} PY FILES")
            return files

        except Exception as e:
            self.errors += 1
            self.log(f"SCAN ERROR {e}")
            return []

    def validate_syntax(self, files):
        try:
            self.log("VALIDATE SYNTAX")

            for f in files:
                result = subprocess.run(
                    ["python", "-m", "py_compile", f],
                    capture_output=True,
                    text=True
                )

                if result.returncode != 0:
                    self.errors += 1
                    self.log(f"SYNTAX ERROR {f}")

            self.steps += 1
            self.log("VALIDATION DONE")

        except Exception as e:
            self.errors += 1
            self.log(f"VALIDATION ERROR {e}")

    def bundle(self, files):
        try:
            self.log("BUNDLE START")

            bundle_file = self.dist_dir / "bundle.txt"

            with open(bundle_file, "w", encoding="utf-8") as out:
                for f in files:
                    try:
                        with open(f, "r", encoding="utf-8", errors="ignore") as src:
                            out.write("\n\n# FILE: " + f + "\n")
                            out.write(src.read())
                    except:
                        self.errors += 1

            self.steps += 1
            self.log("BUNDLE DONE")

        except Exception as e:
            self.errors += 1
            self.log(f"BUNDLE ERROR {e}")

    def make_manifest(self, files):
        try:
            self.log("MAKE MANIFEST")

            manifest = {
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "files": len(files),
                "build_steps": self.steps,
                "errors": self.errors
            }

            with open(self.dist_dir / "manifest.json", "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2)

            self.steps += 1
            self.log("MANIFEST DONE")

        except Exception as e:
            self.errors += 1
            self.log(f"MANIFEST ERROR {e}")

    def run(self):
        self.log("BUILD SYSTEM START")

        self.clean()
        files = self.scan_project()
        self.validate_syntax(files)
        self.bundle(files)
        self.make_manifest(files)

        self.log(f"BUILD COMPLETE | STEPS={self.steps} ERRORS={self.errors}")

        return self.errors == 0


if __name__ == "__main__":
    builder = BuildSystem()
    builder.run()