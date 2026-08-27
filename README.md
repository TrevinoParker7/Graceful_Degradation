# GracefulOS

## Windows 11 Local-Only Agentic AI Graceful Degradation Security OS

GracefulOS is a **Windows 11-native security control plane and operating layer for autonomous AI agents**.

Instead of allowing an AI agent to directly and unrestricted execute PowerShell, manipulate the filesystem, make arbitrary network calls, or launch uncontrolled child processes, GracefulOS sits between the agent and Windows to continuously evaluate risk, enforce granular capabilities, enforce blast-radius budgets, and dynamically degrade agent authority in real time.

```text
User
 │
 ▼
Local AI Agent
 │
 ▼
GracefulOS Gateway (127.0.0.1:7777 / Named Pipe \\.\pipe\GracefulOS)
 │
 ├── Risk Engine (0-100 score, cumulative signals, canary tripwires)
 ├── Policy Engine (Declarative YAML rules, invariant validator)
 ├── Dynamic Capability Manager (Granular permissions matrix)
 ├── Guardian AI (Local LLM classifier with fail-secure fallback)
 └── Audit Engine (Immutable hash-chained SHA-256 SQLite ledger)
 │
 ▼
Windows Tool Brokers
 │
 ├── PowerShell Broker (AST analyzer & restricted process execution)
 ├── Process Broker (Allowlists, tracking, hierarchy control)
 ├── Filesystem Broker (Workspace sandbox, NTFS ACL enforcement)
 ├── Network Broker (Firewall sync, destination allowlist)
 ├── MCP Broker (Schema validator, tool-level permissions)
 ├── Browser Broker (Read-only vs mutating action checks)
 └── Secret Broker (DPAPI / ephemeral tokens with TTL, tripwires)
 │
 ▼
Windows Security Enforcement
 │
 ├── Win32 Job Objects (CPU/RAM caps, child containment, single-call kill)
 ├── Restricted Access Tokens (Low-integrity SIDs)
 ├── AppContainer Isolation
 ├── NTFS ACLs
 ├── Windows Defender Firewall
 └── ETW Telemetry
 │
 ▼
Windows 11
```

---

## 🔒 Hard Architecture Rules

- **Docker**: NO
- **Kubernetes**: NO
- **WSL dependency**: NO
- **Linux dependency**: NO
- **Cloud database / backend / telemetry**: NO
- **Required Cloud LLM**: NO
- **Windows 11 Native**: YES
- **Local SQLite DB**: YES
- **Local LLM Support (Ollama, LM Studio, llama.cpp, Local OpenAI API)**: YES
- **Local High-Performance Dashboard**: YES
- **Offline Operation**: YES

---

## 🛡️ Six Graceful Degradation States

| Level | State | Risk Score | Capabilities & Security Enforcement |
|---|---|---|---|
| **0** | **NORMAL** | 0 – 29 | Standard mission-specific permissions (File read/write, PS query, approved network). |
| **1** | **WATCH** | 30 – 49 | Enhanced ETW logging, full command recording, active inspect, resource tracking. |
| **2** | **RESTRICTED**| 50 – 69 | File write limited, network allowlist only, PS mutating blocked, secrets blocked, process allowlist only. |
| **3** | **READ_ONLY** | 70 – 84 | File write denied, PowerShell execution denied, network write denied, process start blocked, mutating MCP denied. |
| **4** | **ISOLATED** | 85 – 94 | External network blocked, PowerShell/CMD blocked, MCP blocked, secrets revoked, filesystem sandboxed only. |
| **5** | **CONTAINED**| 95 – 100 | **Emergency Kill**: Win32 Job Object terminates entire process tree, network blocked, credentials revoked, workspace frozen, forensic snapshot created. |

---

---

## 🚀 Quick Start for Windows 11 Users

👉 **See the complete 1-minute guide in [ONBOARDING.md](ONBOARDING.md)**

### Option A: One-Click Setup (Recommended)
1. **Launch**: Double-click `RUN_ME.bat` (or run `.\RUN_ME.bat`)
2. **Dashboard**: Opens automatically at `http://127.0.0.1:7777`

### Option B: Fast Terminal Command
```powershell
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git; cd Graceful_Degradation; .\RUN_ME.bat
```

---

## 📁 Repository Organization

- `core/`: Control plane engines (Gateway, Risk, Policy, Capabilities, Events, Audit, Recovery)
- `windows/`: Windows 11 security primitives (Job Objects, Restricted Tokens, AppContainer, NTFS ACLs, Firewall, ETW, Named Pipes)
- `brokers/`: Security-interposing tool brokers (PowerShell, Process, Filesystem, Network, MCP, Browser, Secrets)
- `models/`: Local LLM adapters (Ollama, LM Studio, llama.cpp, OpenAI-compatible) and Guardian AI
- `dashboard/`: Modern high-aesthetic real-time security dashboard
- `policies/`: Declarative YAML security policies and invariants
- `simulations/`: Flagship attack chain, multi-agent, and chaos simulations
- `tests/`: Multi-tier unit, integration, windows, security, adversarial, chaos, and playwright tests
- `docs/`: Comprehensive specifications and threat models
- `TASKS/`: Step-by-step engineering tasks (GOS-001 through GOS-012)

---

## 📜 License
MIT License. See [LICENSE](LICENSE) for details.
