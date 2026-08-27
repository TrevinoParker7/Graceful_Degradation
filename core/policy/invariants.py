"""
Hard Security Invariants Enforcer (INV-001 to INV-008)
"""

from typing import Any, Dict, Optional, Tuple
from core.risk.state_machine import DegradationState

class InvariantViolation(Exception):
    def __init__(self, invariant_id: str, message: str):
        super().__init__(f"[{invariant_id}] Invariant Violation: {message}")
        self.invariant_id = invariant_id
        self.message = message

class InvariantsValidator:
    """
    Validates hard invariant rules:
    - INV-001: An isolated agent cannot access the external network.
    - INV-002: An agent cannot modify its own risk score.
    - INV-003: An agent cannot grant itself capabilities.
    - INV-004: An agent cannot stop the GracefulOS service.
    - INV-005: READ_ONLY agents cannot modify protected files.
    - INV-006: A contained agent has no surviving uncontrolled child processes.
    - INV-007: An agent cannot erase its security audit history.
    - INV-008: Guardian AI failure cannot increase permissions.
    """

    @staticmethod
    def check_network_isolation(state: DegradationState, destination: str) -> Tuple[bool, Optional[str]]:
        """INV-001: An isolated agent cannot access the external network."""
        if state in (DegradationState.ISOLATED, DegradationState.CONTAINED):
            if destination not in ("127.0.0.1", "localhost"):
                return False, "INV-001: Isolated/Contained agent attempted external network access."
        return True, None

    @staticmethod
    def check_agent_risk_mutation(caller_is_agent: bool, target_field: str) -> Tuple[bool, Optional[str]]:
        """INV-002: An agent cannot modify its own risk score."""
        if caller_is_agent and "risk" in target_field.lower():
            return False, "INV-002: Untrusted agent attempted to directly mutate risk score."
        return True, None

    @staticmethod
    def check_agent_capability_grant(caller_is_agent: bool) -> Tuple[bool, Optional[str]]:
        """INV-003: An agent cannot grant itself capabilities."""
        if caller_is_agent:
            return False, "INV-003: Untrusted agent attempted to self-grant capabilities."
        return True, None

    @staticmethod
    def check_service_termination_attempt(command_or_action: str) -> Tuple[bool, Optional[str]]:
        """INV-004: An agent cannot stop the GracefulOS service."""
        forbidden = ["stop-service gracefulos", "taskkill /f /im gracefulos", "kill gracefulos"]
        normalized = command_or_action.lower().replace(" ", "")
        for pattern in forbidden:
            if pattern.replace(" ", "") in normalized:
                return False, "INV-004: Agent attempted to stop or kill the GracefulOS service."
        return True, None

    @staticmethod
    def check_read_only_mutation(state: DegradationState, is_write_action: bool) -> Tuple[bool, Optional[str]]:
        """INV-005: READ_ONLY agents cannot modify files or execute state changes."""
        if state in (DegradationState.READ_ONLY, DegradationState.ISOLATED, DegradationState.CONTAINED) and is_write_action:
            return False, "INV-005: READ_ONLY/ISOLATED/CONTAINED agent attempted mutating filesystem/process action."
        return True, None

    @staticmethod
    def check_audit_log_deletion(target_path_or_query: str) -> Tuple[bool, Optional[str]]:
        """INV-007: An agent cannot erase its security audit history."""
        normalized = target_path_or_query.lower()
        if "gracefulos.db" in normalized or "delete from audit" in normalized or "drop table" in normalized:
            return False, "INV-007: Agent attempted to delete, drop, or erase audit ledger records."
        return True, None

    @staticmethod
    def check_guardian_fallback_permissions(guardian_succeeded: bool, requested_elevated: bool) -> Tuple[bool, Optional[str]]:
        """INV-008: Guardian AI failure cannot increase permissions."""
        if not guardian_succeeded and requested_elevated:
            return False, "INV-008: Guardian AI offline/failed; cannot grant elevated privileges."
        return True, None

invariants_validator = InvariantsValidator()
