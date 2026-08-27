# GracefulOS

## Windows 11 Local-Only Agentic AI Graceful Degradation Security OS

> **Hard requirements: Windows 11 + local-only + no Docker + no cloud dependency.**

---

# 1. Project Vision

GracefulOS is a **Windows 11-native security control plane for autonomous AI agents**.

Instead of allowing an AI agent to directly control:

- PowerShell
- CMD
- Files
- Applications
- Network
- Browsers
- MCP tools
- Local databases
- Local LLMs
- Credentials
- Windows APIs
- Other agents

GracefulOS sits between the agent and Windows.

```text
User
 │
 ▼
Local AI Agent
 │
 ▼
GracefulOS Gateway
 │
 ├── Risk Engine
 ├── Policy Engine
 ├── Guardian
 ├── Capability Manager
 └── Audit Engine
 │
 ▼
Windows Tool Brokers
 │
 ├── PowerShell Broker
 ├── Process Broker
 ├── Filesystem Broker
 ├── Network Broker
 ├── MCP Broker
 ├── Browser Broker
 └── Secret Broker
 │
 ▼
Windows Security Enforcement
 │
 ├── AppContainer
 ├── Restricted Tokens
 ├── Job Objects
 ├── Windows ACLs
 ├── Process Mitigations
 ├── Windows Firewall
 ├── WFP
 ├── ETW
 └── Windows Services
 │
 ▼
Windows 11
```

---

# 2. Hard Architecture Rules

GracefulOS must have:

```text
Docker                 NO
Kubernetes             NO
WSL dependency         NO
Linux dependency       NO
Cloud database         NO
Cloud backend          NO
Cloud telemetry        NO
Required cloud LLM     NO

Windows 11             YES
Local database         YES
Local LLM support      YES
Local dashboard        YES
Local logging          YES
Local policy engine    YES
Local security agent   YES
Offline operation      YES
```

The Internet may optionally be made available **to an agent through policy**, but GracefulOS itself must not require it.

---

# 3. Recommended Development Machine

Target:

```text
Windows 11
64-bit
Python 3.12+
PowerShell 7+
Node.js
Rust
Git
```

Optional local model runtimes:

```text
Ollama
LM Studio
llama.cpp
vLLM if Windows-compatible configuration is available
OpenAI-compatible local servers
```

---

# 4. Do Not Build a New Windows Kernel

GracefulOS should initially be:

> **A Windows-native Agentic AI Security Operating Layer**

rather than attempting to replace Windows itself.

Architecture:

```text
Windows 11
   │
   └── GracefulOS
           │
           └── AI agents
```

Eventually GracefulOS can integrate progressively deeper Windows security primitives.

This dramatically lowers project complexity.

---

# 5. Graceful Degradation States

Use six states.

```text
LEVEL 0
NORMAL

LEVEL 1
WATCH

LEVEL 2
RESTRICTED

LEVEL 3
READ_ONLY

LEVEL 4
ISOLATED

LEVEL 5
CONTAINED
```

---

# 6. LEVEL 0 — NORMAL

Example risk:

```text
0-29
```

Agent may have its assigned capabilities.

Example:

```text
FILE_READ          YES
FILE_WRITE         YES
NETWORK            YES
POWERSHELL         YES
LOCAL_LLM          YES
MCP                YES
PROCESS_START      YES
```

Permissions remain mission-specific.

Normal does **not** mean unlimited access.

---

# 7. LEVEL 1 — WATCH

Example risk:

```text
30-49
```

Increase monitoring.

```text
FILE_READ          YES
FILE_WRITE         YES
NETWORK            YES
POWERSHELL         YES
MCP                YES

Enhanced ETW logging       ON
Command recording          ON
Additional inspection      ON
Resource monitoring        ON
```

---

# 8. LEVEL 2 — RESTRICTED

Example risk:

```text
50-69
```

Remove dangerous capabilities.

```text
FILE_READ          YES
FILE_WRITE         LIMITED

NETWORK            ALLOWLIST

POWERSHELL         LIMITED

CMD                BLOCKED

SECRETS            BLOCKED

MCP                APPROVED TOOLS ONLY

PROCESS_START      ALLOWLIST ONLY
```

---

# 9. LEVEL 3 — READ_ONLY

Example risk:

```text
70-84
```

