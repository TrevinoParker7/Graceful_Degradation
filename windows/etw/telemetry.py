"""
Event Tracing for Windows (ETW) Telemetry Event Models
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class EtwEvent(BaseModel):
    provider_name: str
    event_id: int
    process_id: int
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_name: str
    details: Dict[str, Any] = Field(default_factory=dict)
