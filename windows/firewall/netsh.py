"""
Windows Defender Firewall Controller via netsh / PowerShell
"""

import subprocess
import sys
from typing import Dict, List, Optional
from .rules import FirewallRule

class WindowsFirewallManager:
    def __init__(self):
        self._is_windows = sys.platform == "win32"
        self._active_rules: Dict[str, FirewallRule] = {}

    def block_agent_network(self, agent_id: str, program_path: Optional[str] = None) -> bool:
        """Create a blocking outbound firewall rule for an agent in ISOLATED / CONTAINED state."""
        rule_name = f"GracefulOS_Block_{agent_id}"
        rule = FirewallRule(
            rule_name=rule_name,
            direction="out",
            action="block",
            program_path=program_path,
            agent_id=agent_id,
            enabled=True,
        )
        self._active_rules[rule_name] = rule

        if not self._is_windows:
            return True

        try:
            if program_path:
                cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=out action=block program="{program_path}" enable=yes'
            else:
                cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=out action=block enable=yes'
            
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            return True
        except Exception:
            return False

    def remove_agent_block(self, agent_id: str) -> bool:
        rule_name = f"GracefulOS_Block_{agent_id}"
        self._active_rules.pop(rule_name, None)

        if not self._is_windows:
            return True

        try:
            cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            return True
        except Exception:
            return False

    def get_active_rules(self) -> List[FirewallRule]:
        return list(self._active_rules.values())

firewall_manager = WindowsFirewallManager()
