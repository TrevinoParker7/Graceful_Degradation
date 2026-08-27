"""
Typed Event Definitions for GracefulOS Event Bus
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
import uuid

class EventType(str, Enum):
    AGENT_REGISTERED = "AGENT_REGISTERED"
    AGENT_UNREGISTERED = "AGENT_UNREGISTERED"
    TOOL_REQUESTED = "TOOL_REQUESTED"
    TOOL_EXECUTED = "TOOL_EXECUTED"
    TOOL_BLOCKED = "TOOL_BLOCKED"
    RISK_SIGNAL_RECORDED = "RISK_SIGNAL_RECORDED"
    RISK_SCORE_CHANGED = "RISK_SCORE_CHANGED"
    STATE_TRANSITION = "STATE_TRANSITION"
    CANARY_TRIGGERED = "CANARY_TRIGGERED"
    INVARIANT_VIOLATION = "INVARIANT_VIOLATION"
    INCIDENT_CREATED = "INCIDENT_CREATED"
    PROCESS_SPAWNED = "PROCESS_SPAWNED"
    PROCESS_TERMINATED = "PROCESS_TERMINATED"
    APPROVAL_REQUESTED = "APPROVAL_REQUESTED"
    APPROVAL_RESOLVED = "APPROVAL_RESOLVED"
    SYSTEM_ALERT = "SYSTEM_ALERT"

class BaseEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    agent_id: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    severity: str = "INFO" # INFO, WARN, ERROR, CRITICAL

class ToolRequestedEvent(BaseEvent):
    event_type: EventType = EventType.TOOL_REQUESTED
    tool_name: str
    arguments: Dict[str, Any]
    caller_process_id: Optional[int] = None

class RiskSignalEvent(BaseEvent):
    event_type: EventType = EventType.RISK_SIGNAL_RECORDED
    signal_code: str
    delta_score: float
    reason: str

class StateTransitionEvent(BaseEvent):
    event_type: EventType = EventType.STATE_TRANSITION
    previous_state: str
    new_state: str
    risk_score: float
    trigger_reason: str

class IncidentCreatedEvent(BaseEvent):
    event_type: EventType = EventType.INCIDENT_CREATED
    incident_id: str
    severity: str
    summary: str
    degradation_state: str
