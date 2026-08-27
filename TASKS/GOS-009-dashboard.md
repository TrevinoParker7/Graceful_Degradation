# GOS-009: Local Real-Time Security Dashboard

## Objective
Implement a local, dark-mode, glassmorphism real-time security dashboard served at `http://127.0.0.1:7777` providing 15 specialized views, live WebSocket telemetry, approval workflows, and interactive incident replay.

## Deliverables
1. FastAPI static and WebSocket backend in `core/gateway/app.py`.
2. 15 comprehensive dashboard views (Overview, Agents, Agent Details, Processes, Capabilities, Risk, Incidents, Network, PowerShell, MCP, Policies, Approvals, Audit Ledger, Incident Replay, Settings).
3. Playwright browser tests in `tests/playwright/test_dashboard.py`.
