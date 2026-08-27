"""
Workspace Sandbox Directory Boundary Manager
"""

import os
from pathlib import Path
from typing import Optional, Tuple
from config.settings import config

class SandboxManager:
    def __init__(self, agents_dir: Optional[Path] = None):
        self.agents_dir = agents_dir or config.agents_dir
        self.agents_dir.mkdir(parents=True, exist_ok=True)

    def get_agent_workspace(self, agent_id: str) -> Path:
        ws = self.agents_dir / agent_id
        ws.mkdir(parents=True, exist_ok=True)
        return ws

    def validate_path_in_sandbox(
        self, agent_id: str, target_path: str | Path, allow_read_system: bool = False
    ) -> Tuple[bool, Optional[str]]:
        """
        Ensure requested file path is safely contained within agent workspace,
        preventing directory traversal attacks (.. / symlinks).
        """
        try:
            workspace = self.get_agent_workspace(agent_id).resolve()
            resolved = Path(target_path).resolve()

            # Check if within agent's assigned workspace
            if str(resolved).lower().startswith(str(workspace).lower()):
                return True, None

            # If read system is allowed (e.g. standard program files or test assets in workspace)
            if allow_read_system:
                base_dir = config.data_dir.parent.parent.resolve()
                if str(resolved).lower().startswith(str(base_dir).lower()):
                    return True, None

            return False, f"Path traversal denied: {target_path} is outside workspace {workspace}"
        except Exception as e:
            return False, f"Invalid path resolution: {e}"

sandbox_manager = SandboxManager()
