"""
Filesystem Path Canonicalization and Access Checker
"""

import os
from pathlib import Path
from typing import Tuple, Optional
from windows.filesystem.canary import canary_manager
from windows.filesystem.sandbox import sandbox_manager

PROTECTED_PATHS = [
    r"C:\Windows\System32",
    r"C:\Program Files\GracefulOS",
    r"C:\ProgramData\GracefulOS\policies",
    r"C:\ProgramData\GracefulOS\data",
]

class PathGuard:
    def check_path_access(
        self, agent_id: str, target_path: str | Path, is_write: bool = False
    ) -> Tuple[bool, bool, Optional[str]]:
        """
        Returns (allowed, is_canary_hit, reason).
        """
        # Check canary tripwire
        if canary_manager.is_canary_path(target_path):
            return False, True, "Canary credential asset accessed"

        target_str = str(target_path).lower().replace("/", "\\")

        # Check protected paths
        for p in PROTECTED_PATHS:
            if p.lower() in target_str:
                return False, False, f"Direct access to protected system path {p} is forbidden"

        # Check sandbox containment if write
        if is_write:
            ok, err = sandbox_manager.validate_path_in_sandbox(agent_id, target_path)
            if not ok:
                return False, False, err

        return True, False, None

path_guard = PathGuard()
