"""
Process Broker
Mediates process execution, enforces binary allowlists, and assigns processes to Win32 Job Objects.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from core.audit.ledger import audit_ledger
from core.capabilities.permissions import Capability
from core.policy.engine import policy_engine
from core.risk.engine import risk_engine
from windows.process.launcher import process_launcher
from .allowlist import DEFAULT_PROCESS_ALLOWLIST, FORBIDDEN_BINARIES

class ProcessBroker:
    async def spawn_process(
        self, agent_id: str, executable: str, args: List[str], cwd: Optional[str] = None
    ) -> Dict[str, Any]:
        binary_name = Path(executable).name.lower()
        score_before = risk_engine.get_score(agent_id)

        # Check forbidden
        if binary_name in FORBIDDEN_BINARIES:
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="UNAPPROVED_EXECUTABLE",
                custom_delta=40.0,
                reason=f"Forbidden attack binary requested: {binary_name}",
            )
            return {"success": False, "error": f"Execution of {binary_name} is strictly forbidden."}

        eval_res = policy_engine.evaluate_request(
            agent_id=agent_id,
            tool_name="spawn_process",
            arguments={"executable": executable, "args": args},
            required_capability=Capability.PROCESS_SPAWN,
        )

        if not eval_res["allowed"]:
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="UNAPPROVED_EXECUTABLE",
                reason=f"Process launch denied by policy: {eval_res['reason']}",
            )
            return {"success": False, "error": f"Access Denied: {eval_res['reason']}"}

        # Track blast radius
        profile = risk_engine.get_or_create_profile(agent_id)
        if not profile.blast_tracker.record_process_spawn():
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="BLAST_RADIUS_EXCEEDED",
                reason="Process spawn count exceeded blast radius budget",
            )

        cmd = [executable] + args
        res = process_launcher.launch_agent_process(agent_id=agent_id, command_line=cmd, cwd=cwd)

        audit_ledger.append_record(
            agent_id=agent_id,
            event_type="PROCESS_SPAWNED",
            action_name="spawn_process",
            decision="ALLOW",
            risk_score_before=score_before,
            risk_score_after=risk_engine.get_score(agent_id),
            degradation_state=risk_engine.get_state(agent_id).value,
            details={"executable": executable, "pid": res.get("pid")},
        )

        return res

process_broker = ProcessBroker()
