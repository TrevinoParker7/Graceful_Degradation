# GracefulOS: Windows 11 Onboarding & Setup Guide

Welcome to **GracefulOS**, the local-first security control plane for agentic AI on Windows 11.

This guide walks you through setting up, launching, and integrating GracefulOS on any Windows 11 machine in **under 2 minutes**.

---

## 📋 System Prerequisites

- **Operating System**: Windows 11 64-bit (Build 22000 or newer)
- **Python**: Python 3.12 or newer (tested on Python 3.14 x64)
- **Privileges**: Standard User (or Administrator for full Windows Defender Firewall enforcement)
- **Network**: 100% Offline Compatible (Zero cloud requirements)

---

## ⚡ 1-Minute Quick Start (One-Click Setup)

### Step 1: Install Dependencies
Open a PowerShell terminal in the repository root and run:
```powershell
.\install.bat
```
*(Or manually run `pip install -r requirements.txt`)*

### Step 2: Launch the Control Plane
Double-click `start.bat` or run:
```powershell
python graceful.py start
```

### Step 3: Open the Dashboard
Your default web browser will automatically open to:
👉 **[http://127.0.0.1:7777](http://127.0.0.1:7777)**

---

## 🤖 How AI Agents Connect to GracefulOS

Any AI agent (Python script, AutoGPT, CrewAI, LangChain, Cursor, or custom bot) routes its tool execution through GracefulOS instead of touching Windows directly.

### A. Python Client Example (5 Lines)
See [examples/agent_client_example.py](file:///c:/Users/Elda/projects2/Graceful_Degradation/examples/agent_client_example.py):

```python
import requests

# 1. Register the agent
requests.post("http://127.0.0.1:7777/api/v1/agents/register", json={
    "agent_id": "my-ai-coder",
    "name": "Local Coding Assistant",
    "mission": "Refactor codebase",
    "model": "local-qwen"
})

# 2. Execute a tool through the security gateway
response = requests.post("http://127.0.0.1:7777/api/v1/tools/invoke", json={
    "agent_id": "my-ai-coder",
    "tool_name": "read_file",
    "arguments": {"path": "README.md"}
})

print(response.json())
```

### B. Windows Named Pipe IPC (C / C++ / Rust / C#)
Connect to the local named pipe:
```text
\\.\pipe\GracefulOS
```
Send JSON-framed messages (e.g. `{"action": "evaluate_tool", "agent_id": "...", "tool_name": "..."}`).

---

## 🛡️ What GracefulOS Does Automatically

1. **Monitors Risk (0–100)**: Accumulates penalty points if the agent touches canary tripwires, generates prompt injections, or attempts forbidden shell mutations.
2. **Degrades Posture Smoothly**:
   - **`NORMAL` (0–29.9)**: Full developer capabilities.
   - **`WATCH` (30–49.9)**: Heightened audit logging.
   - **`RESTRICTED` (50–69.9)**: Mutating PowerShell & open network disabled.
   - **`READ_ONLY` (70–84.9)**: Workspace filesystem locked via NTFS ACLs.
   - **`ISOLATED` (85–94.9)**: All outbound network blocked via Windows Firewall.
   - **`CONTAINED` (95–100)**: Synchronous Win32 Job Object process tree kill switch (`TerminateJobObject`).
3. **Cryptographic Blockchain**: All events are hashed with SHA-256 and chained into `runtime/data/gracefulos.db`.

---

## 🛠️ Common CLI Commands

| Task | Command |
|---|---|
| **Start Service** | `python graceful.py start` |
| **Run Flagship Attack Demo** | `python graceful.py attack-demo` |
| **Verify Blockchain Ledger** | `python graceful.py verify-ledger` |
| **Run Full 76-Section QA Test** | `python scripts/plan_full_traceability_qa.py` |
| **Run Win32 OS Kernel QA Test** | `python scripts/qa_real_windows_enforcement.py` |
| **Run Real MCP QA Test** | `python scripts/qa_real_mcp_test.py` |
| **Run All Pytest Suites** | `python -m pytest tests/ -v` |

---

## 🛑 How to Release an Agent from Containment

If an agent was contained and an administrator approves releasing it:
1. Go to the dashboard: **[http://127.0.0.1:7777](http://127.0.0.1:7777)**.
2. Click the **`🛠️ Settings & Tripwires`** tab.
3. Type the Agent ID in the **Administrator Containment Release** box.
4. Click **`Authorize Release`**.

Or via CLI / REST:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:7777/api/v1/recovery/release" -Method Post -Body (@{
    agent_id = "agent-coder-001"
    admin_token = "ADMIN_LOCAL_SECRET_KEY"
    target_state = "WATCH"
    notes = "Approved after manual review"
} | ConvertTo-Json) -ContentType "application/json"
```
