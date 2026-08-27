# GOS-002: Async Event Bus & Event Schema

## Objective
Implement a local in-memory priority event bus using Python `asyncio` to broadcast events across Risk Engine, Policy Engine, Audit Ledger, Guardian AI, and Dashboard WebSocket streams.

## Deliverables
1. Strongly typed event classes in `core/events/events.py` (`AgentRegisteredEvent`, `ToolRequestedEvent`, `RiskChangedEvent`, `StateTransitionEvent`, `IncidentCreatedEvent`, etc.).
2. High-performance asynchronous pub/sub event bus in `core/events/bus.py`.
3. Unit tests verifying event routing and subscriber priority ordering.
