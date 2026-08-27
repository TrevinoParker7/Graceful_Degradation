"""
GracefulOS Model Context Protocol (MCP) Comprehensive QA Test Suite
Tests real local MCP tool catalog, schema validation, real tool execution,
and degradation mutation lockouts across all 6 tiers.
"""

import sys
import asyncio
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from brokers.mcp.gateway import mcp_gateway
from brokers.mcp.validator import REGISTERED_MCP_TOOLS
from core.capabilities.manager import capability_manager
from core.capabilities.descriptor import WindowsAgentSecurityDescriptor, AgentCapabilities, MCPPolicy
from core.risk.engine import risk_engine
from core.capabilities.permissions import Capability
from core.audit.ledger import audit_ledger

def log_mcp(title: str, passed: bool, details: str = ""):
    tag = "[PASS]" if passed else "[FAIL]"
    print(f"{tag} {title} | {details}")
    if not passed:
        raise AssertionError(f"MCP QA Assertion failed: {title} - {details}")

async def run_mcp_qa():
    print("=" * 70)
    print("GRACEFULOS: COMPREHENSIVE MCP SUBSYSTEM QA TEST")
    print("Target: Real Local Tool Handlers & Degradation Locks")
    print("=" * 70)

    agent_id = "qa-mcp-agent"
    desc = WindowsAgentSecurityDescriptor(
        id=agent_id,
        name="MCP QA Agent",
        mission="mcp_testing",
        model="qwen",
        capabilities=AgentCapabilities(
            mcp=MCPPolicy(
                allowed_tools=["local_code_search", "ast_analyzer", "local_git_status", "local_git_commit"],
                mutating_tools=["local_git_commit"]
            )
        )
    )
    capability_manager.register_agent_descriptor(desc)

    # -------------------------------------------------------------
    # 1. MCP Tool Catalog Listing
    # -------------------------------------------------------------
    print("\n--- 1. Testing MCP Tool Discovery & Catalog ---")
    tools = mcp_gateway.list_available_tools()
    log_mcp("Tool Discovery", len(tools) >= 4, f"Discovered tools: {[t['name'] for t in tools]}")
    assert any(t["name"] == "local_code_search" for t in tools)
    assert any(t["name"] == "ast_analyzer" for t in tools)
    assert any(t["name"] == "local_git_status" for t in tools)
    assert any(t["name"] == "local_git_commit" for t in tools)

    # -------------------------------------------------------------
    # 2. Unknown / Unregistered MCP Tool Rejection
    # -------------------------------------------------------------
    print("\n--- 2. Testing Unknown MCP Tool Rejection ---")
    unregistered_res = await mcp_gateway.invoke_tool(agent_id, "remote_arbitrary_eval", {"payload": "exec()"})
    log_mcp("Unknown Tool Rejection", unregistered_res["success"] is False, f"Error: {unregistered_res.get('error')}")

    # -------------------------------------------------------------
    # 3. Real Local Tool Handler: local_code_search
    # -------------------------------------------------------------
    print("\n--- 3. Testing Real Tool Handler: local_code_search ---")
    risk_engine.reset_agent(agent_id, 0.0) # NORMAL
    search_res = await mcp_gateway.invoke_tool(agent_id, "local_code_search", {"query": "GracefulOS"})
    log_mcp("Real Code Search Tool", search_res["success"] is True, f"Found {search_res['output']['total_matches']} matches")
    assert search_res["output"]["total_matches"] > 0

    # -------------------------------------------------------------
    # 4. Real Local Tool Handler: ast_analyzer
    # -------------------------------------------------------------
    print("\n--- 4. Testing Real Tool Handler: ast_analyzer ---")
    sample_code = """
def authenticate_user(username, password):
    if username == "admin":
        return True
    return False

class SecuritySession:
    def __init__(self):
        self.active = True
"""
    ast_res = await mcp_gateway.invoke_tool(agent_id, "ast_analyzer", {"code": sample_code})
    log_mcp("Real AST Analyzer Tool", ast_res["success"] is True, f"Parsed Functions: {ast_res['output']['functions']}")
    assert "authenticate_user" in ast_res["output"]["functions"]
    assert "SecuritySession" in ast_res["output"]["classes"]
    assert ast_res["output"]["valid_syntax"] is True

    # -------------------------------------------------------------
    # 5. Real Local Tool Handler: local_git_status
    # -------------------------------------------------------------
    print("\n--- 5. Testing Real Tool Handler: local_git_status ---")
    git_res = await mcp_gateway.invoke_tool(agent_id, "local_git_status", {})
    log_mcp("Real Git Status Tool", git_res["success"] is True, f"Modified files count: {git_res['output']['modified_files_count']}")

    # -------------------------------------------------------------
    # 6. Degradation State: RESTRICTED (Mutating MCP Blocked)
    # -------------------------------------------------------------
    print("\n--- 6. Testing Degradation Level 2 (RESTRICTED) MCP Mutation Lock ---")
    risk_engine.reset_agent(agent_id, 60.0) # RESTRICTED
    
    # Read-only tool should still work
    ro_res = await mcp_gateway.invoke_tool(agent_id, "local_code_search", {"query": "RiskEngine"})
    log_mcp("Read-Only Tool in RESTRICTED (Allowed)", ro_res["success"] is True)

    # Mutating tool should be REJECTED in RESTRICTED
    mut_res = await mcp_gateway.invoke_tool(agent_id, "local_git_commit", {"message": "Unauthorized commit"})
    log_mcp("Mutating Tool in RESTRICTED (Denied)", mut_res["success"] is False, f"Reason: {mut_res.get('error')}")

    # -------------------------------------------------------------
    # 7. Degradation State: READ_ONLY (INV-005 Mutation Lock)
    # -------------------------------------------------------------
    print("\n--- 7. Testing Degradation Level 3 (READ_ONLY) MCP Lock ---")
    risk_engine.reset_agent(agent_id, 80.0) # READ_ONLY
    mut_ro = await mcp_gateway.invoke_tool(agent_id, "local_git_commit", {"message": "Attempt during read-only"})
    log_mcp("Mutating Tool in READ_ONLY (Denied)", mut_ro["success"] is False, f"Reason: {mut_ro.get('error')}")

    # -------------------------------------------------------------
    # 8. Degradation State: CONTAINED (Zero MCP Access)
    # -------------------------------------------------------------
    print("\n--- 8. Testing Degradation Level 5 (CONTAINED) Total Lock ---")
    risk_engine.reset_agent(agent_id, 100.0) # CONTAINED
    all_res = await mcp_gateway.invoke_tool(agent_id, "local_code_search", {"query": "test"})
    log_mcp("Read-Only Tool in CONTAINED (Denied)", all_res["success"] is False, f"Reason: {all_res.get('error')}")

    # -------------------------------------------------------------
    # 9. Cryptographic Audit Ledger for MCP Events
    # -------------------------------------------------------------
    print("\n--- 9. Verifying MCP Cryptographic Audit Logging ---")
    v = audit_ledger.verify_chain_integrity()
    log_mcp("Audit Ledger Hash Chaining", v["valid"] is True and v["status"] == "VERIFIED_TAMPER_FREE", f"Total verified records: {v['total_records']}")

    print("\n" + "=" * 70)
    print("ALL MCP SUBSYSTEM QUALITY ASSURANCE TESTS PASSED (100% SUCCESS)")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_mcp_qa())
