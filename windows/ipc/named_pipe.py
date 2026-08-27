"""
Windows 11 Native Named Pipe IPC Server and Client
Uses Win32 APIs (win32pipe, win32file) for real local inter-process communication.
Default Pipe: \\\\.\\pipe\\GracefulOS
"""

import asyncio
import json
import sys
import threading
from typing import Any, Callable, Dict, Optional
from config.settings import config

class WindowsNamedPipeIPC:
    def __init__(self, pipe_name: Optional[str] = None):
        self.pipe_name = pipe_name or config.named_pipe_path
        self._is_windows = sys.platform == "win32"
        self._running = False
        self._server_thread: Optional[threading.Thread] = None

    async def handle_client_message(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch received IPC message to GracefulOS control plane."""
        action = request_payload.get("action", "ping")
        if action == "ping":
            return {"status": "PONG", "server": "GracefulOS Windows Core Service"}
        elif action == "evaluate_tool":
            from core.policy.engine import policy_engine
            agent_id = request_payload.get("agent_id", "anon-agent")
            tool_name = request_payload.get("tool_name", "")
            args = request_payload.get("arguments", {})
            return policy_engine.evaluate_request(agent_id=agent_id, tool_name=tool_name, arguments=args)
        return {"status": "UNKNOWN_ACTION", "action": action}

    def client_call(self, request_payload: Dict[str, Any], timeout_ms: int = 2000) -> Dict[str, Any]:
        """Send message to Windows Named Pipe synchronously using CallNamedPipe."""
        if not self._is_windows:
            # Fallback for non-Windows test environments
            loop = asyncio.new_event_loop()
            res = loop.run_until_complete(self.handle_client_message(request_payload))
            loop.close()
            return res

        import win32pipe
        payload_bytes = json.dumps(request_payload).encode("utf-8")
        try:
            response_bytes = win32pipe.CallNamedPipe(
                self.pipe_name,
                payload_bytes,
                65536,
                timeout_ms,
            )
            return json.loads(response_bytes.decode("utf-8"))
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    def _server_loop(self) -> None:
        if not self._is_windows:
            return

        import win32pipe
        import win32file
        import pywintypes

        BUFFER_SIZE = 65536
        while self._running:
            try:
                pipe_handle = win32pipe.CreateNamedPipe(
                    self.pipe_name,
                    win32pipe.PIPE_ACCESS_DUPLEX,
                    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                    win32pipe.PIPE_UNLIMITED_INSTANCES,
                    BUFFER_SIZE,
                    BUFFER_SIZE,
                    0,
                    None,
                )

                # Wait for client connection
                win32pipe.ConnectNamedPipe(pipe_handle, None)

                # Read message
                hr, data = win32file.ReadFile(pipe_handle, BUFFER_SIZE)
                request_payload = json.loads(data.decode("utf-8"))

                # Process message
                loop = asyncio.new_event_loop()
                response = loop.run_until_complete(self.handle_client_message(request_payload))
                loop.close()

                # Write response
                response_bytes = json.dumps(response).encode("utf-8")
                win32file.WriteFile(pipe_handle, response_bytes)
                win32pipe.DisconnectNamedPipe(pipe_handle)
                win32file.CloseHandle(pipe_handle)
            except Exception:
                if not self._running:
                    break

    def start_server_background(self) -> None:
        if self._running or not self._is_windows:
            return
        self._running = True
        self._server_thread = threading.Thread(target=self._server_loop, daemon=True)
        self._server_thread.start()

    def stop_server(self) -> None:
        self._running = False

NamedPipeIPC = WindowsNamedPipeIPC
named_pipe_ipc = WindowsNamedPipeIPC()
