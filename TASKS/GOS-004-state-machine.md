# GOS-004: Degradation State Machine

## Objective
Implement the 6-level graceful degradation state machine with state transition hooks, invariant checks, and automated downgrade triggers.

## Deliverables
1. `core/risk/state_machine.py` managing state evaluation:
   - `LEVEL 0: NORMAL` (0-29)
   - `LEVEL 1: WATCH` (30-49)
   - `LEVEL 2: RESTRICTED` (50-69)
   - `LEVEL 3: READ_ONLY` (70-84)
   - `LEVEL 4: ISOLATED` (85-94)
   - `LEVEL 5: CONTAINED` (95-100)
2. State transition listeners that invoke Windows enforcement handlers upon level escalation.
3. Unit tests verifying state machine boundaries and unidirectional escalation during incidents.
