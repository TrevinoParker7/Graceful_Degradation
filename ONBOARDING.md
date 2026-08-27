# 🚀 GracefulOS: Windows 11 1-Minute Onboarding Guide

Welcome to **GracefulOS** — the local-first security control plane for agentic AI on Windows 11.

---

## ⚡ Method 1: The 1-Click Start (Easiest)

1. **Download or clone** this repository to your Windows 11 machine.
2. **Double-click `RUN_ME.bat`**.

That's it! 
- It automatically installs all dependencies.
- It sets up all storage and security tripwires.
- It launches the control plane and **opens your browser to [http://127.0.0.1:7777](http://127.0.0.1:7777)**.

---

## 💻 Method 2: The Fast Terminal Copy-Paste

Open PowerShell or Command Prompt and paste this line:

```powershell
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git; cd Graceful_Degradation; .\RUN_ME.bat
```

---

## 🎮 How to Test and See It in Action

1. Once your browser opens to **`http://127.0.0.1:7777`**, click the **`⚡ Run Attack Demo`** button in the top-right corner.
2. Watch the live dashboard:
   - A simulated rogue AI agent attempts dangerous PowerShell commands and credential access.
   - The **Risk Score** jumps from `0` to `100 / 100`.
   - The status turns red: **`CONTAINED`**.
   - The Windows kernel terminates the process tree and locks down the filesystem.
   - Click the **`⏪ Incident Replay`** tab in the sidebar to watch the step-by-step playback!

---

## 🤖 How to Connect Any AI Agent (5 Lines of Code)

If you or a developer write a Python script or AI assistant, route its actions through GracefulOS:

```python
import requests

# 1. Register the AI agent
requests.post("http://127.0.0.1:7777/api/v1/agents/register", json={
    "agent_id": "my-ai-coder",
    "name": "Local Coding Assistant",
    "mission": "Refactor codebase",
    "model": "local-assistant"
})

# 2. Safely execute any tool through GracefulOS
response = requests.post("http://127.0.0.1:7777/api/v1/tools/invoke", json={
    "agent_id": "my-ai-coder",
    "tool_name": "read_file",
    "arguments": {"path": "README.md"}
})

print(response.json())
```

---

## 🛑 How to Turn It Off

When you are done, simply **close the black terminal window**. Everything shuts down cleanly.
