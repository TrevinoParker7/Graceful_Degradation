"""
Windows NTFS ACL Management and Workspace Boundary Enforcement
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

class NtfsAclManager:
    def __init__(self):
        self._is_windows = sys.platform == "win32"

    def apply_workspace_acls(self, workspace_path: Path, read_only: bool = False) -> bool:
        """Apply NTFS ACLs using icacls to restrict write or lock down permissions."""
        if not self._is_windows or not workspace_path.exists():
            return True

        try:
            user = os.environ.get("USERNAME", "")
            if read_only:
                # Deny write and delete with container & object inheritance for current user and Everyone
                if user:
                    cmd_user = f'icacls "{workspace_path}" /deny {user}:(OI)(CI)(W,D) /t /c /q'
                    subprocess.run(cmd_user, shell=True, capture_output=True, timeout=5)
                cmd = f'icacls "{workspace_path}" /deny *S-1-1-0:(OI)(CI)(W,D) /t /c /q'
                subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            else:
                if user:
                    cmd_user = f'icacls "{workspace_path}" /grant {user}:(OI)(CI)(M) /t /c /q'
                    subprocess.run(cmd_user, shell=True, capture_output=True, timeout=5)
                cmd = f'icacls "{workspace_path}" /grant *S-1-1-0:(OI)(CI)(M) /t /c /q'
                subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            
            return True
        except Exception:
            return False

    def protect_control_plane_files(self, control_plane_dir: Path) -> bool:
        """Ensure control plane runtime data cannot be modified by low-integrity agents."""
        if not self._is_windows or not control_plane_dir.exists():
            return True

        try:
            # Deny write for untrusted / low integrity SIDs
            cmd = f'icacls "{control_plane_dir}" /inheritance:r /grant:r Administrators:(OI)(CI)F /grant:r SYSTEM:(OI)(CI)F'
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            return True
        except Exception:
            return False

ntfs_acl_manager = NtfsAclManager()
