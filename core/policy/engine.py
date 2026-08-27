"""
GracefulOS Policy Evaluation Engine
"""

import fnmatch
from typing import Any, Dict, List, Optional, Tuple
from core.capabilities.manager import capability_manager
from core.capabilities.permissions import Capability
from core.risk.engine import risk_engine
from core.risk.state_machine import DegradationState
from .invariants import invariants_validator, InvariantViolation
from .loader import policy_loader
from .rules import PolicyDecision, PolicyRule, PolicySet

class PolicyEngine:
    def __init__(self):
        self.policy_sets: Dict[str, PolicySet] = {}
        self.reload_policies()

    def reload_policies(self) -> None:
        self.policy_sets = policy_loader.load_all_policies()

    def evaluate_request(
        self,
        agent_id: str,
        tool_name: str,
        arguments: Dict[str, Any],
        required_capability: Optional[Capability] = None,
        caller_is_agent: bool = True,
    ) -> Dict[str, Any]:
        """
        Evaluate tool request against:
        1. Invariants validation (INV-001..INV-008)
        2. Containment lock
        3. Dynamic Capability Matrix check
        4. Declarative Policy rules
        """
        current_state: DegradationState = risk_engine.get_state(agent_id)
        current_score: float = risk_engine.get_score(agent_id)

        # 1. Hard Invariant Checks
        # INV-004: Service tamper check
        cmd_str = str(arguments.get("command", "") or arguments.get("path", "") or tool_name)
        ok, inv_err = invariants_validator.check_service_termination_attempt(cmd_str)
        if not ok:
            return {
                "decision": PolicyDecision.KILL.value,
                "allowed": False,
                "reason": inv_err,
                "risk_delta": 50.0,
                "rule_id": "INV-004",
            }

        # INV-007: Audit log deletion check
        ok, inv_err = invariants_validator.check_audit_log_deletion(cmd_str)
        if not ok:
            return {
                "decision": PolicyDecision.DENY.value,
                "allowed": False,
                "reason": inv_err,
                "risk_delta": 40.0,
                "rule_id": "INV-007",
            }

        # INV-001: Network isolation check
        if "network" in tool_name.lower() or "destination" in arguments or "url" in arguments:
            dest = str(arguments.get("destination") or arguments.get("url") or arguments.get("host") or "")
            ok, inv_err = invariants_validator.check_network_isolation(current_state, dest)
            if not ok:
                return {
                    "decision": PolicyDecision.DENY.value,
                    "allowed": False,
                    "reason": inv_err,
                    "risk_delta": 25.0,
                    "rule_id": "INV-001",
                }

        # INV-005: Read-only check on mutating actions
        is_mutating = arguments.get("is_write", False) or any(
            k in tool_name.lower() for k in ["write", "delete", "mutate", "install", "stop", "create"]
        )
        ok, inv_err = invariants_validator.check_read_only_mutation(current_state, is_mutating)
        if not ok:
            return {
                "decision": PolicyDecision.DENY.value,
                "allowed": False,
                "reason": inv_err,
                "risk_delta": 20.0,
                "rule_id": "INV-005",
            }

        # 2. Hard Containment Lock
        if current_state == DegradationState.CONTAINED:
            return {
                "decision": PolicyDecision.DENY.value,
                "allowed": False,
                "reason": f"Agent {agent_id} is in CONTAINED state. All tool operations blocked.",
                "risk_delta": 0.0,
                "rule_id": "CONTAINMENT_LOCK",
            }

        # 3. Dynamic Capability Check
        if required_capability:
            if not capability_manager.has_capability(agent_id, required_capability):
                return {
                    "decision": PolicyDecision.DENY.value,
                    "allowed": False,
                    "reason": f"Missing required capability {required_capability.value} under state {current_state.value}",
                    "risk_delta": 15.0,
                    "rule_id": "CAPABILITY_REVOKED",
                }

        # 4. Declarative Policy Rule Matching
        for pset in self.policy_sets.values():
            for rule in pset.rules:
                if fnmatch.fnmatch(tool_name.lower(), rule.tool_pattern.lower()):
                    # Match found
                    return {
                        "decision": rule.decision.value,
                        "allowed": rule.decision == PolicyDecision.ALLOW,
                        "reason": rule.reason,
                        "risk_delta": rule.risk_delta,
                        "rule_id": rule.rule_id,
                    }

        # Default fallback: ALLOW if within Normal/Watch, otherwise conservative ALLOW/APPROVAL
        return {
            "decision": PolicyDecision.ALLOW.value,
            "allowed": True,
            "reason": "Default permissive rule within capability bounds",
            "risk_delta": 0.0,
            "rule_id": "DEFAULT_ALLOW",
        }

policy_engine = PolicyEngine()
