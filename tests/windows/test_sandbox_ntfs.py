"""
Workspace Sandbox Directory and NTFS ACL Tests
"""

import pytest
from pathlib import Path
from windows.filesystem.sandbox import sandbox_manager
from windows.filesystem.ntfs_acl import ntfs_acl_manager

def test_sandbox_path_containment():
    agent_id = "test-agent-sandbox"
    ws = sandbox_manager.get_agent_workspace(agent_id)
    
    # 1. Valid inside workspace
    valid_file = ws / "script.py"
    ok, err = sandbox_manager.validate_path_in_sandbox(agent_id, valid_file)
    assert ok is True

    # 2. Path traversal attack attempt
    traversal_path = ws / ".." / ".." / "Windows" / "System32" / "cmd.exe"
    ok, err = sandbox_manager.validate_path_in_sandbox(agent_id, traversal_path)
    assert ok is False
    assert "Path traversal denied" in err

def test_ntfs_acl_application(tmp_path):
    sub_dir = tmp_path / "acl_test_folder"
    sub_dir.mkdir(parents=True, exist_ok=True)
    res = ntfs_acl_manager.apply_workspace_acls(sub_dir, read_only=True)
    assert res is True
    # Reset permissions back to normal inheritance
    import subprocess
    subprocess.run(f'icacls "{sub_dir}" /reset /t /c /q', shell=True, capture_output=True)
