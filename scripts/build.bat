@echo off
setlocal enabledelayedexpansion

echo "============================================================"
echo "             ARDUINOWAVEHANDLER BUILD TOOL                  "
echo "============================================================"

set ROOT=%cd%
set SRC=%ROOT%
set OUT=%ROOT%\dist

if not exist "%OUT%" (
    mkdir "%OUT%"
)

echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH
    pause
    exit /b 1
)

echo [INFO] Cleaning old build...
if exist "%OUT%\*" del /q "%OUT%\*" >nul 2>&1

echo [INFO] Collecting project files...

for /r "%SRC%" %%f in (*.py) do (
    set FILE=%%f
    set FILE=!FILE:%SRC%\=!
    echo [ADD] !FILE!
)

echo [INFO] Running syntax check...
for /r "%SRC%" %%f in (*.py) do (
    python -m py_compile "%%f"
    if errorlevel 1 (
        echo [FAIL] Syntax error in %%f
        pause
        exit /b 1
    )
)

echo [INFO] Creating package index...
set INDEX=%OUT%\index.txt
echo NORTHBRIDGE SYSTEMS PACKAGE > "%INDEX%"
echo BUILD TIME: %date% %time% >> "%INDEX%"
echo ============================== >> "%INDEX%"

for /r "%SRC%" %%f in (*.py) do (
    set FILE=%%f
    set FILE=!FILE:%SRC%\=!
    echo !FILE! >> "%INDEX%"
)

echo [INFO] Copying files...
xcopy "%SRC%\*.py" "%OUT%" /s /y >nul 2>&1

echo [INFO] Build complete
echo Output: %OUT%

echo ============================================================
pause