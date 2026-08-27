"""
GracefulOS Configuration Settings
Windows 11 Local-Only Architecture
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = BASE_DIR / "runtime" / "data"
DEFAULT_LOGS_DIR = BASE_DIR / "runtime" / "logs"
DEFAULT_POLICIES_DIR = BASE_DIR / "policies"
DEFAULT_INCIDENTS_DIR = BASE_DIR / "runtime" / "incidents"
DEFAULT_AGENTS_DIR = BASE_DIR / "runtime" / "agents"
DEFAULT_SNAPSHOTS_DIR = BASE_DIR / "runtime" / "snapshots"
DEFAULT_CANARY_DIR = BASE_DIR / "runtime" / "canary"

class AppConfig(BaseModel):
    app_name: str = "GracefulOS"
    version: str = "0.1.0"
    environment: str = "production-local"
    host: str = "127.0.0.1"
    port: int = 7777
    named_pipe_path: str = r"\\.\pipe\GracefulOS"
    
    # Storage paths
    data_dir: Path = Field(default_factory=lambda: DEFAULT_DATA_DIR)
    logs_dir: Path = Field(default_factory=lambda: DEFAULT_LOGS_DIR)
    policies_dir: Path = Field(default_factory=lambda: DEFAULT_POLICIES_DIR)
    incidents_dir: Path = Field(default_factory=lambda: DEFAULT_INCIDENTS_DIR)
    agents_dir: Path = Field(default_factory=lambda: DEFAULT_AGENTS_DIR)
    snapshots_dir: Path = Field(default_factory=lambda: DEFAULT_SNAPSHOTS_DIR)
    canary_dir: Path = Field(default_factory=lambda: DEFAULT_CANARY_DIR)
    
    # DB configuration
    db_filename: str = "gracefulos.db"
    
    # Risk parameters
    risk_decay_half_life_seconds: int = 300
    containment_threshold: int = 95
    isolated_threshold: int = 85
    read_only_threshold: int = 70
    restricted_threshold: int = 50
    watch_threshold: int = 30
    
    # Security Invariants
    enforce_invariants: bool = True
    offline_only: bool = True

    @property
    def db_path(self) -> Path:
        return self.data_dir / self.db_filename

    def ensure_directories(self) -> None:
        """Create all required local runtime directories."""
        for directory in [
            self.data_dir,
            self.logs_dir,
            self.policies_dir,
            self.incidents_dir,
            self.agents_dir,
            self.snapshots_dir,
            self.canary_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

# Global configuration instance
config = AppConfig()
config.ensure_directories()
