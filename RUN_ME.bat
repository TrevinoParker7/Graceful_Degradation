@echo off
title GracefulOS - 1-Click All-in-One Launcher
color 0B
echo ======================================================================
echo           GracefulOS: Windows 11 1-Click Setup & Launch
echo ======================================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH!
    echo Opening Python download page...
    start https://www.python.org/downloads/
    echo.
    echo Please install Python and check the box: "Add python.exe to PATH"
    pause
    exit /b 1
)

:: 2. Install Requirements (if needed)
echo [*] Checking dependencies...
pip install -q -r requirements.txt

:: 3. Initialize Storage & Canaries
python -c "
from pathlib import Path
from brokers.filesystem.canary import canary_manager
for d in ['runtime/data', 'runtime/logs', 'runtime/incidents', 'runtime/snapshots', 'runtime/canary']:
    Path(d).mkdir(parents=True, exist_ok=True)
canary_manager.seed_canaries()
" >nul 2>&1

:: 4. Launch Browser Automatically in 2 Seconds
start "" powershell -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:7777'"

:: 5. Start GracefulOS Control Plane
echo [*] Launching GracefulOS Dashboard on http://127.0.0.1:7777 ...
echo.
echo ======================================================================
echo  GracefulOS is running! Close this window when you want to stop.
echo ======================================================================
python graceful.py start
