"""
Windows Defender Firewall Integration Tests
"""

import pytest
from windows.firewall.netsh import firewall_manager

def test_firewall_rule_management():
    agent_id = "test-agent-firewall"
    
    # 1. Add block rule
    ok = firewall_manager.block_agent_network(agent_id)
    assert ok is True

    rules = firewall_manager.get_active_rules()
    assert any(r.agent_id == agent_id for r in rules)

    # 2. Remove block rule
    ok_remove = firewall_manager.remove_agent_block(agent_id)
    assert ok_remove is True
