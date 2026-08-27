"""
Unit Tests for Dynamic Capability Manager
"""

import pytest
from core.capabilities.descriptor import WindowsAgentSecurityDescriptor
from core.capabilities.manager import CapabilityManager
from core.capabilities.permissions import Capability
from core.risk.engine import risk_engine

def test_effective_capability_shrinkage():
    cm = CapabilityManager()
    agent_id = "test-agent-caps-001"
    
    descriptor = WindowsAgentSecurityDescriptor(
        id=agent_id,
        name="Test Agent",
        mission="testing",
        model="qwen",
    )
    cm.register_agent_descriptor(descriptor)

    # 1. In Normal state, agent has FILE_READ, FILE_WRITE
    risk_engine.reset_agent(agent_id, 0.0)
    caps_normal = cm.get_effective_capabilities(agent_id)
    assert Capability.FILE_READ in caps_normal

    # 2. In RESTRICTED state (e.g. risk 60)
    risk_engine.reset_agent(agent_id, 60.0)
    caps_restricted = cm.get_effective_capabilities(agent_id)
    assert Capability.FILE_READ in caps_restricted
    assert Capability.PS_MUTATE not in caps_restricted

    # 3. In CONTAINED state (risk 100) -> ZERO capabilities
    risk_engine.reset_agent(agent_id, 100.0)
    caps_contained = cm.get_effective_capabilities(agent_id)
    assert len(caps_contained) == 0
