"""
Integration Tests for FastAPI Gateway REST Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from core.gateway.app import app

client = TestClient(app)

def test_system_status_endpoint():
    res = client.get("/api/v1/status")
    assert res.status_code == 200
    data = res.json()
    assert data["app_name"] == "GracefulOS"
    assert data["status"] == "OPERATIONAL"

def test_agent_registration_and_flow():
    reg_payload = {
        "agent_id": "test-agent-int-001",
        "name": "Integration Test Agent",
        "mission": "integration_testing",
        "model": "qwen-test",
    }
    res = client.post("/api/v1/agents/register", json=reg_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert data["state"] == "NORMAL"

    # List agents
    res_list = client.get("/api/v1/agents")
    assert res_list.status_code == 200
    agents = res_list.json()
    assert any(a["agent_id"] == "test-agent-int-001" for a in agents)
