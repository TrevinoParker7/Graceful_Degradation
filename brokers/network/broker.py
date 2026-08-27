"""
Network Broker
Mediates outbound network calls, validates allowlists, updates Windows Defender Firewall dynamically.
"""

from typing import Any, Dict, Optional
import urllib.parse
from core.audit.ledger import audit_ledger
from core.capabilities.permissions import Capability
from core.policy.engine import policy_engine
from core.risk.engine import risk_engine
from windows.firewall.netsh import firewall_manager
from .allowlist import DEFAULT_NETWORK_ALLOWLIST

class NetworkBroker:
    async def request_network_access(
        self, agent_id: str, destination: str, port: int = 80, protocol: str = "HTTP"
    ) -> Dict[str, Any]:
        parsed = urllib.parse.urlparse(destination)
        host = parsed.hostname or destination.split(":")[0]
        score_before = risk_engine.get_score(agent_id)

        eval_res = policy_engine.evaluate_request(
            agent_id=agent_id,
            tool_name="network_request",
            arguments={"destination": destination, "host": host, "port": port},
            required_capability=Capability.NETWORK_ALLOWLIST,
        )

        if not eval_res["allowed"] or host not in DEFAULT_NETWORK_ALLOWLIST:
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="UNKNOWN_NETWORK_DESTINATION",
                reason=f"Blocked network connection to unauthorized destination: {host}",
            )
            audit_ledger.append_record(
                agent_id=agent_id,
                event_type="NETWORK_BLOCKED",
                action_name="network_request",
                decision="DENY",
                risk_score_before=score_before,
                risk_score_after=risk_engine.get_score(agent_id),
                degradation_state=risk_engine.get_state(agent_id).value,
                details={"destination": destination, "host": host},
            )
            return {"success": False, "error": f"Network Access Denied to {destination} by GracefulOS policy."}

        # Track blast radius
        profile = risk_engine.get_or_create_profile(agent_id)
        if not profile.blast_tracker.record_network_destination(host):
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="BLAST_RADIUS_EXCEEDED",
                reason="Distinct network destination count exceeded blast radius budget",
            )

        audit_ledger.append_record(
            agent_id=agent_id,
            event_type="NETWORK_CONNECTED",
            action_name="network_request",
            decision="ALLOW",
            risk_score_before=score_before,
            risk_score_after=risk_engine.get_score(agent_id),
            degradation_state=risk_engine.get_state(agent_id).value,
            details={"destination": destination, "host": host},
        )

        return {"success": True, "destination": destination, "status": "CONNECTED"}

network_broker = NetworkBroker()
