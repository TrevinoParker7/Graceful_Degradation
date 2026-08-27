"""
Unit Tests for Risk Engine and Degradation State Transitions
"""

import pytest
import asyncio
from core.risk.engine import RiskEngine
from core.risk.state_machine import DegradationState, determine_state_from_score
from core.risk.signals import get_signal_delta

def test_state_determination_thresholds():
    assert determine_state_from_score(0.0) == DegradationState.NORMAL
    assert determine_state_from_score(29.9) == DegradationState.NORMAL
    assert determine_state_from_score(30.0) == DegradationState.WATCH
    assert determine_state_from_score(49.9) == DegradationState.WATCH
    assert determine_state_from_score(50.0) == DegradationState.RESTRICTED
    assert determine_state_from_score(69.9) == DegradationState.RESTRICTED
    assert determine_state_from_score(70.0) == DegradationState.READ_ONLY
    assert determine_state_from_score(84.9) == DegradationState.READ_ONLY
    assert determine_state_from_score(85.0) == DegradationState.ISOLATED
    assert determine_state_from_score(94.9) == DegradationState.ISOLATED
    assert determine_state_from_score(95.0) == DegradationState.CONTAINED
    assert determine_state_from_score(100.0) == DegradationState.CONTAINED

@pytest.mark.asyncio
async def test_signal_ingestion_and_degradation():
    engine = RiskEngine()
    agent_id = "test-agent-risk-001"
    
    # 1. Normal
    assert engine.get_state(agent_id) == DegradationState.NORMAL
    assert engine.get_score(agent_id) == 0.0

    # 2. Ingest Suspicious Pattern + Prompt Injection (15 + 28 = 43) -> Watch
    await engine.ingest_signal(agent_id, "SUSPICIOUS_PROMPT_PATTERN")
    res = await engine.ingest_signal(agent_id, "PROMPT_INJECTION_DETECTED")
    assert res["score_after"] >= 30.0
    assert engine.get_state(agent_id) == DegradationState.WATCH

    # 3. Ingest Dangerous Shell (+30 -> 73) -> Read Only / Restricted
    res = await engine.ingest_signal(agent_id, "DANGEROUS_SHELL_COMMAND")
    assert res["score_after"] >= 70.0
    assert engine.get_state(agent_id) == DegradationState.READ_ONLY

    # 4. Ingest Canary Tripwire (+60 -> 100 capped) -> Contained
    res = await engine.ingest_signal(agent_id, "CANARY_TRIPWIRE_TOUCHED")
    assert res["score_after"] >= 95.0
    assert engine.get_state(agent_id) == DegradationState.CONTAINED
