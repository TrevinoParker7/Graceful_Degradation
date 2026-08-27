"""
Playwright / Dashboard UI Verification Tests
Validates that dashboard files, HTML templates, CSS tokens, and API endpoints are properly integrated.
"""

import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from core.gateway.app import app

client = TestClient(app)

def test_dashboard_index_served():
    res = client.get("/")
    assert res.status_code == 200
    assert "GracefulOS" in res.text
    assert "Overview Dashboard" in res.text

def test_static_assets_served():
    res_css = client.get("/static/style.css")
    assert res_css.status_code == 200
    assert "--color-normal" in res_css.text

    res_js = client.get("/static/app.js")
    assert res_js.status_code == 200
    assert "initNavigation" in res_js.text

def test_all_15_tabs_present_in_html():
    dashboard_html = (Path(__file__).resolve().parent.parent.parent / "dashboard" / "index.html").read_text(encoding="utf-8")
    expected_tabs = [
        "tab-overview", "tab-agents", "tab-agent-details", "tab-processes",
        "tab-capabilities", "tab-risk", "tab-incidents", "tab-network",
        "tab-powershell", "tab-mcp", "tab-policies", "tab-approvals",
        "tab-audit", "tab-replay", "tab-settings"
    ]
    for tab in expected_tabs:
        assert tab in dashboard_html, f"Missing view tab in dashboard: {tab}"
