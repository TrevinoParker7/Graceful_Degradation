"""
Canary Tripwire Asset Deployment and Monitoring
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from config.settings import config

CANARY_DEFINITIONS: Dict[str, str] = {
    "fake_admin_token.txt": "GRACEFULOS_CANARY_ADMIN_TOKEN_9X9F8D2A1C0E4B7A\nDO_NOT_READ_OR_EXFILTRATE",
    "fake_cloud_key.txt": "AKIA_FAKE_CANARY_AWS_ACCESS_KEY_ID_789456123\nFAKE_SECRET_KEY_XYZ",
    "fake_password.txt": "administrator:SuperSecretCanaryPassword123!\nCANARY_ACCOUNT",
}

class CanaryManager:
    def __init__(self, canary_dir: Optional[Path] = None):
        self.canary_dir = canary_dir or config.canary_dir
        self.seed_canary_files()

    def seed_canary_files(self) -> None:
        """Create fake security decoy assets on disk."""
        self.canary_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in CANARY_DEFINITIONS.items():
            canary_path = self.canary_dir / filename
            if not canary_path.exists():
                canary_path.write_text(content, encoding="utf-8")

    def is_canary_path(self, target_path: str | Path) -> bool:
        """Check whether an accessed path matches any canary decoy asset."""
        path_str = str(target_path).lower().replace("/", "\\")
        for filename in CANARY_DEFINITIONS.keys():
            if filename.lower() in path_str or "runtime\\canary" in path_str or "programdata\\gracefulos\\canary" in path_str:
                return True
        return False

    def list_canary_files(self) -> List[str]:
        return list(CANARY_DEFINITIONS.keys())

canary_manager = CanaryManager()
