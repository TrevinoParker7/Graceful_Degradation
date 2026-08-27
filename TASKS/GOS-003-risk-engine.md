# GOS-003: Dynamic Risk Engine & Signal Accumulator

## Objective
Implement the 0–100 numerical risk engine that scores agent actions, accumulates anomaly signals, tracks canary tripwire hits, calculates cumulative decay over time, and enforces blast-radius budgets.

## Deliverables
1. `core/risk/engine.py` evaluating composite risk scores based on signal severity, historical frequency, and canary breaches.
2. Signal definitions in `core/risk/signals.py` (e.g. `PROMPT_INJECTION_DETECTED: +28`, `DANGEROUS_SHELL_COMMAND: +25`, `CANARY_TRIPWIRE_TOUCHED: +60`, `SERVICE_TAMPER_ATTEMPT: +50`).
3. Blast radius tracker in `core/risk/blast_radius.py` tracking file modifications, process spawns, network destinations, and command counts.
4. Comprehensive unit tests in `tests/unit/test_risk_engine.py`.
