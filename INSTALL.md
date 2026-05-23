````md id="install001"
# INSTALL.md

## ArduinoWaveHandler Installation Guide

This guide explains how to set up and run the ArduinoWaveHandler framework on Windows.

---

## Requirements

### Minimum Requirements
- Windows 10/11
- Python 3.10 or higher
- 200MB free disk space

### Recommended
- Python 3.11+
- VS Code
- Git Bash or MSYS2 terminal

---

## Step 1: Install Python

Download Python:
https://www.python.org/downloads/

During installation:
- Enable "Add Python to PATH"

Verify:
```bash id="p1"
python --version
````

---

## Step 2: Download Project

### Option A: Git

```bash id="p2"
git clone https://example.com/ArduinoWaveHandler.git
cd ArduinoWaveHandler
```

### Option B: Manual

* Extract ZIP into folder
* Open terminal inside folder

---

## Step 3: Install Dependencies

This project is mostly standard library based.

Optional tools:

```bash id="p3"
pip install pyserial
```

(Only needed if Arduino serial expansion is used later)

---

## Step 4: Run System

### Main runtime

```bash id="p4"
python main.py
```

### Build system

```bash id="p5"
python build.py
```

---

## Step 5: Verify Installation

You should see:

* Console engine starting
* Logger initializing
* Device scan loop running
* COM ports being listed (if available)

---

## Troubleshooting

### Python not found

Fix PATH or use:

```bash id="p6"
python3 main.py
```

---

### No devices detected

* Check USB cable
* Install Arduino drivers (CH340 / CP210x)
* Try different COM port

---

### Build errors

Run clean build:

```bash id="p7"
python build.py
```

---

## Folder Check

Ensure structure:

```
ArduinoWaveHandler/
│
├── utils/
├── core/
├── logs/
├── dist/
├── build.py
├── main.py
```

---

## Optional Tools

### Arduino Drivers

* CH340 driver (for clones)
* CP210x driver (Silicon Labs)

---

## Run Tips

* Always run terminal as normal user first
* Use admin only if COM ports are blocked
* Keep antivirus from blocking Python scripts if needed

---

## Done

If everything works, the system is ready to monitor devices and run live logs.

```
```
