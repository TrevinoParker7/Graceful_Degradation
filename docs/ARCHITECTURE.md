# GracefulOS Architecture Specification

## 1. System Topology

```text
┌─────────────────────────────────────────────────────────────┐
│                      TRUSTED CONTROL PLANE                  │
│                                                             │
│  GracefulOS Windows Core Service (GracefulOSCore / Python)  │
│  ├── Gateway API (127.0.0.1:7777 / \\.\pipe\GracefulOS)     │
│  ├── Local Event Bus (asyncio priority queue)               │
│  ├── Risk Engine (0-100 score, signal accumulator, decay)   │
│  ├── Policy Engine (Declarative YAML rules & invariants)    │
│  ├── Dynamic Capability Manager (WASD permission matrix)    │
│  ├── Audit Ledger (Append-only SHA-256 SQLite ledger)       │
│  └── Recovery & Incident Manager (Forensic snapshots)       │
└──────────────────────────────┬──────────────────────────────┘
                               │ Dispatches to
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     TOOL & PROCESS BROKERS                  │
│                                                             │
│  ├── PowerShell Broker (AST parsing, syntax classification) │
│  ├── Process Broker (Allowlists, tracking, containment)     │
│  ├── Filesystem Broker (Workspace sandbox, path guards)     │
│  ├── Network Broker (Firewall sync, allowlist filters)      │
│  ├── MCP Broker (Schema validator, tool permits)            │
│  ├── Browser Broker (Read-only vs mutation permits)         │
│  └── Secret Broker (DPAPI / ephemeral token dispenser)      │
└──────────────────────────────┬──────────────────────────────┘
                               │ Enforces via
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 WINDOWS 11 ENFORCEMENT STACK                │
│                                                             │
│  ├── Win32 Job Objects (Process grouping, CPU/RAM caps)     │
│  ├── Restricted Access Tokens (Low integrity, stripped SIDs)│
│  ├── AppContainer Profiles                                  │
│  ├── NTFS Access Control Lists (ACLs)                       │
│  ├── Windows Defender Firewall / WFP                        │
│  └── Event Tracing for Windows (ETW) Telemetry              │
└──────────────────────────────┬──────────────────────────────┘
                               │ Controls
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    UNTRUSTED DATA PLANE                     │
│                                                             │
│  ├── Autonomous AI Agents (Python / Node / CLI)             │
│  ├── Local LLMs (Ollama / LM Studio / llama.cpp / Qwen)     │
│  └── Untrusted Inputs (Prompts, Web Content, Tool Outputs)  │
└─────────────────────────────────────────────────────────────┘
```

## 2. Control Plane vs. Data Plane Separation
- **Trusted Control Plane**: Houses risk calculations, invariant checks, database writes, and process termination routines. Agent processes run with non-elevated tokens and cannot write to `C:\ProgramData\GracefulOS\` or control plane memory.
- **Untrusted Data Plane**: Houses the agent and model runtimes. Requests are mediated through the Gateway before reaching tool brokers.

## 3. Communication Channels
- **Local IPC**: Windows Named Pipes (`\\.\pipe\GracefulOS`) for high-speed local RPC.
- **REST / WebSockets**: `http://127.0.0.1:7777` providing programmatic endpoints and real-time dashboard telemetry.
- **Database**: Local SQLite database at `runtime/data/gracefulos.db` (or `C:\ProgramData\GracefulOS\data\gracefulos.db`).
