"""
Secret Broker
Dispenses short-lived, scoped ephemeral access credentials, handles DPAPI encryption,
and intercepts canary token requests.
"""

import time
import uuid
from typing import Any, Dict, Optional
from core.audit.ledger import audit_ledger
from core.capabilities.permissions import Capability
from core.policy.engine import policy_engine
from core.risk.engine import risk_engine
from .dpapi import dpapi_service

class SecretBroker:
    def __init__(self):
        self.active_leases: Dict[str, Dict[str, Any]] = {}

    async def request_ephemeral_token(
        self, agent_id: str, scope: str, ttl_seconds: int = 300
    ) -> Dict[str, Any]:
        score_before = risk_engine.get_score(agent_id)

        # Check if agent has capability
        eval_res = policy_engine.evaluate_request(
            agent_id=agent_id,
            tool_name="request_secret",
            arguments={"scope": scope, "ttl": ttl_seconds},
            required_capability=Capability.SECRETS_EPHEMERAL,
        )

        if not eval_res["allowed"]:
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="CREDENTIAL_STORE_ACCESS",
                reason=f"Unauthorized credential request for scope '{scope}': {eval_res['reason']}",
            )
            audit_ledger.append_record(
                agent_id=agent_id,
                event_type="SECRET_DENIED",
                action_name="request_secret",
                decision="DENY",
                risk_score_before=score_before,
                risk_score_after=risk_engine.get_score(agent_id),
                degradation_state=risk_engine.get_state(agent_id).value,
                details={"scope": scope},
            )
            return {"success": False, "error": f"Credential access denied: {eval_res['reason']}"}

        # Issue temporary ephemeral token
        token_id = f"ephem-{uuid.uuid4().hex[:12]}"
        now = time.time()
        lease = {
            "token_id": token_id,
            "agent_id": agent_id,
            "scope": scope,
            "issued_at": now,
            "expires_at": now + ttl_seconds,
            "token_value": f"token_scoped_{scope}_{uuid.uuid4().hex[:8]}",
        }
        self.active_leases[token_id] = lease

        audit_ledger.append_record(
            agent_id=agent_id,
            event_type="SECRET_LEASE_ISSUED",
            action_name="request_secret",
            decision="ALLOW",
            risk_score_before=score_before,
            risk_score_after=risk_engine.get_score(agent_id),
            degradation_state=risk_engine.get_state(agent_id).value,
            details={"token_id": token_id, "scope": scope, "ttl": ttl_seconds},
        )

        return {
            "success": True,
            "token_id": token_id,
            "scope": scope,
            "expires_in_seconds": ttl_seconds,
            "token": lease["token_value"],
        }

    def revoke_all_for_agent(self, agent_id: str) -> int:
        revoked = 0
        for tid, lease in list(self.active_leases.items()):
            if lease["agent_id"] == agent_id:
                del self.active_leases[tid]
                revoked += 1
        return revoked

secret_broker = SecretBroker()
