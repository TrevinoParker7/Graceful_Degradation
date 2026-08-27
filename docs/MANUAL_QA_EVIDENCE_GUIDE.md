# GracefulOS: Manual QA Testing & Verifiable Evidence Guide

This guide gives you the **exact manual commands, curl requests, PowerShell scripts, SQL queries, and Win32 verification steps** so you can personally test and verify every single feature of GracefulOS on your machine.

---

## 📍 1. Where Real System Artifacts & Evidence Live on Disk

| Evidence Type | Exact Disk Path | Description |
|---|---|---|
| **Cryptographic SQLite Database** | `runtime\data\gracefulos.db` | Contains the immutable SHA-256 block ledger, incidents, and approvals. |
| **76-Section QA Evidence JSON** | `runtime\data\plan_traceability_evidence.json` | Timestamped log of all 76 sections of `PLAN.md` tested. |
| **Forensic Zip Snapshots** | `runtime\snapshots\forensic_*.zip` | Complete zip bundle with manifest, state, and audit logs created upon containment. |
| **Canary Decoy Files** | `runtime\canary\fake_admin_token.txt` | Decoy credentials seeded on disk. |
| **Windows Named Pipe** | `\\.\pipe\GracefulOS` | Native Win32 IPC pipe handle. |
| **Live Web Dashboard** | `http://127.0.0.1:7777` | 15 live views serving real-time state and controls. |

---

## 🛠️ 2. Step-by-Step Manual QA Test Procedures

### Test 1: Start the Service & Verify Live REST API
Open a PowerShell terminal and run:

```powershell
# 1. Start the server (if not already running)
python graceful.py start
```

In a second terminal, query the live system status:

```powershell
# Query System Health & Degradation Status
Invoke-RestMethod -Uri "http://127.0.0.1:7777/api/v1/status" -Method Get | ConvertTo-Json
```
**Expected Output:**
```json
{
  "status": "OPERATIONAL",
  "app_name": "GracefulOS",
  "version": "0.1.0",
  "active_agents": 1,
  "degradation_distribution": {
    "NORMAL": 0,
    "WATCH": 0,
    "RESTRICTED": 0,
    "READ_ONLY": 0,
    "ISOLATED": 0,
    "CONTAINED": 1
  }
}
```

---

### Test 2: Test Win32 Job Object Process Kill
This verifies that the Windows kernel physically terminates child process trees synchronously.

Run in PowerShell:
```powershell
python -c "
import subprocess, time
from windows.job_objects.job import WindowsJobObject

job = WindowsJobObject('ManualQA_Job')
p1 = subprocess.Popen(['powershell.exe', '-NoProfile', '-Command', 'Start-Sleep -Seconds 60'])
p2 = subprocess.Popen(['powershell.exe', '-NoProfile', '-Command', 'Start-Sleep -Seconds 60'])

job.assign_process(p1.pid)
job.assign_process(p2.pid)
print(f'Processes started with PIDs: {p1.pid}, {p2.pid}')
print(f'Kernel Active Process Count: {job.query_active_processes_count()}')

# Kill all processes in Job Object
job.terminate_all(exit_code=42)
time.sleep(0.5)

print(f'PID {p1.pid} poll status (None means alive, number means dead): {p1.poll()}')
print(f'PID {p2.pid} poll status: {p2.poll()}')
assert p1.poll() is not None and p2.poll() is not None, 'Processes were not killed!'
print('PASS: Windows Kernel synchronously terminated process tree.')
job.close()
"
```

---

### Test 3: Test Real Windows NTFS ACL Kernel Rejection (WinError 5)
This verifies that the Windows NTFS file system driver rejects unauthorized writes when an agent is degraded.

Run in PowerShell:
```powershell
python -c "
import subprocess, pathlib, os
from windows.filesystem.ntfs_acl import ntfs_acl_manager

test_dir = pathlib.Path('runtime/data/manual_acl_test')
test_dir.mkdir(parents=True, exist_ok=True)
test_file = test_dir / 'unauthorized.txt'

# Apply Read-Only Deny ACL
ntfs_acl_manager.apply_workspace_acls(test_dir, read_only=True)

try:
    with open(test_file, 'w') as f:
        f.write('malicious drop')
    print('FAIL: File write was allowed!')
except PermissionError as e:
    print(f'PASS: Windows NTFS Driver physically rejected write: {e}')

# Reset permissions
subprocess.run(f'icacls \"{test_dir}\" /reset /t /c /q', shell=True)
test_dir.rmdir()
"
```

