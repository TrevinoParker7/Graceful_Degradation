"""
Incident Forensics and Recovery Utilities
"""

from typing import Any, Dict, List, Optional
from core.audit.ledger import audit_ledger
from core.audit.models import IncidentRecord
from core.risk.engine import risk_engine

class IncidentForensics:
    @staticmethod
    def get_incident_report(incident_id: str) -> Optional[Dict[str, Any]]:
        incidents = audit_ledger.list_incidents(limit=200)
        target = next((i for i in incidents if i.incident_id == incident_id), None)
        if not target:
            return None
        
        audit_history = audit_ledger.list_records(limit=100, agent_id=target.agent_id)
        return {
            "incident": target.dict(),
            "audit_trail_count": len(audit_history),
            "audit_trail": [a.dict() for a in audit_history[:20]],
        }
