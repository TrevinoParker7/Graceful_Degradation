"""
ETW Telemetry Listener & Parser
"""

import sys
from typing import Callable, List, Optional
from .telemetry import EtwEvent

class EtwListener:
    def __init__(self):
        self.is_running: bool = False
        self.subscribers: List[Callable[[EtwEvent], None]] = []
        self._is_windows = sys.platform == "win32"

    def subscribe(self, callback: Callable[[EtwEvent], None]) -> None:
        self.subscribers.append(callback)

    def record_simulated_etw(self, event: EtwEvent) -> None:
        for sub in self.subscribers:
            try:
                sub(event)
            except Exception:
                pass

etw_listener = EtwListener()
