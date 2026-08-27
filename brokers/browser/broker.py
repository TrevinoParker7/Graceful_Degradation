"""
Browser Broker
Enforces URL allowlists and restricts mutating browser automations (form fills, clicks) in degraded states.
"""

from typing import Any, Dict
from core.audit.ledger import audit_ledger
from core.capabilities.permissions import Capability
from core.policy.engine import policy_engine
from core.risk.engine import risk_engine
from .guard import BROWSER_ALLOWLIST

class BrowserBroker:
    async def navigate_and_read(self, agent_id: str, url: str) -> Dict[str, Any]:
        score_before = risk_engine.get_score(agent_id)
        
        eval_res = policy_engine.evaluate_request(
            agent_id=agent_id,
            tool_name="browser_navigate",
            arguments={"url": url, "is_write": False},
            required_capability=Capability.NETWORK_ALLOWLIST,
        )

        if not eval_res["allowed"]:
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="UNKNOWN_NETWORK_DESTINATION",
                reason=f"Blocked browser access to {url}: {eval_res['reason']}",
            )
            return {"success": False, "error": f"Browser navigation denied: {eval_res['reason']}"}

        audit_ledger.append_record(
            agent_id=agent_id,
            event_type="BROWSER_NAVIGATE",
            action_name="browser_navigate",
            decision="ALLOW",
            risk_score_before=score_before,
            risk_score_after=risk_engine.get_score(agent_id),
            degradation_state=risk_engine.get_state(agent_id).value,
            details={"url": url},
        )

        return {"success": True, "url": url, "dom": f"<html><body>Simulated content from {url}</body></html>"}

browser_broker = BrowserBroker()
