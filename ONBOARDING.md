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

## 🤖 How to Protect Any AI Script (100% Automatic — No Code Changes!)

You do **NOT** have to modify your AI code or configure API calls! You can run and sandbox ANY Python script or AI program automatically:

```powershell
python graceful.py run python my_ai_script.py
```

### 🪄 What happens automatically:
1. GracefulOS automatically registers your AI agent in the security control plane.
2. GracefulOS automatically binds the process to a native **Windows 11 Job Object**.
3. It sets memory limits, tracks CPU, and enables the emergency kill-switch.
4. Your script runs normally, and you can watch it live on the dashboard at `http://127.0.0.1:7777`!

---

## 🛠️ Advanced: Direct REST API (For Custom Integrations)

If you want your custom AI agent to talk directly to GracefulOS over HTTP:

```python
import requests

# 1. Register the AI agent
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