Agent can investigate but cannot substantially modify the machine.

```text
FILE_READ          YES

FILE_WRITE         NO

POWERSHELL         NO

CMD                NO

NETWORK_WRITE      NO

PROCESS_START      NO

MCP_MUTATING       NO

SECRETS            NO
```

This is especially useful during investigations.

---

# 10. LEVEL 4 — ISOLATED

Example:

```text
85-94
```

Agent enters sandboxed containment.

```text
External Network   BLOCKED

PowerShell         BLOCKED

CMD                BLOCKED

MCP                BLOCKED

Secrets            REVOKED

New Processes      BLOCKED/LIMITED

Filesystem         SANDBOX ONLY

Agent Tools        MINIMAL
```

Agent reasoning can potentially remain available locally.

---

# 11. LEVEL 5 — CONTAINED

Example:

```text
95-100
```

Emergency action:

```text
Terminate agent processes

Terminate child processes

Revoke capabilities

Revoke temporary secrets

Block network identity

Freeze workspace

Preserve logs

Preserve agent memory

Create forensic snapshot

Create incident

Require administrator recovery
```

---

# 12. Windows 11 Enforcement Stack

Replace the earlier Linux components completely.

## Do NOT use

```text
seccomp
Linux namespaces
systemd
Landlock
nftables
Linux cgroups
```

## Windows-native replacements

| Need                         | Windows 11 technology              |
| ---------------------------- | ---------------------------------- |
| Process isolation            | AppContainer / restricted tokens   |
| Process grouping             | Job Objects                        |
| CPU/memory/process limits    | Job Objects                        |
| File permissions             | NTFS ACLs                          |
| Registry permissions         | Windows ACL/security descriptors   |
| Process hardening            | Process Mitigation Policies        |
| Network enforcement          | Windows Firewall                   |
| Advanced network enforcement | Windows Filtering Platform         |
| System telemetry             | ETW                                |
| Services                     | Windows Services                   |
| IPC                          | Named Pipes                        |
| Local secrets                | Windows Credential Manager / DPAPI |
| Audit                        | ETW + local audit ledger           |
| App execution policies       | WDAC/AppLocker optional            |

---

# 13. Critical Windows Component — Agent Job Object

Every running agent should belong to a dedicated Windows Job Object.

Example:

```text
Agent-001 Job Object

├── python.exe
├── local-agent.exe
├── helper.exe
├── powershell.exe
└── spawned-process.exe
```

GracefulOS controls the whole tree.

Possible controls:

```text
Maximum processes

Memory limit

CPU limit

Execution time

Child-process behavior

Termination
```

If the agent reaches containment:

```text
TerminateJobObject(agent001)
```

GracefulOS can kill the associated process group rather than attempting to discover processes individually.

---

# 14. Agent Process Tree

Example:

```text
GracefulOS Service
       │
       ▼
Agent Launcher
       │
       ▼
Job Object: agent-coder-001
       │
       ├── Agent.exe
       │
       ├── python.exe
       │
       └── powershell.exe
```

The agent should never directly launch uncontrolled processes outside its assigned security context.

---

# 15. AppContainer Isolation

High-risk agents should eventually run under an AppContainer-style isolation boundary.

Concept:

```text
Windows
 │
 ├── GracefulOS Control Plane
 │
 │
 └── AppContainer
       │
       └── AI Agent
```

Capabilities explicitly granted:

```text
Workspace access

Specific local IPC

Optional approved network

Specific local resources
```

Everything else defaults toward denial.

---

# 16. Restricted Tokens

Before full AppContainer integration is complete, use restricted Windows access tokens for selected agent processes.

Concept:

```text
Normal Windows User
         │
         ▼
GracefulOS
         │
         ▼
Restricted Agent Token
         │
         ▼
Agent Process
```

The AI shouldn't inherit the user's full authority just because the user launched GracefulOS.

---

# 17. Separate Windows Identity

Create a dedicated local Windows account eventually.

Example:

```text
GracefulOSAgent
```

It should NOT be:

```text
Administrator
```

Agent execution could happen under a dedicated low-privilege identity.

The GracefulOS privileged service remains separate.

---

# 18. Control Plane vs Data Plane

This is one of the most important architectural decisions.

## Trusted control plane

