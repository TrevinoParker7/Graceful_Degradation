# GracefulOS Testing Specification

## 1. Multi-Tier Testing Hierarchy

GracefulOS utilizes a comprehensive, multi-layer verification suite:

```text
tests/
├── unit/                 # Pure Python unit tests for state logic, policies, risk formulas
├── integration/          # Gateway API, Named Pipe IPC, SQLite persistence
├── windows/              # Win32 Job Objects, Restricted Tokens, NTFS ACLs, Firewall rules
├── security/             # Invariants INV-001..INV-008, Blast radius budget, Canaries
├── adversarial/          # Indirect prompt injection, obfuscation, escalation, escape attempts
├── chaos/                # Component fault injection (LLM crash, Guardian crash, DB down)
└── playwright/           # E2E browser testing for Dashboard, Approvals, Replay
```

## 2. Test Execution Philosophy
- **Two-Plane Consensus Rule**: If the UI reports an action is blocked, the corresponding Windows operating system primitive (Job Object, ACL, or Firewall rule) must also actively block the operation. UI assertions alone are insufficient.
- **Fail-Secure Invariant Testing**: When testing component failures, tests must assert that privileges stay equal or contract, never expand.