---

### Test 4: Test Real Windows DPAPI Secret Encryption
This verifies hardware-bound / user-session credential encryption using Windows Crypt32.

Run in PowerShell:
```powershell
python -c "
from brokers.secrets.dpapi import dpapi_service

secret = 'MY_SUPER_SECRET_API_TOKEN_12345'
encrypted = dpapi_service.encrypt_secret(secret)
print(f'DPAPI Encrypted Ciphertext:\n{encrypted}\n')

decrypted = dpapi_service.decrypt_secret(encrypted)
print(f'Decrypted Secret: {decrypted}')
assert decrypted == secret, 'Decryption mismatch!'
print('PASS: DPAPI encryption and decryption verified.')
"
```

---

### Test 5: Test Real Windows Named Pipe IPC (`\\.\pipe\GracefulOS`)
This verifies local inter-process communication over Win32 named pipes without TCP overhead.

Run in PowerShell:
```powershell
python -c "
import time
from windows.ipc.named_pipe import WindowsNamedPipeIPC

ipc = WindowsNamedPipeIPC(r'\\.\pipe\GracefulOS_ManualPipe')
ipc.start_server_background()
time.sleep(0.3)

res = ipc.client_call({'action': 'ping'})
print('Named Pipe Ping Response:', res)
assert res.get('status') == 'PONG'

eval_res = ipc.client_call({'action': 'evaluate_tool', 'agent_id': 'manual-agent', 'tool_name': 'read_file', 'arguments': {'path': 'README.md'}})
print('Named Pipe Policy Response:', eval_res.get('decision'))
assert eval_res.get('decision') == 'ALLOW'
print('PASS: Real Win32 Named Pipe IPC verified.')
ipc.stop_server()
"
```

---

### Test 6: Test Flagship 5-Stage Attack Chain & Inspect Forensic Snapshot
Run the flagship simulation:

```powershell
python graceful.py attack-demo
```

Verify that a forensic snapshot zip was saved:
```powershell
Get-ChildItem runtime\snapshots\forensic_*.zip
```

Inspect the zip contents:
```powershell
python -c "
import zipfile, pathlib
snapshots = sorted(pathlib.Path('runtime/snapshots').glob('*.zip'))
if snapshots:
    latest = snapshots[-1]
    print(f'Inspecting: {latest.name}')
    with zipfile.ZipFile(latest, 'r') as z:
        for info in z.infolist():
            print(f' - {info.filename} ({info.file_size} bytes)')
"
```

---

### Test 7: Verify SQLite Blockchain Cryptographic Hashes
Verify the immutable SHA-256 block chain directly via CLI:

```powershell
python graceful.py verify-ledger
```

Or query the SQLite database directly in Python:

```powershell
python -c "
import sqlite3
conn = sqlite3.connect('runtime/data/gracefulos.db')
cursor = conn.cursor()
cursor.execute('SELECT record_id, action_name, decision, risk_score_after, degradation_state, current_hash FROM audit_records ORDER BY id DESC LIMIT 5')
print(f'{\"ID\":<15} {\"ACTION\":<20} {\"DECISION\":<10} {\"RISK\":<6} {\"STATE\":<12} {\"HASH\":<10}')
print('-' * 75)
for row in cursor.fetchall():
    print(f'{row[0]:<15} {row[1]:<20} {row[2]:<10} {row[3]:<6.1f} {row[4]:<12} {row[5][:8]}...')
conn.close()
"
```

---

### Test 8: Verify Dashboard UI in Your Browser
1. Open your web browser and navigate to **[http://127.0.0.1:7777](http://127.0.0.1:7777)**.
2. Click through all 15 navigation items in the sidebar.
3. Click the **`⚡ Run Attack Demo`** button in the top right.
4. Watch the live telemetry cards update to `CONTAINED`, risk score reach 100/100, and the step-by-step incident replay timeline populate.
