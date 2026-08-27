"""
Filesystem Broker
Brokers file read, write, delete, and list operations through Policy and Sandbox gates.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from core.audit.ledger import audit_ledger
from core.capabilities.permissions import Capability
from core.policy.engine import policy_engine
from core.risk.engine import risk_engine
from .path_guard import path_guard

class FilesystemBroker:
    def __init__(self):
        self.guard = path_guard

    async def read_file(self, agent_id: str, file_path: str) -> Dict[str, Any]:
        score_before = risk_engine.get_score(agent_id)
        
        # Check guard & canaries
        allowed, is_canary, reason = self.guard.check_path_access(agent_id, file_path, is_write=False)
        if is_canary:
            # Canary tripwire touched -> +60 risk!
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="CANARY_TRIPWIRE_TOUCHED",
                reason=f"Agent attempted reading canary credential asset: {file_path}",
                metadata={"path": file_path},
            )
            audit_ledger.append_record(
                agent_id=agent_id,
                event_type="CANARY_TRIGGERED",
                action_name="read_file",
                decision="DENY",
                risk_score_before=score_before,
                risk_score_after=risk_engine.get_score(agent_id),
                degradation_state=risk_engine.get_state(agent_id).value,
                details={"path": file_path, "canary": True},
            )
            return {"success": False, "error": "Access Denied: Protected security asset."}

        eval_res = policy_engine.evaluate_request(
            agent_id=agent_id,
            tool_name="read_file",
            arguments={"path": file_path, "is_write": False},
            required_capability=Capability.FILE_READ,
        )

        if not eval_res["allowed"] or not allowed:
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="PROTECTED_FILE_ACCESS",
                reason=f"Blocked read on {file_path}: {eval_res['reason']}",
            )
            return {"success": False, "error": f"Access Denied: {eval_res['reason']}"}

        try:
            content = Path(file_path).read_text(encoding="utf-8", errors="replace")
            audit_ledger.append_record(
                agent_id=agent_id,
                event_type="FILE_READ",
                action_name="read_file",
                decision="ALLOW",
                risk_score_before=score_before,
                risk_score_after=risk_engine.get_score(agent_id),
                degradation_state=risk_engine.get_state(agent_id).value,
                details={"path": file_path, "bytes": len(content)},
            )
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def write_file(self, agent_id: str, file_path: str, content: str) -> Dict[str, Any]:
        score_before = risk_engine.get_score(agent_id)
        
        allowed, is_canary, reason = self.guard.check_path_access(agent_id, file_path, is_write=True)
        if not allowed:
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="PATH_TRAVERSAL_ATTEMPT",
                reason=f"Blocked write attempt to {file_path}: {reason}",
            )
            return {"success": False, "error": f"Access Denied: {reason}"}

        eval_res = policy_engine.evaluate_request(
            agent_id=agent_id,
            tool_name="write_file",
            arguments={"path": file_path, "is_write": True},
            required_capability=Capability.FILE_WRITE,
        )

        if not eval_res["allowed"]:
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="PROTECTED_FILE_ACCESS",
                reason=f"Write denied by policy: {eval_res['reason']}",
            )
            return {"success": False, "error": f"Access Denied: {eval_res['reason']}"}

        # Track blast radius
        profile = risk_engine.get_or_create_profile(agent_id)
        if not profile.blast_tracker.record_file_modification():
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="BLAST_RADIUS_EXCEEDED",
                reason="File modification budget exceeded",
            )

        try:
            target = Path(file_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            audit_ledger.append_record(
                agent_id=agent_id,
                event_type="FILE_WRITE",
                action_name="write_file",
                decision="ALLOW",
                risk_score_before=score_before,
                risk_score_after=risk_engine.get_score(agent_id),
                degradation_state=risk_engine.get_state(agent_id).value,
                details={"path": file_path, "bytes": len(content)},
            )
            return {"success": True, "written_bytes": len(content)}
        except Exception as e:
            return {"success": False, "error": str(e)}

filesystem_broker = FilesystemBroker()
