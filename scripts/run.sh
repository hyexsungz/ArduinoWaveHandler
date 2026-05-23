#!/bin/bash

echo "============================================================"
echo "               ARDUINOWAVEHANDLER RUN SYSTEM"
echo "============================================================"

ROOT="$(pwd)"

echo "[INFO] Checking Python..."

if ! command -v python3 &> /dev/null
then
    echo "[ERROR] python3 not found"
    exit 1
fi

echo "[INFO] Checking project structure..."

if [ ! -f "$ROOT/main.py" ]; then
    echo "[ERROR] main.py not found"
    exit 1
fi

echo "[INFO] Checking dependencies..."

python3 -c "import serial" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[WARN] pyserial missing - install with: pip install pyserial"
fi

echo "[INFO] Starting ARDUINOWAVEHANDLER..."
echo "------------------------------------------------------------"

python3 "$ROOT/main.py"

echo "------------------------------------------------------------"
echo "[INFO] Program exited"