"""
Unit Tests for Policy Engine and Declarative Rule Evaluation
"""

import pytest
from core.policy.engine import PolicyEngine
from core.capabilities.permissions import Capability
from core.risk.engine import risk_engine

def test_policy_allow_and_deny():
    pe = PolicyEngine()
    agent_id = "test-agent-policy-001"
    risk_engine.reset_agent(agent_id, 0.0)

    # 1. Read file should be allowed under Normal
    res = pe.evaluate_request(
        agent_id=agent_id,
        tool_name="read_file",
        arguments={"path": "README.md"},
        required_capability=Capability.FILE_READ,
    )
    assert res["allowed"] is True

    # 2. Service Tamper attempt should be KILL / DENIED
    res = pe.evaluate_request(
        agent_id=agent_id,
        tool_name="powershell",
        arguments={"command": "Stop-Service GracefulOS"},
    )
    assert res["allowed"] is False
    assert res["rule_id"] == "INV-004"