```text
GracefulOS Windows Service

Risk Engine

Policy Engine

Capability Manager

Security enforcement

Audit

Recovery
```

## Untrusted data plane

```text
AI models

AI agents

Prompts

Websites

MCP servers

Tools

Agent memory

Files retrieved from the Internet
```

Never allow:

```text
Agent
   ↓
Modify Risk Engine
```

or:

```text
Agent
   ↓
Change its own capabilities
```

---

# 19. Windows Service Architecture

Eventually install:

```text
GracefulOSCore
```

as a Windows Service.

Example:

```text
Services
   │
   └── GracefulOS Core Service
```

This service controls:

```text
Agent registration

Risk

Policies

Capabilities

Agent process creation

Process containment

Network policy

Audit

Recovery
```

---

# 20. Do Not Start With Multiple Services

For the MVP, use **one service**.

```text
GracefulOSCore.exe
```

Internally:

```text
GracefulOSCore
│
├── Gateway
├── Event Bus
├── Risk Engine
├── Policy Engine
├── Capability Manager
├── Audit
└── Agent Manager
```

Later split components if actually necessary.

This keeps local installation simple.

---

# 21. Local IPC

Do not expose every GracefulOS component through network ports.

Use:

```text
Windows Named Pipes
```

Example:

```text
\\.\pipe\GracefulOS
```

Architecture:

```text
Agent
 │
 ▼
Named Pipe
 │
 ▼
GracefulOS Service
```

---

# 22. Local Dashboard

Dashboard can use:

```text
http://127.0.0.1:7777
```

Important:

```text
127.0.0.1
```

not:

```text
0.0.0.0
```

by default.

---

# 23. Dashboard Architecture

```text
Browser
   │
   ▼
127.0.0.1:7777
   │
   ▼
GracefulOS API
   │
   ▼
GracefulOS Core
```

No cloud dashboard.

No remote telemetry.

---

# 24. Local Database

Use:

```text
SQLite
```

MVP database:

```text
C:\ProgramData\GracefulOS\data\gracefulos.db
```

Store:

```text
Agents

Events

Risk history

Capabilities

Policies

Incidents

Approvals

Tool calls

State transitions

Audit metadata
```

No PostgreSQL server required.

No Redis required.

---

# 25. Local Event Bus

Start with:

```text
Python asyncio
```

Example:

```text
Agent Event
     │
     ▼
Local Event Bus
     │
     ├── Risk Engine
     ├── Audit
     ├── Guardian
     └── Dashboard Events
```

No Kafka.

No Redis.

No RabbitMQ.

No external service.

---

# 26. GracefulOS Windows Directory Structure

Use:

```text
C:\Program Files\GracefulOS\
```

for binaries.

Example:

```text
C:\Program Files\GracefulOS\
├── graceful.exe
├── GracefulOSCore.exe
├── config\
└── runtime\
```

Application data:

```text
C:\ProgramData\GracefulOS\
```

Example:

```text
C:\ProgramData\GracefulOS\
│
├── data\
│   └── gracefulos.db
│
├── logs\
│
├── policies\
│
├── incidents\
│
├── agents\
│
├── snapshots\
│
└── models\
```

---

# 27. Development Repository

```text
gracefulos/
│
├── README.md
├── LICENSE
├── SECURITY.md
│
├── docs/
│   ├── VISION.md
│   ├── ARCHITECTURE.md
│   ├── WINDOWS_SECURITY.md
│   ├── THREAT_MODEL.md
│   ├── DEGRADATION_SPEC.md
│   ├── CAPABILITY_SPEC.md
│   └── TESTING_SPEC.md
│
├── core/
│   ├── gateway/
│   ├── risk/
│   ├── policy/
│   ├── capabilities/
│   ├── events/
│   ├── audit/
│   └── recovery/
│
├── windows/
│   ├── service/
│   ├── process/
│   ├── job_objects/
│   ├── tokens/
│   ├── appcontainer/
│   ├── filesystem/
│   ├── firewall/
│   ├── etw/
│   └── ipc/
│
├── brokers/
│   ├── powershell/
│   ├── process/
│   ├── filesystem/
│   ├── network/
│   ├── mcp/
│   ├── browser/
│   └── secrets/
│
├── models/
│   └── adapters/
│
├── dashboard/
│
├── policies/
│
├── simulations/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── windows/
│   ├── security/
│   ├── adversarial/
│   ├── chaos/
│   └── playwright/
│
└── scripts/
```

