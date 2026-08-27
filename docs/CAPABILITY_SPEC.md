# GracefulOS Capability & Security Descriptor Specification

## 1. Granular Capability Model

GracefulOS avoids binary permission flags in favor of granular capabilities:

- `CAP_FILE_READ`: Read access to non-sensitive filesystem paths.
- `CAP_FILE_WRITE`: Write access within designated workspace directory.
- `CAP_FILE_DELETE`: Deletion of files within workspace (subject to blast radius limits).
- `CAP_PS_QUERY`: Safe read-only PowerShell commands (e.g. `Get-Service`, `Get-ChildItem`, `Get-Process`).
- `CAP_PS_MUTATE`: Mutating PowerShell commands (e.g. `Set-ItemProperty`, `New-Item`).
- `CAP_PS_INSTALL`: Package installation via `npm`, `pip`, `winget`.
- `CAP_PS_REGISTRY_READ`: Querying non-sensitive Windows registry keys.
- `CAP_PS_REGISTRY_WRITE`: Modifying Windows registry keys.
- `CAP_PS_SERVICE_CONTROL`: Starting, stopping, or configuring Windows services.
- `CAP_NETWORK_CLIENT`: Standard HTTP/HTTPS network requests.
- `CAP_NETWORK_ALLOWLIST`: Network requests restricted to policy allowlisted domains/IPs.
- `CAP_PROCESS_SPAWN`: Spawning child processes inside the assigned Job Object.
- `CAP_MCP_INVOKE`: Invoking approved MCP tools.
- `CAP_SECRETS_EPHEMERAL`: Requesting short-lived scoped secrets from Secret Broker.

---

## 2. Windows Agent Security Descriptor (WASD) Schema

Each agent is defined by a declarative WASD YAML descriptor:

```yaml
agent:
  id: "agent-coder-001"
  name: "Local Code Assistant"
  mission: "fix_local_project"
  model: "local-qwen"
  trust: 70
  degradation: "NORMAL"
  
  capabilities:
    filesystem:
      read: true
      write: "workspace_only"
      delete: false
    powershell:
      query: true
      mutate: false
      install: true
      registry_read: false
      registry_write: false
      service_control: false
    network:
      mode: "allowlist"
      allowlist:
        - "127.0.0.1"
        - "pypi.org"
        - "github.com"
    processes:
      max_active: 5
      allowlist:
        - "python.exe"
        - "git.exe"
        - "pytest.exe"
    secrets:
      access: false
    mcp:
      allowed_tools:
        - "local-code-search"
        - "ast-parser"

  blast_radius:
    files_modified: 50
    files_deleted: 5
    processes_spawned: 10
    network_destinations: 5
    powershell_commands: 50
```
