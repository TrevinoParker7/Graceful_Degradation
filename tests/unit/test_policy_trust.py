"""
Test Allow Once, Always Allow, and Workspace Trust in PolicyEngine
"""

import pytest
from core.policy.engine import policy_engine
from core.risk.engine import risk_engine
from core.capabilities.manager import capability_manager
from core.capabilities.descriptor import WindowsAgentSecurityDescriptor
from core.capabilities.permissions import Capability

def test_allow_once_and_always_allow_workflow():
    agent_id = "test-trust-agent"
    desc = WindowsAgentSecurityDescriptor(
        id=agent_id,
        name="Trust Test Agent",
        mission="testing_trust",
        model="qwen"
    )
    capability_manager.register_agent_descriptor(desc)
    risk_engine.reset_agent(agent_id, 60.0) # RESTRICTED state

    dangerous_cmd = "Remove-Item .\\dist\\* -Recurse"

    # 1. Without trust, this mutating command is denied under RESTRICTED
    eval_before = policy_engine.evaluate_request(
        agent_id=agent_id,
        tool_name="powershell",
        arguments={"command": dangerous_cmd, "is_write": True},
        required_capability=Capability.PS_MUTATE
    )
    assert eval_before["allowed"] is False
    assert eval_before["decision"] == "DENY"

    # 2. Test Allow Once
    policy_engine.authorize_once("powershell")
    eval_once = policy_engine.evaluate_request(
        agent_id=agent_id,
        tool_name="powershell",
        arguments={"command": dangerous_cmd, "is_write": True},
        required_capability=Capability.PS_MUTATE
    )
    assert eval_once["allowed"] is True
    assert eval_once["decision"] == "ALLOW"
    assert "Allow Once" in eval_once["reason"]

    # 3. Next execution should be DENIED again (single-use token consumed)
    eval_after_once = policy_engine.evaluate_request(
        agent_id=agent_id,
        tool_name="powershell",
        arguments={"command": dangerous_cmd, "is_write": True},
        required_capability=Capability.PS_MUTATE
    )
    assert eval_after_once["allowed"] is False

    # 4. Test Always Allow (Permanent Workspace Trust)
    policy_engine.add_trusted_pattern("Remove-Item .\\dist\\*")
    
    eval_always_1 = policy_engine.evaluate_request(
        agent_id=agent_id,
        tool_name="powershell",
        arguments={"command": dangerous_cmd, "is_write": True},
        required_capability=Capability.PS_MUTATE
    )
    assert eval_always_1["allowed"] is True
    assert "Explicitly Trusted" in eval_always_1["reason"]

    eval_always_2 = policy_engine.evaluate_request(
        agent_id=agent_id,
        tool_name="powershell",
        arguments={"command": dangerous_cmd, "is_write": True},
        required_capability=Capability.PS_MUTATE
    )
    assert eval_always_2["allowed"] is True

    # 5. Clean up trust
    policy_engine.remove_trusted_pattern("Remove-Item .\\dist\\*")
    eval_after_cleanup = policy_engine.evaluate_request(
        agent_id=agent_id,
        tool_name="powershell",
        arguments={"command": dangerous_cmd, "is_write": True},
        required_capability=Capability.PS_MUTATE
    )
    assert eval_after_cleanup["allowed"] is False
