"""
Graceful Degradation State Machine
Manages the 6 discrete degradation tiers:
LEVEL 0: NORMAL (0-29)
LEVEL 1: WATCH (30-49)
LEVEL 2: RESTRICTED (50-69)
LEVEL 3: READ_ONLY (70-84)
LEVEL 4: ISOLATED (85-94)
LEVEL 5: CONTAINED (95-100)
"""

from enum import Enum
from typing import Tuple

class DegradationState(str, Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    RESTRICTED = "RESTRICTED"
    READ_ONLY = "READ_ONLY"
    ISOLATED = "ISOLATED"
    CONTAINED = "CONTAINED"

STATE_LEVELS = {
    DegradationState.NORMAL: 0,
    DegradationState.WATCH: 1,
    DegradationState.RESTRICTED: 2,
    DegradationState.READ_ONLY: 3,
    DegradationState.ISOLATED: 4,
    DegradationState.CONTAINED: 5,
}

def determine_state_from_score(risk_score: float) -> DegradationState:
    """Calculate the deterministic degradation tier strictly from the 0-100 risk score."""
    score = max(0.0, min(100.0, float(risk_score)))
    if score >= 95.0:
        return DegradationState.CONTAINED
    elif score >= 85.0:
        return DegradationState.ISOLATED
    elif score >= 70.0:
        return DegradationState.READ_ONLY
    elif score >= 50.0:
        return DegradationState.RESTRICTED
    elif score >= 30.0:
        return DegradationState.WATCH
    else:
        return DegradationState.NORMAL

def evaluate_transition(
    current_state: DegradationState, new_score: float
) -> Tuple[bool, DegradationState]:
    """
    Evaluate if risk score warrants a state transition.
    Returns (has_transitioned, target_state).
    """
    target_state = determine_state_from_score(new_score)
    return (target_state != current_state, target_state)
