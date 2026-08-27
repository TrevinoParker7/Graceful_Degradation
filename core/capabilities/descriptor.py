"""
Windows Agent Security Descriptor (WASD) Schema and Parser
"""

from typing import Any, Dict, List, Optional
import yaml
from pydantic import BaseModel, Field
from .permissions import Capability

class FilesystemPolicy(BaseModel):
    read: bool = True
    write: str = "workspace_only"  # false, workspace_only, full
    delete: bool = False
    allowed_paths: List[str] = Field(default_factory=list)
    denied_paths: List[str] = Field(default_factory=lambda: [
        r"C:\Windows",
        r"C:\Program Files\GracefulOS",
        r"C:\ProgramData\GracefulOS\policies",
        r"C:\ProgramData\GracefulOS\data",
    ])

class PowerShellPolicy(BaseModel):
    query: bool = True
    mutate: bool = False
    install: bool = False
    registry_read: bool = False
    registry_write: bool = False
    service_control: bool = False
    blocked_cmdlets: List[str] = Field(default_factory=lambda: [
        "Remove-Item",
        "Stop-Service",
        "Set-ExecutionPolicy",
        "Invoke-Expression",
        "iex",
    ])

class NetworkPolicy(BaseModel):
    mode: str = "allowlist"  # block, allowlist, open
    allowlist: List[str] = Field(default_factory=lambda: ["127.0.0.1", "localhost"])

class ProcessPolicy(BaseModel):
    max_active: int = 5
    allowlist: List[str] = Field(default_factory=lambda: ["python.exe", "powershell.exe", "git.exe"])

class MCPPolicy(BaseModel):
    allowed_tools: List[str] = Field(default_factory=lambda: ["local_code_search", "ast_analyzer", "local_git_status"])
    mutating_tools: List[str] = Field(default_factory=list)

class AgentCapabilities(BaseModel):
    filesystem: FilesystemPolicy = Field(default_factory=FilesystemPolicy)
    powershell: PowerShellPolicy = Field(default_factory=PowerShellPolicy)
    network: NetworkPolicy = Field(default_factory=NetworkPolicy)
    processes: ProcessPolicy = Field(default_factory=ProcessPolicy)
    secrets: bool = True
    mcp: MCPPolicy = Field(default_factory=MCPPolicy)

class BlastRadiusConfig(BaseModel):
    files_modified: int = 50
    files_deleted: int = 5
    processes_spawned: int = 10
    network_destinations: int = 5
    powershell_commands: int = 50

class WindowsAgentSecurityDescriptor(BaseModel):
    id: str
    name: str = "Agent"
    mission: str = "default_mission"
    model: str = "local-qwen"
    trust: float = 70.0
    degradation: str = "NORMAL"
    capabilities: AgentCapabilities = Field(default_factory=AgentCapabilities)
    blast_radius: BlastRadiusConfig = Field(default_factory=BlastRadiusConfig)

    @classmethod
    def from_yaml(cls, yaml_content: str) -> "WindowsAgentSecurityDescriptor":
        data = yaml.safe_load(yaml_content)
        if "agent" in data:
            data = data["agent"]
        return cls(**data)

    def to_yaml(self) -> str:
        return yaml.dump({"agent": self.dict()}, sort_keys=False)
