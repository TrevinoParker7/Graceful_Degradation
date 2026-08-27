"""
PowerShell Command Safety and AST Analyzer
"""

import re
from typing import Any, Dict, List, Tuple
from core.capabilities.permissions import Capability

QUERY_CMDLETS = {
    "get-service", "get-process", "get-childitem", "dir", "ls", "get-item",
    "get-content", "cat", "type", "test-path", "get-command", "get-help",
    "get-location", "pwd", "get-date", "select-string", "grep", "measure-object",
}

MUTATING_CMDLETS = {
    "set-item", "new-item", "remove-item", "rm", "del", "erase", "move-item", "mv",
    "copy-item", "cp", "rename-item", "set-content", "add-content", "clear-content",
    "out-file", "set-itemproperty", "new-itemproperty", "remove-itemproperty",
}

INSTALL_CMDLETS = {
    "npm", "pip", "winget", "choco", "install-package", "install-module", "dotnet",
}

REGISTRY_READ_PATTERNS = ["hklm:", "hkcu:", "registry::", "get-itemproperty"]
REGISTRY_WRITE_PATTERNS = ["set-itemproperty", "new-itemproperty", "remove-itemproperty"]
SERVICE_CONTROL_CMDLETS = {"start-service", "stop-service", "restart-service", "set-service"}

DANGEROUS_PATTERNS = [
    (r"remove-item\s+c:\\users", 50.0, "Recursive deletion targeting user profiles"),
    (r"remove-item\s+c:\\windows", 60.0, "Deletion targeting Windows system directory"),
    (r"format\s+[a-z]:", 80.0, "Disk formatting command"),
    (r"-\s*enc(odedcommand)?\s+[a-z0-9+/=]{10,}", 35.0, "Obfuscated Base64 PowerShell execution"),
    (r"invoke-expression|iex\s+", 30.0, "Dynamic arbitrary code evaluation (IEX)"),
    (r"stop-service\s+gracefulos", 50.0, "Attempt to terminate GracefulOS security service"),
    (r"taskkill\s+/f\s+/im\s+gracefulos", 50.0, "Attempt to kill GracefulOS process"),
]

class PowerShellAnalyzer:
    def analyze_command(self, command: str) -> Dict[str, Any]:
        """Inspect command tokens, categorize required capabilities, and score potential risk."""
        cmd_lower = command.lower().strip()
        
        # Check explicit high-danger patterns
        for pattern, risk_delta, reason in DANGEROUS_PATTERNS:
            if re.search(pattern, cmd_lower):
                return {
                    "is_dangerous": True,
                    "risk_delta": risk_delta,
                    "reason": reason,
                    "required_capability": Capability.PS_MUTATE,
                    "is_mutating": True,
                }

        # Identify required capability
        tokens = re.split(r"[\s|;&]+", cmd_lower)
        first_token = tokens[0] if tokens else ""

        if any(sc in cmd_lower for sc in SERVICE_CONTROL_CMDLETS):
            return {
                "is_dangerous": False,
                "risk_delta": 25.0,
                "reason": "Windows Service Control cmdlet requested",
                "required_capability": Capability.PS_SERVICE_CONTROL,
                "is_mutating": True,
            }

        if any(reg in cmd_lower for reg in REGISTRY_WRITE_PATTERNS):
            return {
                "is_dangerous": False,
                "risk_delta": 20.0,
                "reason": "Registry write operation requested",
                "required_capability": Capability.PS_REGISTRY_WRITE,
                "is_mutating": True,
            }

        if any(reg in cmd_lower for reg in REGISTRY_READ_PATTERNS):
            return {
                "is_dangerous": False,
                "risk_delta": 5.0,
                "reason": "Registry query requested",
                "required_capability": Capability.PS_REGISTRY_READ,
                "is_mutating": False,
            }

        if first_token in INSTALL_CMDLETS or any(ic in cmd_lower for ic in INSTALL_CMDLETS):
            return {
                "is_dangerous": False,
                "risk_delta": 10.0,
                "reason": "Package installation or tooling build operation",
                "required_capability": Capability.PS_INSTALL,
                "is_mutating": True,
            }

        if first_token in MUTATING_CMDLETS or any(mc in tokens for mc in MUTATING_CMDLETS):
            return {
                "is_dangerous": False,
                "risk_delta": 15.0,
                "reason": "Filesystem or state mutation cmdlet",
                "required_capability": Capability.PS_MUTATE,
                "is_mutating": True,
            }

        # Baseline read/query
        return {
            "is_dangerous": False,
            "risk_delta": 0.0,
            "reason": "Standard read-only query command",
            "required_capability": Capability.PS_QUERY,
            "is_mutating": False,
        }

powershell_analyzer = PowerShellAnalyzer()
