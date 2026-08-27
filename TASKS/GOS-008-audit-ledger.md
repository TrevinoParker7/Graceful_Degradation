# GOS-008: SQLite Immutable Audit Ledger & Incident Replay

## Objective
Implement an append-only, SHA-256 hash-chained local audit ledger in SQLite to record every tool request, policy decision, risk change, state transition, and incident.

## Deliverables
1. `core/audit/ledger.py` managing SQLite schema, transaction commits, and SHA-256 block-level chaining.
2. Forensic snapshot generator in `core/audit/snapshot.py` exporting encrypted/compressed incident packages.
3. Incident replay service in `core/audit/replay.py`.
4. Unit tests in `tests/unit/test_audit_ledger.py`.
