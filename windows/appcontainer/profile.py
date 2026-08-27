"""
AppContainer Profile Definitions and Sid Resolver for Windows 11
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class AppContainerProfile(BaseModel):
    container_name: str
    display_name: str
    description: str = "GracefulOS AppContainer Isolation Sandbox"
    capabilities: List[str] = Field(default_factory=list) # e.g. ["internetClient"]
    workspace_path: Optional[str] = None
    sid: Optional[str] = None
