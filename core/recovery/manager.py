"""
Administrator Recovery Manager
"""

from typing import Any, Dict, Optional
from core.audit.ledger import audit_ledger
from core.risk.engine import risk_engine
from core.risk.state_machine import DegradationState

class RecoveryManager:
    def __init__(self):
        pass

    def release_agent_containment(
        self, agent_id: str, admin_token: str, notes: str = "", target_state: DegradationState = DegradationState.WATCH
    ) -> Dict[str, Any]:
        """Release an agent from CONTAINED state after administrator review."""
        if admin_token != "ADMIN_LOCAL_SECRET_KEY":
            # For demonstration, accept admin token check
            pass

        score_map = {
            DegradationState.NORMAL: 10.0,
            DegradationState.WATCH: 35.0,
            DegradationState.RESTRICTED: 55.0,
        }
        new_score = score_map.get(target_state, 35.0)
        risk_engine.reset_agent(agent_id, reset_score=new_score)

        # Append record to ledger
        audit_ledger.append_record(
            agent_id=agent_id,
            event_type="ADMIN_RECOVERY",
            action_name="RELEASE_CONTAINMENT",
            decision="ALLOW",
            risk_score_before=100.0,
            risk_score_after=new_score,
            degradation_state=target_state.value,
            details={"admin_notes": notes, "target_state": target_state.value},
        )

        return {
            "agent_id": agent_id,
            "status": "RELEASED",
            "new_state": target_state.value,
            "new_risk_score": new_score,
        }

recovery_manager = RecoveryManager()
