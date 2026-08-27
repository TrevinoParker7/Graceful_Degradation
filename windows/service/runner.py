"""
GracefulOS Core Service Runner
Unified control plane daemon orchestrating Event Bus, Risk Engine, Gateway, and Windows Enforcement.
"""

import asyncio
import logging
from config.settings import config
from core.events.bus import event_bus
from core.audit.ledger import audit_ledger
from core.policy.engine import policy_engine
from windows.filesystem.canary import canary_manager

logger = logging.getLogger("GracefulOSCore")

class GracefulOSCoreService:
    def __init__(self):
        self.is_running = False

    async def start(self) -> None:
        logger.info("Initializing GracefulOS Core Windows Service...")
        config.ensure_directories()
        canary_manager.seed_canary_files()
        policy_engine.reload_policies()
        self.is_running = True
        logger.info(f"GracefulOS Core Service running. Localhost API: http://{config.host}:{config.port}")

    async def stop(self) -> None:
        logger.info("Stopping GracefulOS Core Service...")
        self.is_running = False

core_service = GracefulOSCoreService()
