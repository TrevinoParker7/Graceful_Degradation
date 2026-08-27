# GOS-001: Project Scaffold and Environment Configuration

## Objective
Establish the directory layout, configuration system, SQLite schema migrations, and packaging structure for GracefulOS on Windows 11.

## Deliverables
1. Directory structure (`core/`, `windows/`, `brokers/`, `models/`, `dashboard/`, `policies/`, `simulations/`, `tests/`, `scripts/`).
2. Configuration loader in `config/settings.py` supporting offline defaults and file paths.
3. Database initialization in `core/audit/ledger.py` generating tables for agents, events, risk history, incidents, approvals, and snapshots.
4. CLI entrypoint `graceful.py`.
