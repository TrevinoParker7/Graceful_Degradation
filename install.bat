@echo off
title GracefulOS - Windows 11 One-Click Installer
echo ======================================================================
echo           GracefulOS: Windows 11 Security Control Plane Setup
echo ======================================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found on your system PATH!
    echo Please install Python 3.12 or newer from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Installing Python Dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b 1
)

echo.
echo [2/3] Initializing Runtime Directories & Canary Tripwires...
python -c "
from pathlib import Path
from brokers.filesystem.canary import canary_manager
for d in ['runtime/data', 'runtime/logs', 'runtime/incidents', 'runtime/snapshots', 'runtime/canary']:
    Path(d).mkdir(parents=True, exist_ok=True)
canary_manager.seed_canaries()
print('[OK] Runtime storage initialized.')
"

echo.
echo [3/3] Running Quick Self-Test...
python -c "
from windows.job_objects.job import WindowsJobObject
j = WindowsJobObject('InitTestJob')
j.close()
print('[OK] Win32 Kernel Job Object subsystem verified.')
"

echo.
echo ======================================================================
echo   SUCCESS! GracefulOS is ready for your Windows 11 machine.
echo   To start the system, double-click 'start.bat' or run 'python graceful.py start'
echo ======================================================================
echo.
pause
