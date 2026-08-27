"""
Dynamic Capability Manager
Calculates the intersection of agent's assigned profile and current degradation state capabilities.
"""

from typing import Dict, Optional, Set
from .permissions import Capability, STATE_CAPABILITIES
from .descriptor import WindowsAgentSecurityDescriptor
from core.risk.engine import risk_engine
from core.risk.state_machine import DegradationState

class CapabilityManager:
    def __init__(self):
        self._descriptors: Dict[str, WindowsAgentSecurityDescriptor] = {}

    def register_agent_descriptor(self, descriptor: WindowsAgentSecurityDescriptor) -> None:
        self._descriptors[descriptor.id] = descriptor

    def get_descriptor(self, agent_id: str) -> Optional[WindowsAgentSecurityDescriptor]:
        return self._descriptors.get(agent_id)

    def get_effective_capabilities(self, agent_id: str) -> Set[Capability]:
        """
        Calculate effective capability set.
        Effective = (Capabilities granted in WASD) INTERSECT (Capabilities permitted in Current Degradation State).
        """
        current_state: DegradationState = risk_engine.get_state(agent_id)
        state_allowed = STATE_CAPABILITIES.get(current_state.value, set())
        
        descriptor = self._descriptors.get(agent_id)
        if not descriptor:
            # If no custom descriptor, return baseline allowed by state
            return set(state_allowed)

        # Build declared capability set from descriptor
        declared = set()
        caps = descriptor.capabilities
        
        # Filesystem
        if caps.filesystem.read:
            declared.add(Capability.FILE_READ)
        if caps.filesystem.write in ("workspace_only", "full"):
            declared.add(Capability.FILE_WRITE)
        if caps.filesystem.delete:
            declared.add(Capability.FILE_DELETE)

        # PowerShell
        if caps.powershell.query:
            declared.add(Capability.PS_QUERY)
        if caps.powershell.mutate:
            declared.add(Capability.PS_MUTATE)
        if caps.powershell.install:
            declared.add(Capability.PS_INSTALL)
        if caps.powershell.registry_read:
            declared.add(Capability.PS_REGISTRY_READ)
        if caps.powershell.registry_write:
            declared.add(Capability.PS_REGISTRY_WRITE)
        if caps.powershell.service_control:
            declared.add(Capability.PS_SERVICE_CONTROL)

        # Network
        if caps.network.mode == "open":
            declared.add(Capability.NETWORK_CLIENT)
            declared.add(Capability.NETWORK_ALLOWLIST)
        elif caps.network.mode == "allowlist":
            declared.add(Capability.NETWORK_ALLOWLIST)

        # Processes
        if caps.processes.max_active > 0:
            declared.add(Capability.PROCESS_QUERY)
            declared.add(Capability.PROCESS_SPAWN)

        # MCP
        if caps.mcp.allowed_tools:
            declared.add(Capability.MCP_INVOKE)
        if caps.mcp.mutating_tools:
            declared.add(Capability.MCP_MUTATING)

        # Secrets
        if caps.secrets:
            declared.add(Capability.SECRETS_EPHEMERAL)

        # Intersection
        effective = declared.intersection(state_allowed)
        return effective

    def has_capability(self, agent_id: str, capability: Capability) -> bool:
        effective = self.get_effective_capabilities(agent_id)
        return capability in effective

# Singleton capability manager
capability_manager = CapabilityManager()
