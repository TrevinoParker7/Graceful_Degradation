"""
Forensic Snapshot Generator for Incident Containment
"""

import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from config.settings import config

class ForensicSnapshotService:
    def __init__(self, snapshots_dir: Optional[Path] = None):
        self.snapshots_dir = snapshots_dir or config.snapshots_dir
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    def capture_snapshot(
        self,
        incident_id: str,
        agent_id: str,
        risk_score: float,
        degradation_state: str,
        audit_records: list,
        agent_workspace: Optional[Path] = None,
        extra_telemetry: Optional[Dict[str, Any]] = None,
    ) -> Path:
        """Create a compressed, timestamped forensic zip archive containing all forensic state."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        snapshot_filename = f"forensic_{agent_id}_{incident_id}_{timestamp}.zip"
        snapshot_path = self.snapshots_dir / snapshot_filename

        metadata = {
            "snapshot_version": "1.0",
            "incident_id": incident_id,
            "agent_id": agent_id,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "risk_score": risk_score,
            "degradation_state": degradation_state,
            "extra_telemetry": extra_telemetry or {},
            "audit_record_count": len(audit_records),
        }

        with zipfile.ZipFile(snapshot_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
            # Write metadata manifest
            zipf.writestr("manifest.json", json.dumps(metadata, indent=2))
            
            # Write audit history
            serialized_records = [
                r.dict() if hasattr(r, "dict") else r for r in audit_records
            ]
            zipf.writestr("audit_history.json", json.dumps(serialized_records, indent=2))
            
            # Write workspace contents if provided and exists
            if agent_workspace and agent_workspace.exists():
                for file_path in agent_workspace.rglob("*"):
                    if file_path.is_file():
                        rel_path = file_path.relative_to(agent_workspace)
                        zipf.write(file_path, arcname=f"workspace/{rel_path}")

        return snapshot_path

snapshot_service = ForensicSnapshotService()
