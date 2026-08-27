"""
Firewall Rule Models and State Tracker
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class FirewallRule(BaseModel):
    rule_name: str
    direction: str = "out"  # in, out
    action: str = "block"   # allow, block
    program_path: Optional[str] = None
    remote_ip: Optional[str] = None
    remote_port: Optional[str] = None
    protocol: str = "any"
    enabled: bool = True
    agent_id: Optional[str] = None
