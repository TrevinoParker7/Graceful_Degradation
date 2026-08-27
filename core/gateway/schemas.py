"""
Pydantic Schemas for Gateway REST and WebSocket Endpoints
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class AgentRegisterRequest(BaseModel):
    agent_id: str
    name: str = "Assistant"
    mission: str = "code_editing"
    model: str = "local-qwen"
    trust_score: float = 70.0
    wasd_yaml: Optional[str] = None

class ToolInvocationRequest(BaseModel):
    agent_id: str
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

class RiskSignalRequest(BaseModel):
    agent_id: str
    signal_code: str
    custom_delta: Optional[float] = None
    reason: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ApprovalDecisionRequest(BaseModel):
    request_id: str
    approved: bool
    reviewer: str = "administrator"
    notes: str = ""

class ContainmentReleaseRequest(BaseModel):
    agent_id: str
    admin_token: str
    target_state: str = "WATCH"
    notes: str = ""

class SystemStatusResponse(BaseModel):
    app_name: str
    version: str
    status: str
    total_agents: int
    active_incidents: int
    pending_approvals: int
    tamper_free_ledger: bool
    degradation_distribution: Dict[str, int]
