@echo off
title GracefulOS - 1-Click Clean Uninstaller
color 0C
echo ======================================================================
echo           GracefulOS: Windows 11 Clean Uninstaller
echo ======================================================================
echo.

echo [*] Stopping any running GracefulOS processes...
powershell -Command "Get-Process -Name python,pythonw -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*graceful*' } | Stop-Process -Force -ErrorAction SilentlyContinue" >nul 2>&1

echo [*] Resetting NTFS permissions and cleaning runtime storage...
if exist runtime (
    icacls runtime /reset /t /c /q >nul 2>&1
    rmdir /s /q runtime >nul 2>&1
)

echo [*] Removing any active firewall rules...
netsh advfirewall firewall delete rule name="GracefulOS_Agent_Block" >nul 2>&1

echo.
echo ======================================================================
echo  SUCCESS: GracefulOS processes and runtime data have been removed!
echo  To finish uninstallation, simply delete this project folder.
echo ======================================================================
echo.
pause