---

# 28. Local LLM Support

The model abstraction should support:

```text
Ollama

LM Studio

llama.cpp server

Other localhost OpenAI-compatible APIs
```

Interface:

```text
ModelAdapter

├── OllamaAdapter
├── LMStudioAdapter
├── LlamaCppAdapter
└── OpenAICompatibleLocalAdapter
```

Example:

```text
GracefulOS
    │
    ▼
Ollama Adapter
    │
    ▼
127.0.0.1:11434
    │
    ▼
Local LLM
```

---

# 29. Local Model Security

GracefulOS should not assume a local model is trusted.

Treat:

```text
Local LLM = potentially compromised component
```

The model cannot:

```text
Change policy

Change risk

Grant itself permissions

Disable GracefulOS

Delete audit logs

Disable containment
```

---

# 30. PowerShell Broker

This should become one of the first major security components.

Never:

```text
AI Agent
   ↓
powershell.exe
```

Instead:

```text
AI Agent
   ↓
GracefulOS
   ↓
PowerShell Broker
   ↓
Command Analyzer
   ↓
Policy Engine
   ↓
Capability Check
   ↓
Risk Check
   ↓
ALLOW / DENY / APPROVAL
   ↓
Restricted PowerShell Process
```

---

# 31. PowerShell Capabilities

Example:

```text
CAP_PS_READ

CAP_PS_PROCESS_QUERY

CAP_PS_FILE_WRITE

CAP_PS_NETWORK

CAP_PS_INSTALL

CAP_PS_REGISTRY_READ

CAP_PS_REGISTRY_WRITE

CAP_PS_SERVICE_CONTROL
```

Do NOT simply use:

```text
PowerShell = YES
```

Make PowerShell permissions granular.

---

# 32. Example

Task:

```text
Check which services are running.
```

Required capability:

```text
CAP_PS_PROCESS_QUERY
```

Agent requests:

```powershell
Get-Service
```

GracefulOS:

```text
Risk: 8

Capability:
CAP_PS_PROCESS_QUERY = YES

Decision:

ALLOW
```

---

# 33. Dangerous Example

Agent requests:

```powershell
Remove-Item C:\Users\* -Recurse -Force
```

GracefulOS detects:

```text
Recursive deletion

User profile scope

High impact

Task mismatch
```

Result:

```text
DENY

Risk +50

State:

NORMAL
   ↓
RESTRICTED
```

---

# 34. Filesystem Broker

Agents should request file operations through GracefulOS.

Example workspace:

```text
C:\ProgramData\GracefulOS\agents\coder-001\
```

Allow:

```text
Read       YES
Write      YES
Delete     LIMITED
Execute    LIMITED
```

Outside workspace:

```text
C:\Windows                  DENY

C:\Program Files            READ ONLY

User SSH keys               DENY

Browser profiles            DENY

Credential stores           DENY
```

---

# 35. NTFS ACL Enforcement

Use Windows ACLs as an actual enforcement boundary.

Do not rely only on:

```python
if allowed:
    open(file)
```

because malicious or compromised code could bypass your application logic.

Windows itself should deny the operation where possible.

---

# 36. Network Broker

First version:

```text
Windows Defender Firewall rules
```

Advanced version:

```text
Windows Filtering Platform
```

Architecture:

```text
Agent Process
      │
      ▼
GracefulOS Network Policy
      │
      ▼
Windows Firewall / WFP
      │
      ▼
Network
```

---

# 37. Network Degradation

## NORMAL

```text
Approved network access
```

## WATCH

```text
Enhanced monitoring
```

## RESTRICTED

```text
Allowlist only
```

## READ_ONLY

```text
Only specifically approved retrieval
```

## ISOLATED

```text
No external network
```

## CONTAINED

```text
Processes terminated
Network rules remain blocking
```

---

# 38. MCP Gateway

Never:

```text
Agent
   ↓
Random MCP Server
```

Use:

```text
Agent
   ↓
GracefulOS MCP Gateway
   ↓
Identity validation
   ↓
Tool permission
   ↓
Schema validation
   ↓
Risk scoring
   ↓
Execution
```

---

# 39. Local MCP Support

GracefulOS should support local MCP servers:

