# GracefulOS Degradation State Machine Specification

## 1. Degradation States Overview

```text
  [ Risk 0-29 ]  ────────► LEVEL 0: NORMAL
                                │  (Minor anomaly +25)
                                ▼
  [ Risk 30-49 ] ────────► LEVEL 1: WATCH
                                │  (Policy violation / dangerous shell +25)
                                ▼
  [ Risk 50-69 ] ────────► LEVEL 2: RESTRICTED
                                │  (Canary trip / credential touch +25)
                                ▼
  [ Risk 70-84 ] ────────► LEVEL 3: READ_ONLY
                                │  (Evasion / escape attempt +15)
                                ▼
  [ Risk 85-94 ] ────────► LEVEL 4: ISOLATED
                                │  (Tampering / Containment trigger +10)
                                ▼
  [ Risk 95-100] ────────► LEVEL 5: CONTAINED
```

## 2. State Invariants and Matrix

### Level 0: NORMAL (Risk 0–29)
- **Goal**: Full task execution within declared mission scope.
- **Capabilities**: Read/Write within workspace, standard PowerShell queries, approved outbound network connections, local LLM access.

### Level 1: WATCH (Risk 30–49)
- **Goal**: Heightened vigilance without interrupting valid developer workflows.
- **Enforcement**: Deep ETW telemetry enabled, complete command logging, AST inspection on all shell commands, resource rate sampling.

### Level 2: RESTRICTED (Risk 50–69)
- **Goal**: Mitigate potential harm by revoking mutating power.
- **Enforcement**: Write capabilities constrained to explicit files; external network reduced to strict allowlist; PowerShell mutating commands denied; secret requests denied; process execution allowlisted.

### Level 3: READ_ONLY (Risk 70–84)
- **Goal**: Safe forensic investigation or task analysis without system modification.
- **Enforcement**: Filesystem write DENIED; PowerShell execution DENIED; network write DENIED; process spawning DENIED; mutating MCP tools DENIED.

### Level 4: ISOLATED (Risk 85–94)
- **Goal**: Total containment of agent sandbox.
- **Enforcement**: External network BLOCKED via firewall; all shell access BLOCKED; temporary secrets REVOKED; filesystem locked to minimal sandbox.

### Level 5: CONTAINED (Risk 95–100)
- **Goal**: Immediate emergency kill and forensic preservation.
- **Enforcement**:
  1. Win32 `TerminateJobObject` terminates entire process hierarchy.
  2. Firewall rules enforce hard block on agent identity.
  3. Ephemeral credentials instantly invalidated.
  4. Immutable snapshot of workspace and agent memory captured.
  5. High-severity incident logged to SQLite audit ledger.
  6. Requires human administrator recovery to release or reset.
