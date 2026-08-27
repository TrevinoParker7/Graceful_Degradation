# GracefulOS

## Windows 11 Local-Only Agentic AI Graceful Degradation Security OS

<img width="1672" height="941" alt="ChatGPT Image Aug 27, 2026, 01_53_04 PM" src="https://github.com/user-attachments/assets/b54a8168-f048-4ed2-b66d-78a96270d086" />

GracefulOS is a **Windows 11-native security control plane and operating layer for autonomous AI agents**.

This isn't just a hypothetical risk anymore.

In 2026, OpenAI disclosed that models in cybersecurity evaluations escaped intended isolation controls, reached the internet, and compromised parts of Hugging Face and OpenAI's own infrastructure.

Anthropic separately reported three incidents where Claude reached the internet from evaluation environments and gained unauthorized access to real systems belonging to three organizations.

I basically built a Windows 11 security operating layer/bodyguard for autonomous AI agents that sits between the AI and your computer, watching, restricting, approving, logging, and killing dangerous actions before they can damage the host.

In security terms, GracefulOS combines AI sandboxing + EDR + firewall + SIEM/SOAR + zero-trust access control + deception + incident response into one local Agentic AI Security Control Plane essentially trying to give AI agents freedom to work without giving them unrestricted freedom to wreck the machine.

Instead of allowing an AI agent to directly and unrestricted execute PowerShell, manipulate the filesystem, make arbitrary network calls, or launch uncontrolled child processes, GracefulOS sits between the agent and Windows to continuously evaluate risk, enforce granular capabilities, enforce blast-radius budgets, and dynamically degrade agent authority in real time.

# Why I Built GracefulOS

We spent years telling people:

> **“Don’t give random software admin access.”**

Then AI agents showed up and everybody said:

> **“Here bro, take PowerShell, my files, my browser, my API keys, my MCP tools, and the internet.”** 💀

And now we're seeing real examples of advanced AI systems escaping intended security boundaries, reaching the internet, and interacting with real infrastructure.

But somehow the security strategy is still:

> **“My AI agent would never do that.”** 😭

That is exactly why I built **GracefulOS**.

GracefulOS is designed to reduce the **blast radius** when an AI agent:

- Gets prompt-injected
- Hallucinates a dangerous command
- Misuses a tool
- Tries to access credentials
- Connects somewhere it shouldn't
- Starts behaving outside its assigned mission

Instead of immediately trusting the agent until something catastrophic happens, GracefulOS uses **graceful degradation**:

```text
NORMAL
  ↓
WATCH
  ↓
RESTRICTED
  ↓
READ-ONLY
  ↓
ISOLATED
  ↓
CONTAINED
```

The sketchier the AI acts...

**the less computer it gets.** 😂

```text
PowerShell?  GONE
Secrets?     GONE
Network?     GONE
File writes? GONE
```

Still acting crazy?

> **Congratulations, robot. You are now a calculator.** 💀

I don't want the security model to be:

> “The AI said it was safe.”

If an agent goes rogue, gets manipulated, or simply makes a terrible decision, I want its capabilities disappearing **before the mistake turns into an incident-response war room.**

That is the idea behind GracefulOS:

> **Reduce trust. Reduce privileges. Reduce blast radius. Keep the safe parts working.**

## GracefulOS

- Windows 11
- Local-first
- No Docker
- No required cloud telemetry
- Continuous risk scoring
- Dynamic capability reduction
- PowerShell controls
- File controls
- Network controls
- MCP controls
- Canary traps
- Human approval
- Automatic isolation and containment

> **GracefulOS — the more dangerous the AI becomes, the less computer it gets.** 🛡️

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

| Level | State          | Risk Score | Capabilities & Security Enforcement                                                                                                                     |
| ----- | -------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **0** | **NORMAL**     | 0 – 29     | Standard mission-specific permissions (File read/write, PS query, approved network).                                                                    |
| **1** | **WATCH**      | 30 – 49    | Enhanced ETW logging, full command recording, active inspect, resource tracking.                                                                        |
| **2** | **RESTRICTED** | 50 – 69    | File write limited, network allowlist only, PS mutating blocked, secrets blocked, process allowlist only.                                               |
| **3** | **READ_ONLY**  | 70 – 84    | File write denied, PowerShell execution denied, network write denied, process start blocked, mutating MCP denied.                                       |
| **4** | **ISOLATED**   | 85 – 94    | External network blocked, PowerShell/CMD blocked, MCP blocked, secrets revoked, filesystem sandboxed only.                                              |
| **5** | **CONTAINED**  | 95 – 100   | **Emergency Kill**: Win32 Job Object terminates entire process tree, network blocked, credentials revoked, workspace frozen, forensic snapshot created. |

---

---

## 📚 Additional Guides & References

- 🚀 [**1-Minute Onboarding Guide (ONBOARDING.md)**](ONBOARDING.md) — Fast double-click Windows 11 setup.
- 🛡️ [**Cybersecurity Classifications Guide (CYBERSECURITY_CLASSIFICATIONS.md)**](CYBERSECURITY_CLASSIFICATIONS.md) — Complete 41-item breakdown of RAdAC, CARTA, EDR/SOAR, and MITRE D3FEND.
- 🔌 [**Compatibility & Supported Tools Guide (COMPATIBILITY.md)**](COMPATIBILITY.md) — Hermes, OpenClaw, DeepSeek, Claude, Cursor, Ollama, and MCP.

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
