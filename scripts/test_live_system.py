"""
Live System Feature Exerciser
Exercises and tests 100% of GracefulOS features against the running live server on http://127.0.0.1:7777
"""

import sys
import time
import requests

BASE_URL = "http://127.0.0.1:7777"

def log_test(name: str, passed: bool, details: str = ""):
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name} {details}")
    if not passed:
        raise RuntimeError(f"Test failed: {name}")

def main():
    print("=" * 70)
    print("TESTING 100% OF GRACEFULOS FEATURES AGAINST LIVE RUNNING SERVER")
    print(f"Target: {BASE_URL}")
    print("=" * 70)

    # 1. System Status
    res = requests.get(f"{BASE_URL}/api/v1/status")
    log_test("System Status API", res.status_code == 200, f"App: {res.json()['app_name']} | Status: {res.json()['status']}")

    # 2. Register Agent
    agent_id = f"live-agent-{int(time.time())}"
    reg_payload = {
        "agent_id": agent_id,
        "name": "Live Verification Agent",
        "mission": "full_feature_exercise",
        "model": "qwen-2.5-coder",
        "trust_score": 80.0
    }
    res = requests.post(f"{BASE_URL}/api/v1/agents/register", json=reg_payload)
    log_test("Agent Registration", res.status_code == 200, f"Agent ID: {agent_id} | State: {res.json().get('state')}")

    # 3. List Agents
    res = requests.get(f"{BASE_URL}/api/v1/agents")
    agents = res.json()
    log_test("List Agents API", any(a["agent_id"] == agent_id for a in agents), f"Active Agents: {len(agents)}")

    # 4. Agent Details
    res = requests.get(f"{BASE_URL}/api/v1/agents/{agent_id}")
    log_test("Get Agent Details", res.status_code == 200 and res.json()["risk_score"] == 0.0)

    # 5. Tool Broker: Filesystem Read (Normal -> ALLOW)
    res = requests.post(f"{BASE_URL}/api/v1/tools/invoke", json={
        "agent_id": agent_id,
        "tool_name": "read_file",
        "arguments": {"path": "README.md"}
    })
    log_test("Filesystem Broker: Read File", res.json().get("success") is True, f"Bytes read: {len(res.json().get('content', ''))}")

    # 6. Tool Broker: Filesystem Write (Normal -> ALLOW)
    res = requests.post(f"{BASE_URL}/api/v1/tools/invoke", json={
        "agent_id": agent_id,
        "tool_name": "write_file",
        "arguments": {"path": f"runtime/agents/{agent_id}/output.txt", "content": "GracefulOS Live Test Output"}
    })
    log_test("Filesystem Broker: Workspace Write", res.json().get("success") is True)

    # 7. Tool Broker: PowerShell Query (Normal -> ALLOW)
    res = requests.post(f"{BASE_URL}/api/v1/tools/invoke", json={
        "agent_id": agent_id,
        "tool_name": "powershell",
        "arguments": {"command": "Get-Date"}
    })
    log_test("PowerShell Broker: Query Command", res.json().get("success") is True, f"Output: {res.json().get('stdout', '').strip()}")

    # 8. Tool Broker: Network Request to Allowlisted Domain (ALLOW)
    res = requests.post(f"{BASE_URL}/api/v1/tools/invoke", json={
        "agent_id": agent_id,
        "tool_name": "network_request",
        "arguments": {"destination": "http://127.0.0.1:7777"}
    })
    log_test("Network Broker: Allowlisted Destination", res.json().get("success") is True)

    # 9. Tool Broker: MCP Gateway Tool Invocation (ALLOW)
    res = requests.post(f"{BASE_URL}/api/v1/tools/invoke", json={
        "agent_id": agent_id,
        "tool_name": "mcp",
        "arguments": {"tool_name": "local_code_search", "args": {"query": "GracefulOS"}}
    })
    log_test("MCP Gateway: Code Search Tool", res.json().get("success") is True)

    # 10. Tool Broker: Browser Broker Navigation (ALLOW)
    res = requests.post(f"{BASE_URL}/api/v1/tools/invoke", json={
        "agent_id": agent_id,
        "tool_name": "browser",
        "arguments": {"url": "http://127.0.0.1:7777"}
    })
    log_test("Browser Broker: Navigation", res.json().get("success") is True)

    # 11. Tool Broker: Secret Broker Lease (ALLOW under Normal)
    res = requests.post(f"{BASE_URL}/api/v1/tools/invoke", json={
        "agent_id": agent_id,
        "tool_name": "secret",
        "arguments": {"scope": "github_read"}
    })
    log_test("Secret Broker: Ephemeral Lease", res.json().get("success") is True, f"Token ID: {res.json().get('token_id')}")

    # 12. Risk Engine: Ingest Prompt Injection Signal (+35 -> Transition to WATCH)
    res = requests.post(f"{BASE_URL}/api/v1/risk/signal", json={
        "agent_id": agent_id,
        "signal_code": "PROMPT_INJECTION_DETECTED",
        "custom_delta": 35.0,
        "reason": "Prompt injection detected in untrusted user document"
    })
    log_test("Risk Engine: Anomaly Ingestion & Watch Transition", res.json()["state_after"] == "WATCH", f"Score: {res.json()['score_after']}")

    # 13. Policy Engine: Block Mutating Command under Escalated Risk (+25 -> RESTRICTED)
    res = requests.post(f"{BASE_URL}/api/v1/tools/invoke", json={
        "agent_id": agent_id,
        "tool_name": "powershell",
        "arguments": {"command": "Set-ItemProperty HKLM:\\Software\\Test -Value 1"}
    })
    log_test("Policy Engine: Mutating Command Blocked", res.json().get("success") is False, f"State: {res.json().get('degradation_state')}")

    # 14. Filesystem Canary Tripwire (+25 -> READ_ONLY)
    res = requests.post(f"{BASE_URL}/api/v1/risk/signal", json={
        "agent_id": agent_id,
        "signal_code": "CANARY_TRIPWIRE_TOUCHED",
        "custom_delta": 25.0,
        "reason": "Decoy token accessed"
    })
    log_test("Canary Tripwire: Read Only Transition", res.json()["state_after"] == "READ_ONLY", f"Score: {res.json()['score_after']}")

    # 15. Invariant INV-004: Service Tamper Defense (+50 -> CONTAINED)
    res = requests.post(f"{BASE_URL}/api/v1/tools/invoke", json={
        "agent_id": agent_id,
        "tool_name": "powershell",
        "arguments": {"command": "Stop-Service GracefulOS"}
    })
    log_test("Self-Protection Invariant INV-004", res.json().get("success") is False)

    # Verify agent state is now CONTAINED
    res = requests.get(f"{BASE_URL}/api/v1/agents/{agent_id}")
    log_test("Containment State Lock", res.json()["state"] == "CONTAINED", f"Risk: {res.json()['risk_score']}/100")

    # 16. Incident Reporting
    res = requests.get(f"{BASE_URL}/api/v1/incidents")
    incidents = res.json()
    log_test("Incidents Ledger", len(incidents) > 0, f"Total Incidents: {len(incidents)}")

    # 17. Incident Replay Step-by-Step Timeline
    res = requests.get(f"{BASE_URL}/api/v1/replay/{agent_id}")
    replay_data = res.json()
    log_test("Incident Replay Timeline", len(replay_data["timeline"]) > 0, f"Timeline Steps: {replay_data['total_steps']}")

    # 18. Administrator Containment Release
    res = requests.post(f"{BASE_URL}/api/v1/recovery/release", json={
        "agent_id": agent_id,
        "admin_token": "ADMIN_LOCAL_SECRET_KEY",
        "target_state": "WATCH",
        "notes": "Admin authorized sandbox release"
    })
    log_test("Admin Recovery Release", res.json().get("status") == "RELEASED", f"New State: {res.json().get('new_state')}")

    # 19. Cryptographic Audit Chain Verification
    res = requests.get(f"{BASE_URL}/api/v1/audit/verify")
    chain_status = res.json()
    log_test("SHA-256 Ledger Cryptographic Integrity", chain_status["valid"] is True and chain_status["status"] == "VERIFIED_TAMPER_FREE", f"Blocks: {chain_status['total_records']}")

    # 20. Dashboard Static Asset Delivery
    res = requests.get(f"{BASE_URL}/")
    log_test("Dashboard HTML Delivery", res.status_code == 200 and "GracefulOS" in res.text)
    res_css = requests.get(f"{BASE_URL}/static/style.css")
    log_test("Dashboard CSS Delivery", res_css.status_code == 200)
    res_js = requests.get(f"{BASE_URL}/static/app.js")
    log_test("Dashboard JS Delivery", res_js.status_code == 200)

    print("=" * 70)
    print("ALL 20 LIVE SYSTEM FEATURE TESTS PASSED (100% SUCCESS)")
    print("=" * 70)

if __name__ == "__main__":
    main()
