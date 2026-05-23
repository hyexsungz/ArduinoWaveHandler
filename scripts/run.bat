@echo off
setlocal enabledelayedexpansion
title ARDUINOWAVEHANDLER RUNNER

echo "============================================================"
echo "               ARDUINOWAVEHANDLER RUN SYSTEM"
echo "============================================================"

set ROOT=%cd%

echo "[INFO] Checking Python..."
python --version >nul 2>&1
if errorlevel 1 (
    echo "[ERROR] Python not found in PATH"
    pause
    exit /b 1
)

echo "[INFO] Checking project structure..."

if not exist "%ROOT%\main.py" (
    echo "[ERROR] main.py not found"
    pause
    exit /b 1
)

echo "[INFO] Checking dependencies..."
python -c "import serial" >nul 2>&1
if errorlevel 1 (
    echo "[WARN] pyserial missing - install with: pip install pyserial"
)

echo "[INFO] Starting ARDUINOWAVEHANDLER..."
echo "------------------------------------------------------------"

python "%ROOT%\main.py"

echo "------------------------------------------------------------"
echo "[INFO] Program exited"
pause