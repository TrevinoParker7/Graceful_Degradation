# GracefulOS 1-Line PowerShell Setup & Launch Script
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "          GracefulOS: Windows 11 Automated Setup & Launch             " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Python is not installed or not in PATH." -ForegroundColor Red
    Start-Process "https://www.python.org/downloads/"
    Write-Host "Please install Python 3.12+ with 'Add python.exe to PATH' checked." -ForegroundColor Yellow
    exit 1
}

# 2. Install dependencies
Write-Host "[*] Installing Python dependencies..." -ForegroundColor Green
pip install -q -r requirements.txt

# 3. Seed runtime storage
python -c "
from pathlib import Path
from windows.filesystem.canary import canary_manager
for d in ['runtime/data', 'runtime/logs', 'runtime/incidents', 'runtime/snapshots', 'runtime/canary']:
    Path(d).mkdir(parents=True, exist_ok=True)
canary_manager.seed_canary_files()
"

# 4. Open browser
Start-Job -ScriptBlock { Start-Sleep -Seconds 2; Start-Process "http://127.0.0.1:7777" } | Out-Null

# 5. Start Control Plane
Write-Host "[*] Starting GracefulOS Control Plane on http://127.0.0.1:7777 ..." -ForegroundColor Green
python graceful.py start
