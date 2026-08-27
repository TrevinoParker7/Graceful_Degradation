# GOS-011: Granular PowerShell & Tool Brokers

## Objective
Implement security brokers mediating all OS operations: PowerShell AST parsing, Process execution allowlisting, Filesystem path containment, Network firewall synchronization, MCP schema filtering, and DPAPI Secret dispensing.

## Deliverables
1. `brokers/powershell/` AST command safety analyzer and execution wrapper in Job Object.
2. `brokers/filesystem/` sandbox boundary checker and NTFS ACL manager.
3. `brokers/network/` firewall sync and destination allowlist broker.
4. `brokers/mcp/` local MCP schema gateway.
5. `brokers/secrets/` DPAPI / ephemeral token dispenser and canary tripwire manager.
6. Broker unit & integration tests.
