"""
Agent Blast Radius Tracker
Enforces quantitative resource and operational impact limits.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict

class BlastRadiusBudget(BaseModel):
    max_files_modified: int = 50
    max_files_deleted: int = 5
    max_processes_spawned: int = 10
    max_network_destinations: int = 5
    max_powershell_commands: int = 50
    max_children_agents: int = 2

class BlastRadiusUsage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    files_modified: int = 0
    files_deleted: int = 0
    processes_spawned: int = 0
    network_destinations: set[str] = Field(default_factory=set)
    powershell_commands: int = 0
    children_agents: int = 0

class BlastRadiusTracker:
    def __init__(self, agent_id: str, budget: Optional[BlastRadiusBudget] = None):
        self.agent_id = agent_id
        self.budget = budget or BlastRadiusBudget()
        self.usage = BlastRadiusUsage()

    def record_file_modification(self) -> bool:
        self.usage.files_modified += 1
        return self.usage.files_modified <= self.budget.max_files_modified

    def record_file_deletion(self) -> bool:
        self.usage.files_deleted += 1
        return self.usage.files_deleted <= self.budget.max_files_deleted

    def record_process_spawn(self) -> bool:
        self.usage.processes_spawned += 1
        return self.usage.processes_spawned <= self.budget.max_processes_spawned

    def record_network_destination(self, destination: str) -> bool:
        self.usage.network_destinations.add(destination)
        return len(self.usage.network_destinations) <= self.budget.max_network_destinations

    def record_powershell_command(self) -> bool:
        self.usage.powershell_commands += 1
        return self.usage.powershell_commands <= self.budget.max_powershell_commands

    def is_within_budget(self) -> tuple[bool, Optional[str]]:
        if self.usage.files_modified > self.budget.max_files_modified:
            return False, f"Files modified ({self.usage.files_modified}) exceeded budget ({self.budget.max_files_modified})"
        if self.usage.files_deleted > self.budget.max_files_deleted:
            return False, f"Files deleted ({self.usage.files_deleted}) exceeded budget ({self.budget.max_files_deleted})"
        if self.usage.processes_spawned > self.budget.max_processes_spawned:
            return False, f"Processes spawned ({self.usage.processes_spawned}) exceeded budget ({self.budget.max_processes_spawned})"
        if len(self.usage.network_destinations) > self.budget.max_network_destinations:
            return False, f"Distinct network destinations ({len(self.usage.network_destinations)}) exceeded budget ({self.budget.max_network_destinations})"
        if self.usage.powershell_commands > self.budget.max_powershell_commands:
            return False, f"PowerShell commands ({self.usage.powershell_commands}) exceeded budget ({self.budget.max_powershell_commands})"
        return True, None

    def get_summary(self) -> Dict[str, Any]:
        return {
            "budget": self.budget.dict(),
            "usage": {
                "files_modified": self.usage.files_modified,
                "files_deleted": self.usage.files_deleted,
                "processes_spawned": self.usage.processes_spawned,
                "network_destinations": list(self.usage.network_destinations),
                "powershell_commands": self.usage.powershell_commands,
                "children_agents": self.usage.children_agents,
            },
        }
