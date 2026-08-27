# GOS-005: Declarative YAML Policy Engine & Invariants

## Objective
Implement the declarative policy engine that parses security profiles, evaluates tool requests against allowlists/denylists, and validates hard security invariants (`INV-001` through `INV-008`).

## Deliverables
1. Policy parser in `core/policy/loader.py` reading YAML policy files from `policies/`.
2. Rule evaluator in `core/policy/engine.py` determining `ALLOW`, `DENY`, `REQUIRES_APPROVAL`, or `DEGRADE`.
3. Invariant enforcer in `core/policy/invariants.py`.
4. Unit tests in `tests/unit/test_policy_engine.py` and invariant tests in `tests/security/test_invariants.py`.
