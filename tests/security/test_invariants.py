"""
Security Invariants Test Suite (INV-001 through INV-008)
"""

import pytest
from core.policy.invariants import invariants_validator
from core.risk.state_machine import DegradationState

def test_inv_001_network_isolation():
    # ISOLATED state cannot access external network
    ok, err = invariants_validator.check_network_isolation(DegradationState.ISOLATED, "https://api.adversary.com")
    assert ok is False
    assert "INV-001" in err

    # Localhost allowed
    ok_local, _ = invariants_validator.check_network_isolation(DegradationState.ISOLATED, "127.0.0.1")
    assert ok_local is True

def test_inv_002_agent_risk_mutation():
    ok, err = invariants_validator.check_agent_risk_mutation(caller_is_agent=True, target_field="risk_score")
    assert ok is False
    assert "INV-002" in err

def test_inv_003_agent_capability_grant():
    ok, err = invariants_validator.check_agent_capability_grant(caller_is_agent=True)
    assert ok is False
    assert "INV-003" in err

def test_inv_004_service_termination_defense():
    ok, err = invariants_validator.check_service_termination_attempt("Stop-Service GracefulOS")
    assert ok is False
    assert "INV-004" in err

def test_inv_005_read_only_mutation_defense():
    ok, err = invariants_validator.check_read_only_mutation(DegradationState.READ_ONLY, is_write_action=True)
    assert ok is False
    assert "INV-005" in err

def test_inv_007_audit_log_deletion_defense():
    ok, err = invariants_validator.check_audit_log_deletion("del gracefulos.db")
    assert ok is False
    assert "INV-007" in err

def test_inv_008_guardian_failure_fail_secure():
    # Guardian failure cannot grant elevated permissions
    ok, err = invariants_validator.check_guardian_fallback_permissions(guardian_succeeded=False, requested_elevated=True)
    assert ok is False
    assert "INV-008" in err
