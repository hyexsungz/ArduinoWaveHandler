#!/bin/bash

echo "============================================================"
echo "                ARDUINOWAVEHANDLER FLASH TOOL"
echo "============================================================"

PORT="/dev/ttyUSB0"
FIRMWARE="firmware.hex"
MCU="atmega328p"
PROGRAMMER="arduino"
BAUD="115200"

echo "[INFO] Checking avrdude..."

if ! command -v avrdude &> /dev/null
then
    echo "[ERROR] avrdude not installed"
    exit 1
fi

if [ ! -f "$FIRMWARE" ]; then
    echo "[ERROR] firmware.hex not found"
    exit 1
fi

echo "[INFO] Using PORT: $PORT"
echo "[INFO] Flashing firmware: $FIRMWARE"

avrdude -v \
  -p $MCU \
  -c $PROGRAMMER \
  -P $PORT \
  -b $BAUD \
  -D \
  -U flash:w:$FIRMWARE:i

if [ $? -ne 0 ]; then
    echo "[ERROR] Flash failed"
    exit 1
fi

echo "============================================================"
echo "FLASH COMPLETE - DEVICE PROGRAMMED SUCCESSFULLY"
echo "============================================================"