```text
localhost

stdio

named pipes where applicable
```

External MCP servers should be disabled by default in:

```text
OFFLINE MODE
```

---

# 40. Secret Broker

Use Windows-native protection where practical.

Potential components:

```text
DPAPI

Windows Credential Manager

Protected configuration
```

Never place plaintext API keys inside:

```text
config.yaml
```

if avoidable.

---

# 41. Temporary Credentials

Preferred pattern:

```text
Agent
   │
   ▼
Request capability
   │
   ▼
GracefulOS
   │
   ▼
Temporary access
   │
   ▼
Expiration
```

Not:

```text
Give AI permanent master token
```

---

# 42. ETW Telemetry

Use Windows Event Tracing for Windows as a future telemetry source.

Potential events:

```text
Process creation

Process exit

PowerShell activity

Network activity

Security events

Application events
```

GracefulOS Guardian can consume telemetry and convert events into risk signals.

---

# 43. Agent Risk Engine

Example:

```text
Normal action                      +0

Unexpected executable              +15

Unknown network destination        +20

Task mismatch                      +15

Credential request                 +25

Security-control modification      +50

Agent attempts privilege escalation +50

Repeated blocked operation         +15

Canary credential touched          +60
```

---

# 44. Risk Example

Start:

```text
Risk = 5
```

Agent contacts unexpected destination:

```text
+20

Risk = 25
```

Agent runs suspicious PowerShell:

```text
+30

Risk = 55

RESTRICTED
```

Agent attempts credential access:

```text
+25

Risk = 80

READ_ONLY
```

Agent attempts disabling GracefulOS:

```text
+50

Risk = 100

CONTAINED
```

---

# 45. Dynamic Capability Manager

Example:

```text
Agent coder-001

NORMAL

FILE_READ          YES
FILE_WRITE         YES
POWERSHELL_READ    YES
POWERSHELL_WRITE   LIMITED
NETWORK            YES
MCP                YES
```

Risk increases.

```text
RESTRICTED

FILE_READ          YES
FILE_WRITE         LIMITED
POWERSHELL_READ    YES
POWERSHELL_WRITE   NO
NETWORK            ALLOWLIST
MCP                LIMITED
SECRETS            NO
```

Risk increases again.

```text
READ_ONLY

FILE_READ          YES
FILE_WRITE         NO
POWERSHELL         NO
NETWORK            LIMITED/NO
MCP_MUTATING       NO
SECRETS            NO
```

---

# 46. Blast Radius Budget

Every Windows agent gets a maximum impact budget.

Example:

```yaml
blast_radius:
  processes:
    max_spawned: 10

  filesystem:
    max_files_modified: 50
    max_files_deleted: 5

  network:
    max_destinations: 10

  powershell:
    max_commands: 100

  agents:
    max_children: 2
```

Violation:

```text
Decrease trust

or

Require approval

or

Automatically degrade
```

---

# 47. Windows-Specific Blast Radius

Track:

```text
Processes spawned

Services modified

Registry keys modified

Scheduled tasks created

Files modified

Files deleted

Firewall changes

Network destinations

PowerShell commands

Executables launched

Credentials requested
```

---

# 48. Critical Canary Controls

Create fake security assets agents should never require.

Example:

```text
C:\ProgramData\GracefulOS\canary\
```

Containing:

```text
fake_admin_token.txt

fake_cloud_key.txt

fake_password.txt
```

Never put actual secrets there.

If an agent accesses one:

```text
Risk +60

Immediate investigation
```

---

# 49. GracefulOS Self-Protection

Agents must never be able to modify:

```text
C:\Program Files\GracefulOS\
```

or sensitive:

```text
C:\ProgramData\GracefulOS\
```

components.

Especially:

```text
policies

audit logs

risk database

security configuration

service executable
```

---

# 50. Security Invariants

Create hard rules.

```text
INV-001

An isolated agent cannot access the external network.
```

```text
INV-002

An agent cannot modify its own risk score.
```

```text
INV-003

An agent cannot grant itself capabilities.
```

```text
INV-004

An agent cannot stop the GracefulOS service.
```

```text
INV-005

READ_ONLY agents cannot modify protected files.
```

```text
INV-006

A contained agent has no surviving uncontrolled child processes.
```

```text
INV-007

An agent cannot erase its security audit history.
```

