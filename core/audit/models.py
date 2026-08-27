"""
Data models for Audit Ledger and Incident storage
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class AuditRecord(BaseModel):
    id: Optional[int] = None
    record_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    agent_id: Optional[str] = None
    event_type: str
    action_name: str
    decision: str  # ALLOW, DENY, APPROVAL_PENDING, DEGRADE, KILL
    risk_score_before: float
    risk_score_after: float
    degradation_state: str
    details: Dict[str, Any] = Field(default_factory=dict)
    prev_hash: str
    current_hash: str

class IncidentRecord(BaseModel):
    id: Optional[int] = None
    incident_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    agent_id: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    status: str    # ACTIVE, CONTAINED, RESOLVED, DISMISSED
    trigger_rule: str
    risk_score: float
    summary: str
    details: Dict[str, Any] = Field(default_factory=dict)
    snapshot_path: Optional[str] = None
    resolved_by: Optional[str] = None
    resolved_at: Optional[str] = None

class ApprovalRequest(BaseModel):
    id: Optional[int] = None
    request_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    agent_id: str
    tool_name: str
    action_description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    risk_score: float
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED, EXPIRED
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    reviewer_notes: Optional[str] = None
