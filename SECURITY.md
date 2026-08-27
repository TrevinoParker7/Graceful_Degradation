# Security Policy

## Reporting Security Vulnerabilities

GracefulOS is a security operating layer designed to enforce boundaries around autonomous AI agents. If you discover a vulnerability in GracefulOS itself, we ask you to report it locally or via secure disclosure channels.

## Core Security Invariants

GracefulOS maintains eight non-negotiable security invariants:

1. **INV-001**: An isolated agent cannot access the external network.
2. **INV-002**: An agent cannot modify its own risk score.
3. **INV-003**: An agent cannot grant itself capabilities.
4. **INV-004**: An agent cannot stop the GracefulOS service.
5. **INV-005**: READ_ONLY agents cannot modify protected files.
6. **INV-006**: A contained agent has no surviving uncontrolled child processes.
7. **INV-007**: An agent cannot erase its security audit history.
8. **INV-008**: Guardian AI failure cannot increase permissions.

## Self-Protection Boundary

All GracefulOS control plane components, databases, policies, and binaries are protected from untrusted agent modifications. Agents run under lower integrity tokens or AppContainers and do not possess permissions to write to control plane state directories or kill the host service.
