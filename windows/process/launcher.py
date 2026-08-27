"""
Sandboxed Process Launcher for Windows 11
Binds spawned processes to agent's dedicated Job Object and tracks lifetime.
"""

import os
import subprocess
import sys
from typing import Any, Dict, List, Optional
from windows.job_objects.job import job_manager
from core.events.bus import event_bus
from core.events.events import BaseEvent, EventType

class ProcessLauncher:
    def __init__(self):
        self.active_processes: Dict[int, Dict[str, Any]] = {}

    def launch_agent_process(
        self,
        agent_id: str,
        command_line: List[str] | str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        capture_output: bool = True,
        timeout: Optional[int] = 30,
    ) -> Dict[str, Any]:
        """Launch a process securely assigned into the agent's Job Object."""
        job = job_manager.get_or_create_job(agent_id)
        
        # Spawn process suspended/normal
        proc = subprocess.Popen(
            command_line,
            cwd=cwd,
            env=env or os.environ.copy(),
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            text=True,
            shell=isinstance(command_line, str),
        )

        pid = proc.pid
        job.assign_process(pid)

        self.active_processes[pid] = {
            "agent_id": agent_id,
            "pid": pid,
            "command": str(command_line),
            "status": "RUNNING",
        }

        stdout, stderr = None, None
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            exit_code = -1
        finally:
            self.active_processes.pop(pid, None)

        return {
            "pid": pid,
            "exit_code": exit_code,
            "stdout": stdout or "",
            "stderr": stderr or "",
            "success": exit_code == 0,
        }

process_launcher = ProcessLauncher()
