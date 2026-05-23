````md id="buildmd001"
# BUILDING.md

## ArduinoWaveHandler Build Guide

This document explains how to build, run, and test the ArduinoWaveHandler framework.

---

## Requirements

### Python Version
- Python 3.10+
- pip installed

### Optional Tools
- Git
- VS Code
- Arduino IDE (for hardware testing)
- CMake (only if integrating C/C++ modules later)

---

## Project Setup

Clone or extract the project:

```bash
cd ArduinoWaveHandler
````

Check structure:

```
utils/
core/
tests/
build.py
main.py
ARCHITECTURE.md
```

---

## Running the System

### Run main framework

```bash
python main.py
```

### Run build system

```bash
python build.py
```

---

## Build System Behavior

When you run `build.py`, it will:

1. Clean old build files
2. Scan all `.py` files
3. Validate syntax
4. Bundle all scripts into a single file
5. Generate a build manifest

Output:

```
/build
/dist
/logs/build.log
```

---

## Testing Modules

You can test modules individually:

### Console

```bash
python -c "from utils.console import *"
```

### Logger

```bash
python -c "from utils.logger import logger; logger.info('test')"
```

### File Utils

```bash
python -c "from utils.file_utils import file_utils; print(file_utils.stats())"
```

### Parser

```bash
python -c "from utils.parser import parser; print(parser.stats())"
```

### String Utils

```bash
python -c "from utils.string_utils import string_utils; print(string_utils.random_string(32))"
```

### Time Utils

```bash
python -c "from utils.time_utils import time_utils; print(time_utils.now_time())"
```

---

## Debug Mode

To debug build system:

```bash
python build.py
```

Check logs:

```
/logs/build.log
```

---

## Expected Output Example

```
BUILD SYSTEM START
CLEAN START
CLEAN DONE
SCAN PROJECT
FOUND 6 PY FILES
VALIDATE SYNTAX
VALIDATION DONE
BUNDLE START
BUNDLE DONE
MAKE MANIFEST
BUILD COMPLETE | STEPS=4 ERRORS=0
```

---

## Common Issues

### 1. Python not found

Use:

```bash
python3 build.py
```

---

### 2. Permission errors

Run terminal as administrator (Windows)

---

### 3. Missing modules

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Notes

* This build system is a **logical bundler**, not a compiler
* It does NOT create executables yet
* Future versions may integrate PyInstaller or CMake bridge

---

## Future Upgrades

* EXE compilation (PyInstaller)
* Cross-platform packaging
* Plugin build hooks
* Live Arduino integration build step

```
```