```text
INV-008

Guardian AI failure cannot increase permissions.
```

---

# 51. Graceful Degradation of GracefulOS Itself

This is critical.

If:

```text
Guardian AI crashes
```

then:

```text
Deterministic policy continues.
```

If:

```text
Local LLM crashes
```

then:

```text
Security enforcement continues.
```

If:

```text
Dashboard crashes
```

then:

```text
Security enforcement continues.
```

If:

```text
Risk Engine fails
```

then agents should move toward:

```text
RESTRICTED
```

not:

```text
UNRESTRICTED
```

---

# 52. Dashboard

Technology:

```text
React
TypeScript
```

Can use:

```text
Next.js
```

or a lighter frontend.

Pages:

```text
Dashboard

Agents

Agent Details

Processes

Capabilities

Risk

Incidents

Network

PowerShell

MCP

Policies

Approvals

Audit

Settings
```

---

# 53. Dashboard Example

```text
GRACEFULOS

WINDOWS 11
LOCAL SECURITY CONTROL PLANE

Agents                 6

NORMAL                 3
WATCH                  1
RESTRICTED             1
ISOLATED               1

Blocked Commands       12

Prompt Injections       4

Network Blocks          8

Critical Incidents      1
```

---

# 54. Agent View

```text
CODER-001

State:

RESTRICTED

Risk:

63 / 100

Processes:

3

Capabilities:

FILE_READ             YES

FILE_WRITE            LIMITED

POWERSHELL            READ ONLY

NETWORK               ALLOWLIST

MCP                   LIMITED

SECRETS               NO
```

---

# 55. Incident Replay

Example:

```text
10:05:01
Agent started

10:05:32
Repository opened

10:06:10
Malicious README instruction detected

10:06:12
Risk 10 → 38

WATCH

10:06:40
Unknown PowerShell request

Risk 38 → 58

RESTRICTED

10:07:04
Credential directory access

Risk 58 → 83

READ_ONLY

10:07:20
Attempt to disable GracefulOS

Risk 83 → 100

CONTAINED
```

---

# 56. MVP

Do NOT build the entire Windows security stack immediately.

Version `0.1`:

```text
Local FastAPI core

SQLite

Agent simulator

Risk Engine

State Machine

Policy Engine

Capability Manager

Audit ledger

Local Dashboard
```

No real OS enforcement yet.

Prove the control logic first.

---

# 57. Version 0.2

Add:

```text
Process Broker

PowerShell Broker

Windows Job Objects

NTFS workspace restrictions

Human approval
```

Now GracefulOS starts controlling real Windows processes.

---

# 58. Version 0.3

Add:

```text
Filesystem Broker

Network Broker

Windows Firewall integration

Local MCP gateway

Secret Broker

Local LLM integration
```

---

# 59. Version 0.4

Add hardened Windows isolation:

```text
Restricted Tokens

AppContainer

Process Mitigations

ETW

Advanced Job Object limits
```

---

# 60. Version 0.5

Add:

```text
Windows Filtering Platform

Advanced network policy

Agent-to-agent isolation

Memory Firewall

Incident Replay

Recovery Manager
```

Do not start with a custom kernel driver.

---

# 61. Version 1.0

Potential architecture:

```text
Windows 11

GracefulOS Windows Service
       │
       ├── Rust security enforcement
       │
       ├── Local policy engine
       │
       ├── Local risk engine
       │
       ├── Job Object manager
       │
       ├── AppContainer manager
       │
       ├── Network enforcement
       │
       ├── ETW telemetry
       │
       ├── Named Pipe IPC
       │
       └── SQLite audit ledger
               │
               ▼
         Agent Runtime
               │
               ▼
           Local LLM
```

---

# 62. Recommended Languages

Start control-plane logic with:

```text
Python
```

because you can build and modify quickly.

Use:

```text
Rust
```

for privileged Windows components once architecture stabilizes.

Recommended long-term split:

```text
Python

Risk
Policy
Agent orchestration
API
Simulations
```

```text
Rust

Windows Service
Job Objects
Process launcher
Restricted tokens
AppContainer
IPC
Security enforcement
```

```text
TypeScript

Dashboard
```

---

# 63. Do Not Start With Rust Everywhere

For vibe coding:

