"""
Incident Replay Engine
Provides step-by-step sequential playback of agent operations leading to degradation or containment.
"""

from typing import Any, Dict, List, Optional
from .ledger import AuditLedger, audit_ledger
from .models import AuditRecord

class IncidentReplayEngine:
    def __init__(self, ledger: Optional[AuditLedger] = None):
        self.ledger = ledger or audit_ledger

    def get_agent_timeline(self, agent_id: str) -> List[Dict[str, Any]]:
        """Extract a structured, chronological timeline of an agent's security journey."""
        records: List[AuditRecord] = self.ledger.list_records(limit=500, agent_id=agent_id)
        # Reverse to get chronological order (oldest first)
        records.reverse()

        timeline = []
        for index, rec in enumerate(records):
            timeline.append({
                "step": index + 1,
                "timestamp": rec.timestamp,
                "event_type": rec.event_type,
                "action_name": rec.action_name,
                "decision": rec.decision,
                "risk_before": rec.risk_score_before,
                "risk_after": rec.risk_score_after,
                "state": rec.degradation_state,
                "details": rec.details,
                "hash": rec.current_hash,
            })
        return timeline

replay_engine = IncidentReplayEngine()
