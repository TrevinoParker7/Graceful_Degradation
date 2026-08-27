# GOS-006: Dynamic Capability Manager & Security Descriptors

## Objective
Implement dynamic capability resolution based on agent degradation states and parse the Windows Agent Security Descriptor (WASD) YAML format.

## Deliverables
1. Capability registry in `core/capabilities/permissions.py` defining granular capabilities (`CAP_FILE_READ`, `CAP_PS_QUERY`, `CAP_NETWORK_CLIENT`, etc.).
2. Dynamic state-to-capability mapper in `core/capabilities/manager.py`.
3. WASD descriptor parser in `core/capabilities/descriptor.py`.
4. Unit tests in `tests/unit/test_capability_manager.py`.