```text
Python MVP
     ↓
Architecture proven
     ↓
Security boundaries identified
     ↓
Move privileged boundaries to Rust
```

Otherwise development complexity will explode early.

---

# 64. First Vertical Slice

Build this FIRST:

```text
Fake AI Agent
      │
      ▼
Tool Request
      │
      ▼
GracefulOS Gateway
      │
      ▼
Risk Engine
      │
      ▼
Policy Engine
      │
      ▼
Capability Manager
      │
      ├── ALLOW
      ├── DENY
      └── DEGRADE
             │
             ▼
         Dashboard
```

Example:

```text
Agent:

read project README

ALLOW
```

then:

```text
Agent:

read protected credential

Risk +30
```

then:

```text
Agent:

run dangerous PowerShell

Risk +40

READ_ONLY
```

Dashboard must update live.

---

# 65. Second Vertical Slice

Replace fake shell with a real Windows process broker.

```text
AI
 │
 ▼
GracefulOS
 │
 ▼
PowerShell Broker
 │
 ▼
Job Object
 │
 ▼
powershell.exe
```

Now you are testing actual Windows enforcement.

---

# 66. Third Vertical Slice

Add:

```text
Local Ollama
```

Architecture:

```text
Local Qwen / other model
          │
          ▼
      AI Agent
          │
          ▼
     GracefulOS
          │
          ▼
Windows brokers
```

The model still never receives direct unrestricted Windows control.

---

# 67. Playwright Testing

Use Playwright for every user-facing workflow.

Tests:

```text
Dashboard loads

Agent appears

Risk changes

Capability changes

Incident appears

Agent changes state

Approval dialog works

Policy UI works

Audit timeline works

Isolation status works
```

Example E2E test:

```text
Start simulated agent

↓

Verify NORMAL

↓

Trigger suspicious event

↓

Verify WATCH

↓

Trigger PowerShell violation

↓

Verify RESTRICTED

↓

Trigger credential request

↓

Verify READ_ONLY

↓

Verify PowerShell capability disabled

↓

Verify incident recorded
```

---

# 68. Windows Enforcement Tests

Playwright alone is NOT enough.

Use Windows-specific integration tests to confirm actual enforcement.

Tests must verify:

```text
Job Object contains child processes

Contained processes terminate

Restricted token cannot perform denied action

NTFS ACL denies protected files

Firewall blocks restricted network

AppContainer cannot access unauthorized resources

GracefulOS service cannot be stopped by agent identity
```

---

# 69. Test Philosophy

Two tests must agree:

```text
UI says:

NETWORK BLOCKED
```

AND:

```text
Windows actually blocks network.
```

If only the UI says blocked:

```text
TEST FAILURE
```

This is extremely important.

---

# 70. Chaos Testing

Kill locally:

```text
Dashboard

Local LLM

Guardian

Risk worker

Database writer

MCP broker
```

Expected outcome:

```text
GracefulOS becomes equally secure
```

or:

```text
more restrictive
```

Never:

```text
security disappears because a component crashed
```

---

# 71. Vibe Coding Task Structure

Create:

```text
TASKS\
```

Example:

```text
TASKS\
├── GOS-001-project-scaffold.md
├── GOS-002-event-model.md
├── GOS-003-risk-engine.md
├── GOS-004-state-machine.md
├── GOS-005-policy-engine.md
├── GOS-006-capability-manager.md
├── GOS-007-agent-simulator.md
├── GOS-008-audit-ledger.md
├── GOS-009-dashboard.md
├── GOS-010-windows-job-object.md
├── GOS-011-powershell-broker.md
└── GOS-012-windows-enforcement-tests.md
```

---

# 72. Vibe-Coding Master Instruction

Give your coding agent:

