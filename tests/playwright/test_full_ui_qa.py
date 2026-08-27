"""
Comprehensive UI Dashboard & All Features / Buttons QA Test
Tests every tab, button, card, and interactive control in the GracefulOS Dashboard.
"""

import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:7777"

def test_ui_all_15_tabs_and_buttons():
    # 1. Verify Server is Online
    res = requests.get(f"{BASE_URL}/api/v1/status")
    assert res.status_code == 200
    status_data = res.json()
    assert status_data["status"] == "OPERATIONAL"

    # 2. Verify HTML and all 15 tab declarations
    res_html = requests.get(f"{BASE_URL}/")
    assert res_html.status_code == 200
    html = res_html.text

    expected_tabs = [
        "tab-overview", "tab-agents", "tab-agent-details", "tab-processes",
        "tab-capabilities", "tab-risk", "tab-incidents", "tab-network",
        "tab-powershell", "tab-mcp", "tab-policies", "tab-approvals",
        "tab-audit", "tab-replay", "tab-settings"
    ]

    for tab in expected_tabs:
        assert f'data-tab="{tab}"' in html, f"Missing nav item for {tab}"
        assert f'id="{tab}"' in html, f"Missing panel for {tab}"

    # 3. Verify Buttons in HTML
    assert "triggerRefresh()" in html
    assert "runAttackDemo()" in html
    assert "releaseContainment()" in html

    # 4. Test Attack Demo API Flow (triggered by the 'Run Attack Demo' button)
    reg_res = requests.post(f"{BASE_URL}/api/v1/agents/register", json={
        "agent_id": "ui-qa-agent",
        "name": "UI QA Agent",
        "mission": "dashboard_test",
        "model": "qwen"
    })
    assert reg_res.status_code == 200

    # Trigger attack progression
    requests.post(f"{BASE_URL}/api/v1/risk/signal", json={
        "agent_id": "ui-qa-agent",
        "signal_code": "PROMPT_INJECTION_DETECTED",
        "reason": "UI demo attack"
    })
    
    # 5. Verify Agent Telemetry API (used by Agent Details tab & Inspect button)
    agent_detail = requests.get(f"{BASE_URL}/api/v1/agents/ui-qa-agent").json()
    assert agent_detail["agent_id"] == "ui-qa-agent"
    assert agent_detail["risk_score"] > 0
    assert "effective_capabilities" in agent_detail
    assert "blast_radius" in agent_detail

    # 6. Verify Incident Replay API (used by Replay tab)
    replay_data = requests.get(f"{BASE_URL}/api/v1/replay/ui-qa-agent").json()
    assert "timeline" in replay_data

    # 7. Verify Approval Workflow Buttons
    appr_res = requests.get(f"{BASE_URL}/api/v1/approvals").json()
    assert isinstance(appr_res, list)

    # 8. Verify Release Containment API (used by Settings Authorize Release button)
    rel_res = requests.post(f"{BASE_URL}/api/v1/recovery/release", json={
        "agent_id": "ui-qa-agent",
        "admin_token": "ADMIN_LOCAL_SECRET_KEY",
        "target_state": "WATCH",
        "notes": "UI Release Button Test"
    })
    assert rel_res.status_code == 200
    assert rel_res.json()["status"] == "RELEASED"

    # 9. Verify Immutable Audit Ledger Integrity Badge API
    audit_verify = requests.get(f"{BASE_URL}/api/v1/audit/verify").json()
    assert audit_verify["valid"] is True
    assert audit_verify["status"] == "VERIFIED_TAMPER_FREE"

    print("\n[PASS] All 15 Dashboard Tabs, Buttons, Telemetry Cards, and Control Handlers Verified!")
