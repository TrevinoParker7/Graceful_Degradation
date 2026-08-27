# GOS-012: Windows Security Enforcement & Invariant Tests

## Objective
Build and run the full suite of Windows enforcement tests, adversarial tests, chaos fault injection tests, and invariant validation tests across both OS and UI planes.

## Deliverables
1. `tests/windows/` (Job object containment, ACL blocks, firewall sync).
2. `tests/security/` (INV-001..INV-008 invariant tests, blast radius tests, canary tests).
3. `tests/adversarial/` (Prompt injection, command evasion, privilege escalation).
4. `tests/chaos/` (Fail-secure tests on simulated component crashes).
5. Flagship demo automated verification script.