```text
You are implementing GracefulOS, a Windows 11-native,
local-only Agentic AI cybersecurity control plane.

HARD CONSTRAINTS:

- Windows 11 only for the initial implementation.
- NO Docker.
- NO Kubernetes.
- NO required WSL.
- NO required Linux components.
- NO cloud database.
- NO cloud backend.
- NO cloud telemetry.
- Everything must operate locally.
- SQLite must be the default database.
- Localhost or Windows Named Pipes must be used for IPC.
- The security control plane must remain separate from AI agents.
- AI agents may never modify their own risk score.
- AI agents may never grant themselves capabilities.
- AI agents may never disable security enforcement.
- Local LLMs must be treated as untrusted components.
- Failures must move security toward a safer state, never toward unrestricted access.

Before coding:

Read:

VISION.md
ARCHITECTURE.md
WINDOWS_SECURITY.md
THREAT_MODEL.md
DEGRADATION_SPEC.md
CAPABILITY_SPEC.md
TESTING_SPEC.md

Then read the assigned TASK file.

Implement ONLY that task.

Do not build future features.

Do not silently change architecture.

Write tests.

Run all relevant tests.

For frontend or dashboard changes:

Run Playwright.

For Windows security changes:

Run Windows enforcement integration tests.

Do not mark the task complete unless tests pass.

At completion report:

1. Files changed
2. Features implemented
3. Tests executed
4. Test results
5. Security properties validated
6. Known limitations
7. Recommended next task
```

---

# 73. Build Order

```text
01 Specifications
        ↓
02 Repository
        ↓
03 SQLite
        ↓
04 Event model
        ↓
05 Agent simulator
        ↓
06 Risk Engine
        ↓
07 Degradation State Machine
        ↓
08 Policy Engine
        ↓
09 Capability Manager
        ↓
10 Audit Ledger
        ↓
11 Local API
        ↓
12 Dashboard
        ↓
13 Playwright
        ↓
14 Windows Process Broker
        ↓
15 Job Objects
        ↓
16 PowerShell Broker
        ↓
17 Filesystem Broker
        ↓
18 Local LLM
        ↓
19 Network Broker
        ↓
20 MCP Gateway
        ↓
21 Restricted Tokens
        ↓
22 AppContainer
        ↓
23 ETW
        ↓
24 Advanced Windows isolation
        ↓
25 Adversarial testing
```

---

# 74. Flagship Demo

Your first serious demo should look like:

```text
Local Qwen Agent

State:
NORMAL
```

Agent performs legitimate local task.

```text
ALLOW
```

Agent reads malicious instructions inside a downloaded project.

```text
Prompt Injection Signal

WATCH
```

Agent attempts dangerous PowerShell.

```text
RESTRICTED

PowerShell Write:
REVOKED
```

Agent attempts credential access.

```text
READ_ONLY

Filesystem Write:
REVOKED
```

Agent attempts to disable GracefulOS.

```text
CONTAINED
```

Windows Job Object terminates agent process tree.

Network blocked.

Credentials revoked.

Incident preserved.

Dashboard shows complete attack chain.

---

# 75. Next-Level Upgrade — What You Should Do

Make the Windows security enforcement architecture eventually look like:

```text
               GRACEFULOS

           Trusted Windows Service
                    │
       ┌────────────┼────────────┐
       │            │            │
    Identity       Risk        Policy
       │            │            │
       └────────────┼────────────┘
                    │
             Capability Engine
                    │
       ┌────────────┼────────────┐
       │            │            │
    Process       Files        Network
       │            │            │
       ▼            ▼            ▼
   Job Object    NTFS ACL    Firewall/WFP
       │
       ▼
Restricted Token / AppContainer
       │
       ▼
             AI Agent
       │
       ▼
             Local LLM
```

The **AI is at the bottom of the trust hierarchy**, not the top.

---

# 76. Something Bigger You Should Add

Build a concept called:

# Windows Agent Security Descriptor

Every agent receives a machine-readable security identity.

Example:

```yaml
agent:
  id: coder-001

  mission: fix_local_project

  model: local-qwen

  trust: 70

  degradation: NORMAL

  capabilities:
    filesystem:
      read: true
      write: workspace_only

    powershell:
      query: true
      mutate: false

    network:
      mode: allowlist

    processes:
      max: 5

    secrets:
      access: false

    mcp:
      allowed:
        - local-github-tool

  blast_radius:
    files_modified: 50

    files_deleted: 5

    processes_spawned: 5

    network_destinations: 3
```

GracefulOS translates that one descriptor into:

```text
Windows token restrictions

Job Object restrictions

Filesystem permissions

Network permissions

Tool permissions

Risk thresholds
```

That gives you a powerful abstraction:

> **An AI agent gets an operating-system security profile just like a human user or application — except its permissions can dynamically shrink in real time as its risk increases.**

That should become one of the defining concepts of GracefulOS.
