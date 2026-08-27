@echo off
title GracefulOS Control Plane Daemon
echo ======================================================================
echo           GracefulOS: Starting Control Plane on http://127.0.0.1:7777
echo ======================================================================
echo.

:: Launch browser in background after 2 seconds
start "" powershell -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:7777'"

:: Start GracefulOS
python graceful.py start
pause
