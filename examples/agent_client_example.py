"""
GracefulOS Client Example: How Any AI Agent Connects
This demonstrates how an AI agent safely routes its tool actions through GracefulOS.
"""

import requests

BASE_URL = "http://127.0.0.1:7777"
AGENT_ID = "my-developer-agent"

def main():
    print(f"1. Registering agent '{AGENT_ID}' with GracefulOS...")
    reg_response = requests.post(f"{BASE_URL}/api/v1/agents/register", json={
        "agent_id": AGENT_ID,
        "name": "Developer Coding Assistant",
        "mission": "Write code and execute safe tests",
        "model": "local-assistant"
    })
    print("Registration Status:", reg_response.json())

    print("\n2. Invoking a Safe Tool Action (Read File)...")
    read_res = requests.post(f"{BASE_URL}/api/v1/tools/invoke", json={
        "agent_id": AGENT_ID,
        "tool_name": "read_file",
        "arguments": {"path": "README.md"}
    })
    res_json = read_res.json()
    print(f"Read File Result: success={res_json.get('success')}, bytes={len(str(res_json.get('content', '')))}")

    print("\n3. Invoking a Safe PowerShell Query (Get-ChildItem)...")
    ps_res = requests.post(f"{BASE_URL}/api/v1/tools/invoke", json={
        "agent_id": AGENT_ID,
        "tool_name": "powershell",
        "arguments": {"command": "Get-ChildItem -Path ."}
    })
    ps_json = ps_res.json()
    print(f"PowerShell Query Result: success={ps_json.get('success')}, exit_code={ps_json.get('exit_code')}")

    print("\n4. Checking Agent's Current Degradation Posture...")
    agent_status = requests.get(f"{BASE_URL}/api/v1/agents/{AGENT_ID}").json()
    print(f"Current State: {agent_status['state']} | Risk Score: {agent_status['risk_score']} / 100")
    print(f"Effective Capabilities: {agent_status['effective_capabilities']}")

if __name__ == "__main__":
    main()
