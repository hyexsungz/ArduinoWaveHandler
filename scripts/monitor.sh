#!/bin/bash

echo "============================================================"
echo "                 ARDUINOWAVEHANDLER MONITOR"
echo "============================================================"

echo "[INFO] Checking Python..."

if ! command -v python3 &> /dev/null
then
    echo "[ERROR] python3 not found"
    exit 1
fi

echo "[INFO] Checking pyserial..."

python3 -c "import serial.tools.list_ports" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] pyserial missing (pip install pyserial)"
    exit 1
fi

echo "[INFO] Starting stable monitor loop..."
echo ""

python3 -u - << 'EOF'
import time
import serial.tools.list_ports as p

last = set()

while True:
    ports = set(x.device for x in p.comports())
    added = ports - last
    removed = last - ports

    if added or removed:
        print("\n================ PORT UPDATE ================")
        for a in added:
            print("[+] CONNECTED:", a)
        for r in removed:
            print("[-] DISCONNECTED:", r)
        print("===========================================\n")

    last = ports
    time.sleep(1)
EOF