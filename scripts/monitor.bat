@echo off
setlocal enabledelayedexpansion
title ARDUINOWAVEHANDLER MONITOR

echo "============================================================"
echo "                 ARDUINOWAVEHANDLER MONITOR"
echo "============================================================"

echo "[INFO] Checking Python..."
python --version >nul 2>&1
if errorlevel 1 (
    echo "[ERROR] Python not found"
    pause
    exit /b 1
)

echo "[INFO] Checking pyserial..."
python -c "import serial.tools.list_ports" >nul 2>&1
if errorlevel 1 (
    echo "[ERROR] pyserial missing (pip install pyserial)"
    pause
    exit /b 1
)

echo "[INFO] Starting stable monitor loop..."
echo " "

python -u -c "import time,serial.tools.list_ports as p; last=set()
while True:
    ports=set(x.device for x in p.comports())
    added=ports-last
    removed=last-ports

    if added or removed:
        print('\n================ PORT UPDATE ================')
        for a in added:
            print('[+] CONNECTED:', a)
        for r in removed:
            print('[-] DISCONNECTED:', r)
        print('===========================================\n')

    last=ports
    time.sleep(1)"