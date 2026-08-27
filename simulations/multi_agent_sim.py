"""
Multi-Agent Parallel Scenario Simulation
Simulates concurrent agents operating across different degradation levels simultaneously.
"""

import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.capabilities.descriptor import WindowsAgentSecurityDescriptor
from core.capabilities.manager import capability_manager
from core.risk.engine import risk_engine
from core.risk.state_machine import DegradationState

async def run_multi_agent_simulation():
    print("=" * 60)
    print("RUNNING MULTI-AGENT CONCURRENT SIMULATION")
    print("=" * 60)

    agents = [
        ("agent-dev-01", "Developer Agent", "coding", 0.0),
        ("agent-audit-02", "Security Auditor", "auditing", 35.0),
        ("agent-untrusted-03", "Third Party Scraper", "scraping", 65.0),
        ("agent-contained-04", "Compromised Agent", "unknown", 100.0),
    ]

    for aid, name, mission, initial_risk in agents:
        desc = WindowsAgentSecurityDescriptor(id=aid, name=name, mission=mission, model="qwen")
        capability_manager.register_agent_descriptor(desc)
        risk_engine.reset_agent(aid, reset_score=initial_risk)
        
        state = risk_engine.get_state(aid)
        caps = capability_manager.get_effective_capabilities(aid)
        print(f"[{aid}] Posture: {state.value} | Risk: {initial_risk} | Effective Caps: {len(caps)}")

    print("=" * 60)
    print("MULTI-AGENT CONCURRENT SIMULATION COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_multi_agent_simulation())
