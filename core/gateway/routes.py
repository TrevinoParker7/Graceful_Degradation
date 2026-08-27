"""
Gateway API Routes
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from core.audit.ledger import audit_ledger
from core.audit.replay import replay_engine
from core.capabilities.descriptor import WindowsAgentSecurityDescriptor
from core.capabilities.manager import capability_manager
from core.events.bus import event_bus
from core.events.events import EventType, BaseEvent
from core.policy.engine import policy_engine
from core.recovery.manager import recovery_manager
from core.risk.engine import risk_engine
from core.risk.state_machine import DegradationState
from brokers.powershell.broker import powershell_broker
from brokers.filesystem.broker import filesystem_broker
from brokers.process.broker import process_broker
from brokers.network.broker import network_broker
from brokers.mcp.gateway import mcp_gateway
from brokers.browser.broker import browser_broker
from brokers.secrets.broker import secret_broker
from .schemas import (
    AgentRegisterRequest,
    ToolInvocationRequest,
    RiskSignalRequest,
    ApprovalDecisionRequest,
    ContainmentReleaseRequest,
    SystemStatusResponse,
)

router = APIRouter(prefix="/api/v1")

# Track registered agents in-memory
ACTIVE_AGENTS: Dict[str, Dict[str, Any]] = {}

@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status():
    incidents = audit_ledger.list_incidents()
    approvals = audit_ledger.list_approvals(status="PENDING")
    integrity = audit_ledger.verify_chain_integrity()

    dist = {"NORMAL": 0, "WATCH": 0, "RESTRICTED": 0, "READ_ONLY": 0, "ISOLATED": 0, "CONTAINED": 0}
    for ag in ACTIVE_AGENTS.values():
        state = risk_engine.get_state(ag["agent_id"]).value
        dist[state] = dist.get(state, 0) + 1

    return SystemStatusResponse(
        app_name="GracefulOS",
        version="0.1.0",
        status="OPERATIONAL",
        total_agents=len(ACTIVE_AGENTS),
        active_incidents=len([i for i in incidents if i.status == "ACTIVE" or i.status == "CONTAINED"]),
        pending_approvals=len(approvals),
        tamper_free_ledger=integrity.get("valid", True),
        degradation_distribution=dist,
    )

@router.post("/agents/register")
async def register_agent(req: AgentRegisterRequest):
    if req.wasd_yaml:
        descriptor = WindowsAgentSecurityDescriptor.from_yaml(req.wasd_yaml)
    else:
        descriptor = WindowsAgentSecurityDescriptor(
            id=req.agent_id,
            name=req.name,
            mission=req.mission,
            model=req.model,
            trust=req.trust_score,
        )
    
    capability_manager.register_agent_descriptor(descriptor)
    risk_engine.get_or_create_profile(req.agent_id, initial_score=0.0)
    
    ACTIVE_AGENTS[req.agent_id] = {
        "agent_id": req.agent_id,
        "name": req.name,
        "mission": req.mission,
        "model": req.model,
        "trust_score": req.trust_score,
    }

    audit_ledger.append_record(
        agent_id=req.agent_id,
        event_type="AGENT_REGISTERED",
        action_name="register",
        decision="ALLOW",
        risk_score_before=0.0,
        risk_score_after=0.0,
        degradation_state="NORMAL",
        details={"name": req.name, "mission": req.mission, "model": req.model},
    )

    return {"status": "SUCCESS", "agent_id": req.agent_id, "state": "NORMAL", "risk_score": 0.0}

@router.get("/agents")
async def list_agents():
    res = []
    for aid, ag in ACTIVE_AGENTS.items():
        res.append({
            **ag,
            "risk_score": risk_engine.get_score(aid),
            "state": risk_engine.get_state(aid).value,
            "capabilities": [c.value for c in capability_manager.get_effective_capabilities(aid)],
        })
    return res

@router.get("/agents/{agent_id}")
async def get_agent_details(agent_id: str):
    if agent_id not in ACTIVE_AGENTS:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    ag = ACTIVE_AGENTS[agent_id]
    profile = risk_engine.get_or_create_profile(agent_id)
    caps = capability_manager.get_effective_capabilities(agent_id)
    timeline = replay_engine.get_agent_timeline(agent_id)
    blast = profile.blast_tracker.get_summary()

    return {
        **ag,
        "risk_score": risk_engine.get_score(agent_id),
        "state": risk_engine.get_state(agent_id).value,
        "effective_capabilities": [c.value for c in caps],
        "blast_radius": blast,
        "signals_count": len(profile.signal_history),
        "recent_timeline": timeline[-10:],
    }

@router.post("/tools/invoke")
async def invoke_tool(req: ToolInvocationRequest):
    tool = req.tool_name.lower()
    args = req.arguments
    agent_id = req.agent_id

    if tool == "powershell":
        return await powershell_broker.execute_command(agent_id=agent_id, command=args.get("command", ""), cwd=args.get("cwd"))
    elif tool == "read_file":
        return await filesystem_broker.read_file(agent_id=agent_id, file_path=args.get("path", ""))
    elif tool == "write_file":
        return await filesystem_broker.write_file(agent_id=agent_id, file_path=args.get("path", ""), content=args.get("content", ""))
    elif tool == "network_request":
        return await network_broker.request_network_access(agent_id=agent_id, destination=args.get("destination", ""))
    elif tool == "mcp":
        return await mcp_gateway.invoke_tool(agent_id=agent_id, tool_name=args.get("tool_name", ""), arguments=args.get("args", {}))
    elif tool == "browser":
        return await browser_broker.navigate_and_read(agent_id=agent_id, url=args.get("url", ""))
    elif tool == "secret":
        return await secret_broker.request_ephemeral_token(agent_id=agent_id, scope=args.get("scope", "default"))
    else:
        # Generic broker evaluation
        eval_res = policy_engine.evaluate_request(agent_id=agent_id, tool_name=tool, arguments=args)
        return eval_res

@router.post("/risk/signal")
async def record_risk_signal(req: RiskSignalRequest):
    res = await risk_engine.ingest_signal(
        agent_id=req.agent_id,
        signal_code=req.signal_code,
        custom_delta=req.custom_delta,
        reason=req.reason,
        metadata=req.metadata,
    )
    return res

@router.get("/audit/records")
async def get_audit_records(limit: int = 100, agent_id: Optional[str] = None):
    records = audit_ledger.list_records(limit=limit, agent_id=agent_id)
    return [r.dict() for r in records]

@router.get("/audit/verify")
async def verify_audit_chain():
    return audit_ledger.verify_chain_integrity()

@router.get("/incidents")
async def get_incidents(limit: int = 50):
    incidents = audit_ledger.list_incidents(limit=limit)
    return [i.dict() for i in incidents]

@router.get("/approvals")
async def get_approvals(status: Optional[str] = None):
    approvals = audit_ledger.list_approvals(status=status)
    return [a.dict() for a in approvals]

@router.post("/approvals/resolve")
async def resolve_approval(req: ApprovalDecisionRequest):
    res = audit_ledger.resolve_approval(
        request_id=req.request_id,
        approved=req.approved,
        reviewer=req.reviewer,
        notes=req.notes,
    )
    if not res:
        raise HTTPException(status_code=404, detail="Approval request not found")
    
    # If approved and always_trust is requested, permanently whitelist in PolicyEngine
    if req.approved:
        if req.always_trust:
            pattern = res.action_description.strip() or res.tool_name
            policy_engine.add_trusted_pattern(pattern)
        else:
            policy_engine.authorize_once(res.tool_name)

    return res.dict()

@router.get("/policy/trust")
async def get_trusted_patterns():
    return {"trusted_patterns": policy_engine.list_trusted_patterns()}

@router.post("/policy/trust")
async def add_trusted_pattern(payload: Dict[str, Any]):
    pattern = payload.get("pattern", "").strip()
    if not pattern:
        raise HTTPException(status_code=400, detail="Pattern cannot be empty")
    policy_engine.add_trusted_pattern(pattern)
    return {"status": "ADDED", "pattern": pattern, "trusted_patterns": policy_engine.list_trusted_patterns()}

@router.delete("/policy/trust")
async def remove_trusted_pattern(payload: Dict[str, Any]):
    pattern = payload.get("pattern", "").strip()
    policy_engine.remove_trusted_pattern(pattern)
    return {"status": "REMOVED", "pattern": pattern, "trusted_patterns": policy_engine.list_trusted_patterns()}

@router.get("/replay/{agent_id}")
async def get_incident_replay(agent_id: str):
    timeline = replay_engine.get_agent_timeline(agent_id)
    return {"agent_id": agent_id, "timeline": timeline, "total_steps": len(timeline)}

@router.post("/recovery/release")
async def release_containment(req: ContainmentReleaseRequest):
    target = getattr(DegradationState, req.target_state.upper(), DegradationState.WATCH)
    res = recovery_manager.release_agent_containment(
        agent_id=req.agent_id,
        admin_token=req.admin_token,
        notes=req.notes,
        target_state=target,
    )
    return res
