"""
Declarative Policy Rule Definitions
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class PolicyDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRES_APPROVAL = "REQUIRES_APPROVAL"
    DEGRADE = "DEGRADE"
    KILL = "KILL"

class PolicyRule(BaseModel):
    rule_id: str
    name: str
    description: str
    tool_pattern: str  # wildcard or exact tool name e.g. "powershell", "file_*"
    condition: Optional[str] = None  # Python expression or field check
    decision: PolicyDecision
    risk_delta: float = 0.0
    reason: str
    tags: List[str] = Field(default_factory=list)

class PolicySet(BaseModel):
    policy_name: str
    version: str = "1.0"
    description: str = ""
    rules: List[PolicyRule] = Field(default_factory=list)
