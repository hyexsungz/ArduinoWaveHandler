@echo off
setlocal enabledelayedexpansion

echo "============================================================"
echo "                ARDUINOWAVEHANDLER FLASH TOOL              "
echo "============================================================"

set PORT=COM3
set FIRMWARE=firmware.hex
set MCU=atmega328p
set PROGRAMMER=arduino
set BAUD=115200

echo [INFO] Checking avrdude...
avrdude -v >nul 2>&1
if errorlevel 1 (
    echo [ERROR] avrdude not installed or not in PATH
    pause
    exit /b 1
)

if not exist "%FIRMWARE%" (
    echo [ERROR] firmware.hex not found in current directory
    pause
    exit /b 1
)

echo [INFO] Using PORT: %PORT%
echo [INFO] Flashing firmware: %FIRMWARE%

avrdude -v ^
 -p %MCU% ^
 -c %PROGRAMMER% ^
 -P %PORT% ^
 -b %BAUD% ^
 -D ^
 -U flash:w:%FIRMWARE%:i

if errorlevel 1 (
    echo [ERROR] Flash failed
    pause
    exit /b 1
)

echo ============================================================
echo FLASH COMPLETE - DEVICE PROGRAMMED SUCCESSFULLY
echo ============================================================

pause