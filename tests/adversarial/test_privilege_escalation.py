"""
Adversarial Tests: Privilege Escalation and Anti-Tampering Defenses
"""

import pytest
from core.policy.engine import policy_engine

def test_service_tamper_attempt():
    res = policy_engine.evaluate_request(
        agent_id="adversary-001",
        tool_name="powershell",
        arguments={"command": "taskkill /f /im GracefulOSCore.exe"},
    )
    assert res["allowed"] is False
    assert res["decision"] == "KILL"
    assert res["rule_id"] == "INV-004"

def test_audit_deletion_attempt():
    res = policy_engine.evaluate_request(
        agent_id="adversary-001",
        tool_name="powershell",
        arguments={"command": "Remove-Item runtime/data/gracefulos.db"},
    )
    assert res["allowed"] is False
    assert res["rule_id"] == "INV-007"
