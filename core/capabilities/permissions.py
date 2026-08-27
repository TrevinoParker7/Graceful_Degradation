"""
Granular Capability Definitions for GracefulOS
"""

from enum import Enum
from typing import Dict, List, Set

class Capability(str, Enum):
    # Filesystem capabilities
    FILE_READ = "CAP_FILE_READ"
    FILE_WRITE = "CAP_FILE_WRITE"
    FILE_DELETE = "CAP_FILE_DELETE"
    FILE_EXECUTE = "CAP_FILE_EXECUTE"
    
    # PowerShell capabilities
    PS_QUERY = "CAP_PS_QUERY"                # Get-*, Test-*
    PS_MUTATE = "CAP_PS_MUTATE"              # Set-*, New-*, Remove-*
    PS_INSTALL = "CAP_PS_INSTALL"            # npm, pip, winget
    PS_REGISTRY_READ = "CAP_PS_REGISTRY_READ"# Get-ItemProperty HKLM/HKCU
    PS_REGISTRY_WRITE = "CAP_PS_REGISTRY_WRITE"
    PS_SERVICE_CONTROL = "CAP_PS_SERVICE_CONTROL" # Start-Service, Stop-Service
    
    # Network capabilities
    NETWORK_CLIENT = "CAP_NETWORK_CLIENT"
    NETWORK_ALLOWLIST = "CAP_NETWORK_ALLOWLIST"
    NETWORK_SERVER = "CAP_NETWORK_SERVER"
    
    # Process management
    PROCESS_SPAWN = "CAP_PROCESS_SPAWN"
    PROCESS_QUERY = "CAP_PROCESS_QUERY"
    
    # MCP (Model Context Protocol)
    MCP_INVOKE = "CAP_MCP_INVOKE"
    MCP_MUTATING = "CAP_MCP_MUTATING"
    
    # Secret Management
    SECRETS_EPHEMERAL = "CAP_SECRETS_EPHEMERAL"
    SECRETS_PERSISTENT = "CAP_SECRETS_PERSISTENT"

# Degradation State Default Allowed Capability Sets
STATE_CAPABILITIES: Dict[str, Set[Capability]] = {
    "NORMAL": {
        Capability.FILE_READ,
        Capability.FILE_WRITE,
        Capability.FILE_DELETE,
        Capability.PS_QUERY,
        Capability.PS_MUTATE,
        Capability.PS_INSTALL,
        Capability.PS_REGISTRY_READ,
        Capability.NETWORK_CLIENT,
        Capability.NETWORK_ALLOWLIST,
        Capability.PROCESS_SPAWN,
        Capability.PROCESS_QUERY,
        Capability.MCP_INVOKE,
        Capability.MCP_MUTATING,
        Capability.SECRETS_EPHEMERAL,
    },
    "WATCH": {
        Capability.FILE_READ,
        Capability.FILE_WRITE,
        Capability.FILE_DELETE,
        Capability.PS_QUERY,
        Capability.PS_MUTATE,
        Capability.PS_INSTALL,
        Capability.PS_REGISTRY_READ,
        Capability.NETWORK_CLIENT,
        Capability.NETWORK_ALLOWLIST,
        Capability.PROCESS_SPAWN,
        Capability.PROCESS_QUERY,
        Capability.MCP_INVOKE,
        Capability.MCP_MUTATING,
        Capability.SECRETS_EPHEMERAL,
    },
    "RESTRICTED": {
        Capability.FILE_READ,
        Capability.FILE_WRITE,  # Limited to workspace
        Capability.PS_QUERY,
        Capability.PS_REGISTRY_READ,
        Capability.NETWORK_ALLOWLIST, # Strict allowlist only
        Capability.PROCESS_QUERY,
        Capability.MCP_INVOKE,        # Approved non-mutating tools only
    },
    "READ_ONLY": {
        Capability.FILE_READ,
        Capability.PROCESS_QUERY,
        Capability.MCP_INVOKE,        # Read-only tools only
    },
    "ISOLATED": {
        Capability.FILE_READ,         # Sandbox only
        Capability.PROCESS_QUERY,
    },
    "CONTAINED": set(),               # Zero capabilities granted
}
