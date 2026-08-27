"""
PowerShell Broker
Interposes all PowerShell execution requests through Policy, Risk, Capability checks,
and executes allowed commands within the agent's assigned Win32 Job Object.
"""

import sys
from typing import Any, Dict, Optional
from core.audit.ledger import audit_ledger
from core.capabilities.manager import capability_manager
from core.policy.engine import policy_engine
from core.risk.engine import risk_engine
from windows.process.launcher import process_launcher
from windows.filesystem.canary import canary_manager
from .analyzer import powershell_analyzer

class PowerShellBroker:
    def __init__(self):
        self.analyzer = powershell_analyzer

    async def execute_command(
        self, agent_id: str, command: str, cwd: Optional[str] = None
    ) -> Dict[str, Any]:
        """Broker a PowerShell command request."""
        score_before = risk_engine.get_score(agent_id)

        # 0. Active Canary Tripwire & Token Exfiltration Check
        if canary_manager.contains_canary_token(command) or canary_manager.is_canary_path(command):
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="CANARY_TRIPWIRE_TOUCHED",
                reason=f"Canary credential tripwire / stolen token exfiltration detected in PowerShell command",
                metadata={"command": command},
            )
            audit_ledger.append_record(
                agent_id=agent_id,
                event_type="CANARY_TRIGGERED",
                action_name="powershell",
                decision="DENY",
                risk_score_before=score_before,
                risk_score_after=risk_engine.get_score(agent_id),
                degradation_state=risk_engine.get_state(agent_id).value,
                details={"command": command, "canary_active": True},
            )
            return {
                "success": False,
                "executed": False,
                "error": "Access Denied: High-priority canary decoy asset or stolen token detected.",
                "degradation_state": risk_engine.get_state(agent_id).value,
            }

        # 1. Analyze command syntax and safety
        analysis = self.analyzer.analyze_command(command)
        required_cap = analysis["required_capability"]
        
        # 2. Evaluate against policy engine
        eval_result = policy_engine.evaluate_request(
            agent_id=agent_id,
            tool_name="powershell",
            arguments={"command": command, "is_write": analysis["is_mutating"]},
            required_capability=required_cap,
        )

        score_before = risk_engine.get_score(agent_id)
        
        if not eval_result["allowed"]:
            # Record risk signal for blocked or dangerous command
            risk_delta = max(eval_result.get("risk_delta", 0.0), analysis.get("risk_delta", 15.0))
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="DANGEROUS_SHELL_COMMAND" if analysis["is_dangerous"] else "REPEATED_BLOCKED_COMMAND",
                custom_delta=risk_delta,
                reason=f"Blocked PowerShell: {eval_result['reason']}",
                metadata={"command": command, "analysis": analysis},
            )

            audit_ledger.append_record(
                agent_id=agent_id,
                event_type="POWERSHELL_BLOCKED",
                action_name="powershell",
                decision="DENY",
                risk_score_before=score_before,
                risk_score_after=risk_engine.get_score(agent_id),
                degradation_state=risk_engine.get_state(agent_id).value,
                details={"command": command, "reason": eval_result["reason"], "analysis": analysis},
            )

            return {
                "success": False,
                "executed": False,
                "error": f"GracefulOS Security Denied: {eval_result['reason']}",
                "degradation_state": risk_engine.get_state(agent_id).value,
            }

        # If analysis scored high delta even if policy tentatively allowed (e.g. suspicious activity)
        if analysis["risk_delta"] > 0:
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="DANGEROUS_SHELL_COMMAND",
                custom_delta=analysis["risk_delta"],
                reason=analysis["reason"],
            )

        # 3. Track blast radius
        risk_profile = risk_engine.get_or_create_profile(agent_id)
        if not risk_profile.blast_tracker.record_powershell_command():
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="BLAST_RADIUS_EXCEEDED",
                reason="PowerShell command rate exceeded blast radius budget",
            )

        # 4. Execute within Win32 Job Object
        ps_exec = "powershell.exe" if sys.platform == "win32" else "python"
        cmd_args = ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command] if sys.platform == "win32" else ["echo", f"Simulated: {command}"]
        
        exec_res = process_launcher.launch_agent_process(
            agent_id=agent_id,
            command_line=cmd_args,
            cwd=cwd,
            timeout=30,
        )

        audit_ledger.append_record(
            agent_id=agent_id,
            event_type="POWERSHELL_EXECUTED",
            action_name="powershell",
            decision="ALLOW",
            risk_score_before=score_before,
            risk_score_after=risk_engine.get_score(agent_id),
            degradation_state=risk_engine.get_state(agent_id).value,
            details={"command": command, "exit_code": exec_res["exit_code"]},
        )

        return {
            "success": exec_res["success"],
            "executed": True,
            "stdout": exec_res["stdout"],
            "stderr": exec_res["stderr"],
            "exit_code": exec_res["exit_code"],
            "degradation_state": risk_engine.get_state(agent_id).value,
        }

powershell_broker = PowerShellBroker()
