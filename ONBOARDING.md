# 🚀 GracefulOS: Windows 11 1-Minute Onboarding Guide

Welcome to **GracefulOS** — the local-first security control plane for agentic AI on Windows 11.

---

## ⚡ Method 1: The 1-Click Start (Easiest & Zero-Effort)

### Step 1: Get the folder onto your computer
1. On GitHub, click the green **`<> Code`** button near the top right and click **`Download ZIP`**.
2. Go to your `Downloads` folder, right-click the downloaded `.zip` file, and click **`Extract All...`**, then click **`Extract`**.
3. Open the extracted **`Graceful_Degradation`** folder.

### Step 2: Double-click `RUN_ME.bat`
1. Inside the folder, look for the file named **`RUN_ME.bat`** (or `RUN_ME`).
2. **Double-click it with your mouse** (just like opening an app or a game).

### 🪄 What Happens Automatically:
- A black window will appear for a few seconds setting up the system and dependencies.
- **Your web browser (Chrome or Edge) will automatically pop open** to the live GracefulOS Dashboard at:
  👉 **`http://127.0.0.1:7777`**

You do not need to type any terminal commands, configure databases, or download AI models!

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

## 🤖 How to Connect Any AI Agent (For Developers)

*(Note: Regular users don't need to write any code! This section is only for developers building AI programs.)*

### 🎯 What is this for? (The Problem & The Solution)
- **The Problem**: If an AI runs directly on your Windows PC with full access, a confused or hacked AI could delete your files, run dangerous PowerShell scripts, or steal passwords.
- **The GracefulOS Solution**: GracefulOS acts like a **Security Guard** standing between the AI and Windows 11. The AI must ask GracefulOS for permission before touching the computer.

```text
[ AI Agent ] ──► "Can I read this file?" ──► [ GracefulOS Security Guard ] ──► [ Windows 11 ]
                                                    │
                                     ┌──────────────┴──────────────┐
                                     ▼                             ▼
                            If SAFE: "ALLOW"              If DANGEROUS: "DENY & FREEZE"
```

---

### 🔍 Step-by-Step Code Example:

#### Step 1: The AI introduces itself to GracefulOS
```python
import requests

# The AI tells GracefulOS its name and mission
requests.post("http://127.0.0.1:7777/api/v1/agents/register", json={
    "agent_id": "my-ai-coder",
    "name": "Local Coding Assistant",
    "mission": "Write code and tests"
})
```
> **What this does**: GracefulOS creates a secure sandbox for the AI and sets its risk score to `0 / 100`.

#### Step 2: The AI asks permission to do an action (like reading a file)
```python
# The AI asks permission to read README.md
response = requests.post("http://127.0.0.1:7777/api/v1/tools/invoke", json={
    "agent_id": "my-ai-coder",
    "tool_name": "read_file",
    "arguments": {"path": "README.md"}
})

print(response.json())
```
> **What this does**: GracefulOS verifies the file is safe and returns the content: `{"success": true, "content": "..."}`.

#### Step 3: What happens if the AI tries something dangerous?
If the AI tries to run a dangerous command (like deleting folders):
```python
response = requests.post("http://127.0.0.1:7777/api/v1/tools/invoke", json={
    "agent_id": "my-ai-coder",
    "tool_name": "powershell",
    "arguments": {"command": "Remove-Item C:\\Users\\* -Recurse"}
})
```
> **What GracefulOS does**:
> 1. GracefulOS blocks the command and responds: `{"success": false, "error": "Dangerous command blocked"}`.
> 2. GracefulOS increases the AI's risk score from `0` to `50` (`RESTRICTED`).
> 3. If the AI keeps attacking, GracefulOS triggers the **emergency kill switch** (`CONTAINED`), terminating the process in the Windows kernel!

---

## 🛑 How to Turn It Off

When you are done, simply **close the black terminal window**. Everything shuts down cleanly.
