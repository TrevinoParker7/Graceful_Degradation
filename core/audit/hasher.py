"""
Cryptographic Integrity Hashing for Audit Ledger (SHA-256 Hash Chain)
"""

import hashlib
import json
from typing import Any, Dict

GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

def compute_record_hash(
    record_id: str,
    timestamp: str,
    agent_id: str | None,
    event_type: str,
    action_name: str,
    decision: str,
    risk_score_before: float,
    risk_score_after: float,
    degradation_state: str,
    details: Dict[str, Any],
    prev_hash: str,
) -> str:
    """Compute deterministic SHA-256 hash for audit record chaining."""
    payload = {
        "record_id": record_id,
        "timestamp": timestamp,
        "agent_id": agent_id or "",
        "event_type": event_type,
        "action_name": action_name,
        "decision": decision,
        "risk_score_before": round(float(risk_score_before), 4),
        "risk_score_after": round(float(risk_score_after), 4),
        "degradation_state": degradation_state,
        "details": details,
        "prev_hash": prev_hash,
    }
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
