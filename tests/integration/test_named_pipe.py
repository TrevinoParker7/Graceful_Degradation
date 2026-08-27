"""
Integration Tests for Named Pipe IPC Message Handling
"""

import pytest
from windows.ipc.named_pipe import named_pipe_ipc

@pytest.mark.asyncio
async def test_named_pipe_ipc_messages():
    # Ping
    ping_res = await named_pipe_ipc.handle_client_message({"action": "ping"})
    assert ping_res["status"] == "PONG"

    # Evaluate tool
    eval_res = await named_pipe_ipc.handle_client_message({
        "action": "evaluate_tool",
        "agent_id": "pipe-agent-001",
        "tool_name": "read_file",
        "arguments": {"path": "README.md"},
    })
    assert "decision" in eval_res
