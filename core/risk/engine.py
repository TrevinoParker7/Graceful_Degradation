"""
GracefulOS Dynamic Risk Engine
"""

import math
import time
from typing import Any, Dict, List, Optional
from core.events.bus import event_bus
from core.events.events import RiskSignalEvent, StateTransitionEvent, IncidentCreatedEvent
from core.audit.ledger import audit_ledger
from .signals import get_signal_delta, get_signal_description, RISK_SIGNALS
from .state_machine import DegradationState, determine_state_from_score
from .blast_radius import BlastRadiusTracker, BlastRadiusBudget

class AgentRiskProfile:
    def __init__(self, agent_id: str, initial_score: float = 0.0, budget: Optional[BlastRadiusBudget] = None):
        self.agent_id = agent_id
        self.current_score: float = max(0.0, min(100.0, initial_score))
        self.current_state: DegradationState = determine_state_from_score(self.current_score)
        self.last_updated: float = time.time()
        self.signal_history: List[Dict[str, Any]] = []
        self.blast_tracker = BlastRadiusTracker(agent_id=agent_id, budget=budget)
        self.is_contained: bool = self.current_state == DegradationState.CONTAINED

class RiskEngine:
    def __init__(self, half_life_seconds: float = 300.0):
        self.half_life_seconds = half_life_seconds
        self._profiles: Dict[str, AgentRiskProfile] = {}

    def get_or_create_profile(
        self, agent_id: str, initial_score: float = 0.0, budget: Optional[BlastRadiusBudget] = None
    ) -> AgentRiskProfile:
        if agent_id not in self._profiles:
            self._profiles[agent_id] = AgentRiskProfile(agent_id, initial_score, budget)
        return self._profiles[agent_id]

    def apply_decay(self, profile: AgentRiskProfile) -> float:
        """Apply exponential decay to risk score over elapsed time (if not contained)."""
        if profile.is_contained:
            # Contained agents never automatically decay down; administrator action is required
            return profile.current_score

        now = time.time()
        elapsed = now - profile.last_updated
        if elapsed <= 0:
            return profile.current_score

        # Exponential decay factor
        decay_factor = math.pow(0.5, elapsed / self.half_life_seconds)
        profile.current_score = max(0.0, round(profile.current_score * decay_factor, 2))
        profile.last_updated = now
        profile.current_state = determine_state_from_score(profile.current_score)
        return profile.current_score

    async def ingest_signal(
        self,
        agent_id: str,
        signal_code: str,
        custom_delta: Optional[float] = None,
        reason: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Record an anomaly signal and update agent risk score and degradation state."""
        profile = self.get_or_create_profile(agent_id)
        self.apply_decay(profile)
        
        delta = custom_delta if custom_delta is not None else get_signal_delta(signal_code)
        sig_reason = reason or get_signal_description(signal_code)
        
        score_before = profile.current_score
        state_before = profile.current_state
        
        # Accumulate score
        new_score = min(100.0, max(0.0, score_before + delta))
        profile.current_score = new_score
        profile.last_updated = time.time()
        
        # Determine new state
        new_state = determine_state_from_score(new_score)
        state_changed = new_state != state_before
        profile.current_state = new_state
        if new_state == DegradationState.CONTAINED:
            profile.is_contained = True

        signal_record = {
            "signal_code": signal_code,
            "delta": delta,
            "reason": sig_reason,
            "score_before": score_before,
            "score_after": new_score,
            "timestamp": time.time(),
            "metadata": metadata or {},
        }
        profile.signal_history.append(signal_record)

        # Publish signal event
        await event_bus.publish(
            RiskSignalEvent(
                agent_id=agent_id,
                signal_code=signal_code,
                delta_score=delta,
                reason=sig_reason,
                data={"score_before": score_before, "score_after": new_score},
            )
        )

        # Handle state transition if changed
        incident = None
        if state_changed:
            await event_bus.publish(
                StateTransitionEvent(
                    agent_id=agent_id,
                    previous_state=state_before.value,
                    new_state=new_state.value,
                    risk_score=new_score,
                    trigger_reason=f"Risk signal {signal_code} (+{delta}) -> Score {new_score}",
                )
            )

            # Auto-record incident if escalated into RESTRICTED or higher
            if new_score >= 50.0:
                severity = "CRITICAL" if new_score >= 95 else ("HIGH" if new_score >= 70 else "MEDIUM")
                incident = audit_ledger.record_incident(
                    agent_id=agent_id,
                    severity=severity,
                    trigger_rule=signal_code,
                    risk_score=new_score,
                    summary=f"Agent transitioned from {state_before.value} to {new_state.value} ({sig_reason})",
                    details={"signal": signal_record, "history_len": len(profile.signal_history)},
                )
                await event_bus.publish(
                    IncidentCreatedEvent(
                        agent_id=agent_id,
                        incident_id=incident.incident_id,
                        severity=severity,
                        summary=incident.summary,
                        degradation_state=new_state.value,
                    )
                )

        # Log to ledger
        audit_ledger.append_record(
            agent_id=agent_id,
            event_type="RISK_SIGNAL",
            action_name=signal_code,
            decision="DEGRADE" if state_changed else "MONITOR",
            risk_score_before=score_before,
            risk_score_after=new_score,
            degradation_state=new_state.value,
            details={"signal": signal_record, "state_changed": state_changed},
        )

        return {
            "agent_id": agent_id,
            "signal_code": signal_code,
            "delta": delta,
            "score_before": score_before,
            "score_after": new_score,
            "state_before": state_before.value,
            "state_after": new_state.value,
            "state_changed": state_changed,
            "incident_id": incident.incident_id if incident else None,
        }

    def get_score(self, agent_id: str) -> float:
        profile = self.get_or_create_profile(agent_id)
        return self.apply_decay(profile)

    def get_state(self, agent_id: str) -> DegradationState:
        profile = self.get_or_create_profile(agent_id)
        self.apply_decay(profile)
        return profile.current_state

    def reset_agent(self, agent_id: str, reset_score: float = 0.0) -> None:
        """Administrative reset of an agent profile."""
        profile = self.get_or_create_profile(agent_id)
        profile.current_score = reset_score
        profile.current_state = determine_state_from_score(reset_score)
        profile.is_contained = False
        profile.last_updated = time.time()

# Singleton risk engine instance
risk_engine = RiskEngine()
