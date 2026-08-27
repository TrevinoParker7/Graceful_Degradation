"""
Process Binary Allowlist and Safety Categorization
"""

from typing import List, Set

DEFAULT_PROCESS_ALLOWLIST: Set[str] = {
    "python.exe", "python3.exe", "powershell.exe", "git.exe", "node.exe", "npm.cmd",
    "pytest.exe", "cargo.exe", "rustc.exe", "dotnet.exe", "curl.exe", "tar.exe"
}

FORBIDDEN_BINARIES: Set[str] = {
    "mimikatz.exe", "psexec.exe", "vssadmin.exe", "bcdedit.exe", "certutil.exe", "net.exe"
}
