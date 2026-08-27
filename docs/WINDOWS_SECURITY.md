# GracefulOS Windows 11 Security Integration

## 1. Win32 Job Objects
Job Objects allow GracefulOS to group processes into manageable units.
- **Process Grouping**: When an agent launches, a dedicated Job Object is instantiated. All child processes spawned (e.g. `powershell.exe`, compiler tools, Python workers) are automatically assigned to the same Job Object.
- **Resource Limits**:
  - `JobObjectBasicLimitInformation`: Active process limit, CPU rate control, per-job memory limits.
  - `JobObjectExtendedLimitInformation`: Maximum commit limit preventing OOM exhaustion.
- **Instant Kill Switch**: Invoking `TerminateJobObject(hJob, exitCode)` terminates all processes in the tree synchronously, eliminating runaway or detached child processes.

## 2. Restricted Tokens & Low Integrity
- GracefulOS uses `CreateRestrictedToken` to strip administrative privileges (`SeDebugPrivilege`, `SeImpersonatePrivilege`, etc.) and convert security groups into deny-only SIDs.
- Agent processes execute under Low Integrity Level (`Mandatory Integrity Control`), preventing agents from sending Windows messages (UIPI) or writing to Medium/High integrity files and registry keys.

## 3. AppContainer Isolation
- For maximum containment of untrusted agents, AppContainer profiles are generated via `CreateAppContainerProfile`.
- Capabilities granted are explicitly enumerated (e.g. `internetClient` is omitted unless explicitly permitted in NORMAL state).
- The agent workspace directory receives explicit ACEs granted to the AppContainer SID.

## 4. NTFS ACLs & Sandbox Directories
- Workspaces are constrained to designated sandboxes (`runtime/agents/<agent-id>/` or `C:\ProgramData\GracefulOS\agents\<agent-id>\`).
- Canary files (`fake_admin_token.txt`, `fake_cloud_key.txt`, `fake_password.txt`) are deployed outside or within decoy folders to act as tripwires.

## 5. Windows Defender Firewall Integration
- GracefulOS programmatically manages firewall rules via `netsh advfirewall firewall` or PowerShell `NetSecurity` cmdlets to enforce allowlisting and complete network isolation for agents in `RESTRICTED`, `ISOLATED`, or `CONTAINED` states.

## 6. Event Tracing for Windows (ETW)
- GracefulOS integrates ETW providers (`Microsoft-Windows-Kernel-Process`, `Microsoft-Windows-PowerShell`) to independently observe process spawns, command lines, and network connections without relying on agent-reported telemetry.
