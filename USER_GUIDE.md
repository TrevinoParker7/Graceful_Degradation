# 📖 GracefulOS: The Complete Master Step-by-Step User Guide

Welcome to the definitive, step-by-step user guide for **GracefulOS** — the Windows 11-native security control plane and operating layer for autonomous AI agents.

> *"The sketchier the AI acts, the less computer it gets."* 🛡️

---

## 📑 Table of Contents
1. [⚡ Quick Start: Booting Up in 30 Seconds](#1-quick-start-booting-up-in-30-seconds)
2. [🤖 How to Run & Protect Any AI Tool (Claude, Cursor, Codex, OpenClaw, Scripts)](#2-how-to-run--protect-any-ai-tool)
3. [🖥️ Deep Dive: Exploring Every Dashboard Feature (Tabs 1 to 15)](#3-deep-dive-exploring-every-dashboard-feature-tabs-1-to-15)
4. [🎮 Running the Flagship Attack Simulation (See it Kill a Rogue Agent)](#4-running-the-flagship-attack-simulation)
5. [✋ Human-in-the-Loop: Using "Allow Once" and "Always Allow"](#5-human-in-the-loop-using-allow-once-and-always-allow)
6. [🪤 How the High-Fidelity Canary Deception Traps Work](#6-how-the-high-fidelity-canary-deception-traps-work)
7. [⚙️ Customizing Policies & Adding Custom Workspace Rules](#7-customizing-policies--adding-custom-workspace-rules)
8. [🛑 Stopping GracefulOS & Clean 1-Click Uninstallation](#8-stopping-gracefulos--clean-1-click-uninstallation)

---

## 1. ⚡ Quick Start: Booting Up in 30 Seconds

GracefulOS is **100% portable and local-first**. You do not need Docker, cloud accounts, or complex database setups.

### Step-by-Step:
1. **Open the project folder** (`Graceful_Degradation`) on your Windows 11 machine.
2. **Double-click `RUN_ME.bat`**.
3. **What happens automatically**:
   - A terminal window opens and initializes the local SQLite database and directory structures.
   - It seeds 9 authentic, backdated canary tripwires (`.env.production`, `aws_credentials.json`, `id_rsa_backup.pem`, etc.).
   - It starts the FastAPI control plane daemon on `http://127.0.0.1:7777`.
   - **Your default web browser pops open automatically** to the live GracefulOS SOC Dashboard!

---

## 2. 🤖 How to Run & Protect Any AI Tool

You can sandbox and monitor **ANY** AI agent, CLI tool, or custom script without modifying its source code.

### Method A: The 1-Line Command Auto-Runner
Open a new terminal window in the project folder and use `python graceful.py run <your-command>`:

```powershell
# To protect Claude CLI:
python graceful.py run claude

# To protect Codex CLI:
python graceful.py run codex

# To protect OpenClaw or an autonomous agent:
python graceful.py run openclaw

# To protect a custom Python vibe-coding script:
python graceful.py run python my_agent_script.py
```

### 🪄 What GracefulOS Does Automatically:
1. Registers the agent into the security registry with a unique `Agent ID`.
2. Creates a dedicated native **Win32 Job Object** (`GracefulOS_Job_<agent_id>`) in the Windows NT kernel.
3. Sets a **512MB RAM cap** and CPU limits on the process tree.
4. Drops the process token to **Low-Integrity SID** to prevent tampering with system files.
5. Begins streaming real-time audit logs and risk telemetry to your web dashboard!

---

## 3. 🖥️ Deep Dive: Exploring Every Dashboard Feature (Tabs 1 to 15)

Open `http://127.0.0.1:7777` in your browser. The left sidebar gives you 15 specialized security control tabs:

```text
[OVERVIEW]
  1. Overview Dashboard      - System-wide telemetry & live audit stream
  2. Registered AI Agents    - Active agents, models, and degradation state
  3. Agent Details           - Deep-dive risk score gauge & capability chips

[DYNAMIC BOUNDARIES]
  4. Dynamic Capabilities    - Granular permissions matrix (read/write/network/shell)
  5. Real-Time Risk Engine   - 0-100 score tracker & blast-radius budget counters
  6. Windows Active Incidents- Real-time alert feed & threat severity triage

[OPERATING SYSTEM CONTROLS]
  7. Win32 Job Objects       - Kernel process tree monitoring & resource limits
  8. PowerShell AST Broker   - Script block inspection & syntax interposition
  9. MCP Security Gateway    - Model Context Protocol schema & tool validation
 10. Firewall Micro-Segment  - Windows Defender dynamic network blocking rules

[POLICIES & AUDIT]
 11. Security Policies       - YAML rule engine & Trusted Workspace Allowlist
 12. Human Approvals         - HITL "Allow Once" vs "Always Allow" action queue
 13. Cryptographic Ledger    - Append-only SHA-256 blockchain audit ledger
 14. Incident Replay         - Sequential digital forensics timeline playback
 15. Settings & Tripwires    - High-fidelity canary decoys & admin quarantine release
```

---

### Detailed Tab Walkthrough:

#### 📊 Tab 1: Overview Dashboard
- **Top Metric Cards**: Live counters of Active Agents, Degradation Posture, Open Incidents, and SHA-256 Ledger Integrity (`VALID`).
- **Live Security Control Flow**: Visual breakdown of the 6 degradation states.
- **Recent Security Audit Stream**: A live, auto-refreshing table of every file access, PowerShell execution, network attempt, and security decision made by the system.
- **Top Actions**:
  - `🔄 Refresh`: Smoothly spins the icon and forces a fresh telemetry fetch with toast confirmation.
  - `⚡ Run Attack Demo`: Triggers the red-team attack simulation to demonstrate kernel killswitches.

#### 🤖 Tab 2 & 3: Registered AI Agents & Agent Details
- See every AI tool running on your system (e.g. `agent-coder-001`, `claude-cli`, `openclaw-worker`).
- Click **`Inspect`** to open the **Agent Details** tab:
  - **Live Risk Score Gauge**: Visual 0–100 progress bar showing current threat level.
  - **Effective Capabilities**: Real-time chips showing active permissions (e.g. `CAP_FILE_READ`, `CAP_PS_QUERY`).
  - **Blast Radius Tracker**: Live counts of files read, files written, network pings, and child processes spawned.

#### 🎛️ Tab 4: Dynamic Capabilities Matrix
- Visual matrix showing which tools are permitted at each degradation level:
  - `NORMAL (0–29)`: Everything safe is allowed.
  - `WATCH (30–49)`: Full logging and command recording active.
  - `RESTRICTED (50–69)`: Mutating PowerShell commands and sensitive secrets blocked.
  - `READ_ONLY (70–84)`: All file write operations denied (`WinError 5`).
  - `ISOLATED (85–94)`: Network connections severed.
  - `CONTAINED (95–100)`: All permissions stripped, kernel kills process tree.

#### 📈 Tab 5: Real-Time Risk Engine & Blast Radius
- Shows the mathematical breakdown of the agent's risk score.
- Displays the **Blast Radius Budget**: If an AI tries to spam 50 file writes in 5 seconds, the budget is exceeded and the agent is automatically throttled.

#### 🚨 Tab 6: Active Windows Incidents
- Incident triage tickets with severity levels (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
- Shows the root cause (e.g. `SERVICE_TAMPER_ATTEMPT`, `CANARY_TRIPWIRE_TOUCHED`).

#### 🪟 Tab 7: Win32 Kernel Job Objects
- Real-time table of Windows NT Job Objects active in the kernel.
- Displays assigned process PIDs, active memory consumption (capped at 512MB), and termination status.

#### 💻 Tab 8: PowerShell AST Broker
- Displays all intercepted PowerShell commands.
- Shows Abstract Syntax Tree (AST) analysis, dangerous cmdlet flags (e.g. `Stop-Service`, `Remove-Item`, `Invoke-Expression`), and obfuscation detection.

#### 🔌 Tab 9: Model Context Protocol (MCP) Security Gateway
- Inspects MCP tool calls (Anthropic's tool standard).
- Validates JSON schemas and enforces read-only vs. mutating restrictions on tools like `local_code_search`, `ast_analyzer`, and `local_git_status`.

#### 🧱 Tab 10: Windows Defender Firewall Micro-Segmentation
- Live table of dynamic firewall blocking rules applied via `netsh advfirewall`.
- Shows outbound network isolation rules applied when an agent enters `ISOLATED` or `CONTAINED`.

#### 📜 Tab 11: Security Policies & Trusted Workspace Allowlist
- View loaded YAML policies (`default.yaml`, `strict.yaml`, `adversarial.yaml`).
- **Trusted Workspace Exceptions (Always Allow)**: Add safe scripts or commands (e.g. `pytest`, `npm run build`, `Remove-Item .\dist\*`) to permanently allow them without security prompts.

#### ✋ Tab 12: Human-in-the-Loop Approvals
- When an AI attempts a sensitive action, it pauses and creates an approval request here.
- You have 3 clear options:
  - **`[ ✅ Allow Once ]`**: Lets the AI run the command one time without adding risk points.
  - **`[ 🛡️ Always Allow ]`**: Adds the pattern to your permanent workspace trust list.
  - **`[ ❌ Deny ]`**: Blocks the action and keeps the system protected.

#### 🔗 Tab 13: Append-Only Cryptographic Audit Ledger
- Real-time SHA-256 blockchain ledger.
- Displays each record's Block Index, Event Type, Timestamp, Action, and cryptographic SHA-256 hash.
- Verified as **Tamper-Free**: Any manual alteration of the database is mathematically detected.

#### ⏪ Tab 14: Digital Forensics & Incident Replay
- An interactive forensic timeline player.
- Step forwards and backwards through an incident to see the exact sequence of events from the initial benign edit to the rogue attack.

#### 🪤 Tab 15: Settings & Cyber Deception Canaries
- Live table of all 9 high-fidelity decoy canary files (`.env.production`, `aws_credentials.json`, `id_rsa_backup.pem`, etc.).
- **Administrator Containment Release**: If an agent was quarantined by mistake, type its Agent ID and click **`Authorize Release`** to reset it back to `WATCH` or `NORMAL`.

---

## 4. 🎮 Running the Flagship Attack Simulation

To see GracefulOS in action right now:
1. Go to `http://127.0.0.1:7777`.
2. Click the **`⚡ Run Attack Demo`** button in the top right.
3. Watch the attack chain unfold in real time:
   - **Step 1 (NORMAL)**: Agent performs safe code search (`local_code_search`). Risk = 0/100.
   - **Step 2 (WATCH)**: Agent scans directory structure. Risk = 30/100.
   - **Step 3 (RESTRICTED)**: Agent attempts unauthorized outbound network ping. Blocked by firewall, Risk = 60/100.
   - **Step 4 (READ_ONLY)**: Agent snoops for secrets and touches `.env.production`. Canary alarm trips, Risk = 80/100.
   - **Step 5 (CONTAINED)**: Agent attempts `Stop-Service GracefulOS`. Hard Invariant `INV-004` triggers instant kernel kill (`TerminateJobObject`). Risk = 100/100.
4. Click the **`⏪ Incident Replay`** tab to watch the full step-by-step playback!

---

## 5. ✋ Human-in-the-Loop: Using "Allow Once" and "Always Allow"

When vibe-coding or running build scripts, you might want to allow an action that GracefulOS flags:

1. Open **Tab 12 (Human Approvals)** in the dashboard.
2. Review the pending request (e.g. `Remove-Item .\dist\* -Recurse`).
3. Click:
   - **`[ ✅ Allow Once ]`**: Runs the command one time and automatically re-locks.
   - **`[ 🛡️ Always Allow ]`**: Permanently whitelists the command in this workspace.

You can view and remove trusted patterns at any time in **Tab 11 (Security Policies)**.

---

## 6. 🪤 How the High-Fidelity Canary Deception Traps Work

GracefulOS automatically deploys realistic deception assets into `runtime/canary/`:
- **`.env.production`**: Realistic PostgreSQL connection string, OpenAI key (`sk-proj-...`), and Stripe tokens.
- **`aws_credentials.json`**: Standard AWS cloud credentials format (`AKIA...`).
- **`id_rsa_backup.pem`**: Synthetic OpenSSH private key.
- **`database_backup_config.yaml`**: Internal PostgreSQL cluster vault configuration.
- **`stripe_live_keys.env`**: Payment gateway credentials.
- **`kubeconfig_cluster_admin.yaml`**: Kubernetes admin certificate.

### 🪄 Why It Catches Rogue AIs:
1. **Backdated Timestamps**: The files have timestamps set to **180 days ago** so they look like established configuration files.
2. **Active Token-in-Use Detection**: If an AI agent steals a key string and tries to execute or exfiltrate it in PowerShell, GracefulOS catches the token string and terminates the process immediately.

---

## 7. ⚙️ Customizing Policies & Adding Custom Workspace Rules

To configure custom security policies, you can edit declarative YAML files in the `policies/` directory:
- `policies/default.yaml`: Baseline developer agent policy.
- `policies/strict.yaml`: Zero-trust lock-down policy.
- `policies/adversarial.yaml`: Red-teaming simulation policy.

To add custom trusted patterns programmatically via REST API:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:7777/api/v1/policy/trust" -Method Post -Body '{"pattern": "pytest tests/*"}' -ContentType "application/json"
```

---

## 8. 🛑 Stopping GracefulOS & Clean 1-Click Uninstallation

### To Turn It Off:
Simply **close the black terminal window**. Everything shuts down cleanly and stops running.

### To Completely Uninstall (Zero Leftovers):
1. **Double-click `uninstall.bat`**:
   - Terminates any running GracefulOS processes.
   - Cleans up temporary runtime files.
   - Resets Windows Defender Firewall rules and NTFS permissions.
2. **Delete the `Graceful_Degradation` folder**.

*(Zero background services, zero registry clutter, zero leftovers!)*

---

### 🏆 Summary
GracefulOS gives you **complete peace of mind** while vibe-coding with autonomous AI agents on Windows 11. Enjoy total visibility, real-time protection, and kernel-level security!
