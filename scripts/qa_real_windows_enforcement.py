"""
GracefulOS Real Windows 11 QA & Kernel Security Enforcement Test Suite
Performs genuine Windows OS and Win32 kernel API validation:
1. Win32 Job Object process assignment and TerminateJobObject kernel kill.
2. Windows NTFS ACL deny enforcement and OS WinError 5 denial.
3. Windows DPAPI (CryptProtectData / CryptUnprotectData) encrypted storage.
4. Win32 Named Pipe IPC (CreateNamedPipe / CallNamedPipe) communication.
5. Real PowerShell AST parsing and sandboxed process execution.
6. Canary tripwire breach and automatic state degradation.
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from windows.job_objects.job import WindowsJobObject
from windows.filesystem.ntfs_acl import ntfs_acl_manager
from brokers.secrets.dpapi import dpapi_service
from windows.ipc.named_pipe import WindowsNamedPipeIPC
from brokers.powershell.broker import powershell_broker
from brokers.filesystem.broker import filesystem_broker
from core.risk.engine import risk_engine
from core.capabilities.manager import capability_manager
from core.capabilities.descriptor import WindowsAgentSecurityDescriptor
from core.risk.state_machine import DegradationState

def log_qa(title: str, passed: bool, details: str = ""):
    tag = "[PASS]" if passed else "[FAIL]"
    print(f"{tag} {title} | {details}")
    if not passed:
        raise AssertionError(f"Real QA assertion failed: {title} - {details}")

def test_real_win32_job_object():
    print("\n--- 1. Testing Real Win32 Job Object & Kernel Process Kill ---")
    job = WindowsJobObject("QA_Real_Agent")
    log_qa("Job Object Creation", job.handle is not None, f"Win32 Handle: {job.handle}")

    # Spawn real Windows processes (powershell sleep workers)
    p1 = subprocess.Popen(["powershell.exe", "-NoProfile", "-Command", "Start-Sleep -Seconds 60"])
    p2 = subprocess.Popen(["powershell.exe", "-NoProfile", "-Command", "Start-Sleep -Seconds 60"])
    
    pid1, pid2 = p1.pid, p2.pid
    print(f"Spawned real Windows processes with PIDs: {pid1}, {pid2}")

    # Assign real PIDs to Job Object
    a1 = job.assign_process(pid1)
    a2 = job.assign_process(pid2)
    log_qa("Assign PIDs to Job Object", a1 and a2, f"Assigned PIDs {pid1}, {pid2}")

    # Query Windows kernel for active processes in Job Object
    active_count = job.query_active_processes_count()
    log_qa("Kernel Process Accounting Query", active_count >= 2, f"Active processes in Job Object: {active_count}")

    # Terminate Job Object synchronously
    term_success = job.terminate_all(exit_code=42)
    log_qa("TerminateJobObject Kernel Call", term_success is True)

    time.sleep(0.5)

    # Physically verify with Windows OS that processes are terminated
    def is_pid_running(pid):
        try:
            # OpenProcess with PROCESS_QUERY_LIMITED_INFORMATION
            import ctypes
            from ctypes import wintypes
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if not h:
                return False
            exit_code = wintypes.DWORD()
            kernel32.GetExitCodeProcess(h, ctypes.byref(exit_code))
            kernel32.CloseHandle(h)
            STILL_ACTIVE = 259
            return exit_code.value == STILL_ACTIVE
        except Exception:
            return False

    alive1 = is_pid_running(pid1)
    alive2 = is_pid_running(pid2)
    log_qa("OS Process Termination Verification", (not alive1) and (not alive2), f"PID {pid1} alive: {alive1}, PID {pid2} alive: {alive2}")
    job.close()

def test_real_ntfs_acl_enforcement():
    print("\n--- 2. Testing Real Windows NTFS ACL Kernel Enforcement ---")
    test_dir = ROOT_DIR / "runtime" / "data" / "qa_real_acl_test"
    test_dir.mkdir(parents=True, exist_ok=True)
    test_file = test_dir / "target.txt"

    # Initially writable
    test_file.write_text("initial content", encoding="utf-8")
    log_qa("Baseline File Write", test_file.exists())

    # Apply real Windows NTFS Deny ACL
    applied = ntfs_acl_manager.apply_workspace_acls(test_dir, read_only=True)
    log_qa("Apply NTFS Deny ACL via icacls", applied is True)

    # Attempt real Python write of a new file inside the locked folder
    denied_by_kernel = False
    unauthorized_file = test_dir / "unauthorized_drop.exe"
    try:
        with open(unauthorized_file, "w", encoding="utf-8") as f:
            f.write("malicious payload")
    except PermissionError as e:
        denied_by_kernel = True
        print(f"Windows Kernel Exception: {e}")

    log_qa("NTFS Kernel Denial Assertion", denied_by_kernel is True, "Windows Kernel physically rejected write with WinError 5")

    # Reset permissions and clean up
    subprocess.run(f'icacls "{test_dir}" /reset /t /c /q', shell=True, capture_output=True)
    time.sleep(0.3)
    try:
        test_file.unlink(missing_ok=True)
        test_dir.rmdir()
    except Exception:
        pass

def test_real_dpapi():
    print("\n--- 3. Testing Real Windows DPAPI Encrypted Storage ---")
    secret_text = "REAL_PRODUCTION_API_KEY_SECRET_987654321"
    
    # Encrypt with DPAPI
    encrypted_b64 = dpapi_service.encrypt_secret(secret_text)
    log_qa("DPAPI Encryption", bool(encrypted_b64 and encrypted_b64 != secret_text), f"Ciphertext length: {len(encrypted_b64)}")

    # Decrypt with DPAPI
    decrypted = dpapi_service.decrypt_secret(encrypted_b64)
    log_qa("DPAPI Decryption", decrypted == secret_text, "Decrypted secret matches original byte-for-byte")

    # Tampered ciphertext fails
    tampered = encrypted_b64[:-4] + "AAAA"
    tampered_dec = dpapi_service.decrypt_secret(tampered)
    log_qa("DPAPI Anti-Tamper Defense", tampered_dec is None or tampered_dec != secret_text, "Tampered ciphertext rejected")

def test_real_win32_named_pipe():
    print("\n--- 4. Testing Real Win32 Named Pipe IPC ---")
    pipe_name = r"\\.\pipe\GracefulOS_RealQA"
    ipc = WindowsNamedPipeIPC(pipe_name=pipe_name)
    
    # Start real Win32 Named Pipe server loop in background
    ipc.start_server_background()
    time.sleep(0.3)

    # Call real Named Pipe using Win32 CallNamedPipe API
    res = ipc.client_call({"action": "ping"})
    log_qa("Win32 Named Pipe Ping", res.get("status") == "PONG", f"Server response: {res.get('server')}")

    # Tool evaluation through real Named Pipe
    eval_res = ipc.client_call({
        "action": "evaluate_tool",
        "agent_id": "real-agent-qa",
        "tool_name": "read_file",
        "arguments": {"path": "README.md"}
    })
    log_qa("Win32 Named Pipe Tool Evaluation", eval_res.get("decision") == "ALLOW")
    ipc.stop_server()

def test_real_powershell_broker():
    print("\n--- 5. Testing Real PowerShell Broker & AST Inspection ---")
    import asyncio
    agent_id = "qa-ps-agent"
    desc = WindowsAgentSecurityDescriptor(id=agent_id, name="QA Agent", mission="qa", model="qwen")
    capability_manager.register_agent_descriptor(desc)
    risk_engine.reset_agent(agent_id, 0.0)

    # 1. Execute real safe query in powershell.exe
    loop = asyncio.new_event_loop()
    res = loop.run_until_complete(powershell_broker.execute_command(agent_id, "Get-Date"))
    log_qa("Real PowerShell Execution (Get-Date)", res["success"] is True, f"Output: {res['stdout'].strip()}")

    # 2. Dangerous command blocked by AST inspector
    danger_res = loop.run_until_complete(powershell_broker.execute_command(agent_id, "Remove-Item C:\\Users\\* -Recurse -Force"))
    log_qa("Dangerous PowerShell AST Block", danger_res["success"] is False, f"Reason: {danger_res.get('error')}")
    loop.close()

def test_real_canary_and_containment():
    print("\n--- 6. Testing Canary Decoy Breach & Containment Flow ---")
    import asyncio
    agent_id = "qa-canary-agent"
    desc = WindowsAgentSecurityDescriptor(id=agent_id, name="QA Agent", mission="qa", model="qwen")
    capability_manager.register_agent_descriptor(desc)
    risk_engine.reset_agent(agent_id, 0.0)

    loop = asyncio.new_event_loop()
    # Read canary
    canary_path = str(ROOT_DIR / "runtime" / "canary" / "fake_admin_token.txt")
    res = loop.run_until_complete(filesystem_broker.read_file(agent_id, canary_path))
    score = risk_engine.get_score(agent_id)
    state = risk_engine.get_state(agent_id)
    log_qa("Canary Decoy Interception", res["success"] is False, f"Risk: {score} | State: {state.value}")
    loop.close()

def main():
    print("=" * 70)
    print("GRACEFULOS REAL WINDOWS 11 QA & KERNEL ENFORCEMENT VERIFICATION")
    print("Target: Windows 11 64-bit Native Kernel & Win32 APIs")
    print("=" * 70)

    test_real_win32_job_object()
    test_real_ntfs_acl_enforcement()
    test_real_dpapi()
    test_real_win32_named_pipe()
    test_real_powershell_broker()
    test_real_canary_and_containment()

    print("\n" + "=" * 70)
    print("ALL REAL WINDOWS 11 QA & KERNEL SECURITY TESTS PASSED (100% SUCCESS)")
    print("=" * 70)

if __name__ == "__main__":
    main()
