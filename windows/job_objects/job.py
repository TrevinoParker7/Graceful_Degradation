"""
Windows 11 Native Job Object Implementation via ctypes
"""

import ctypes
import os
import sys
from ctypes import wintypes
from typing import Dict, List, Optional
from .limits import JobResourceLimits

# Win32 Constants
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
JOB_OBJECT_LIMIT_ACTIVE_PROCESS = 0x00000008
JOB_OBJECT_LIMIT_JOB_MEMORY = 0x00000200
JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x00000100
JOB_OBJECT_CPU_RATE_CONTROL_ENABLE = 0x00000001
JOB_OBJECT_CPU_RATE_CONTROL_HARD_CAP = 0x00000004

JobObjectBasicLimitInformation = 2
JobObjectExtendedLimitInformation = 9
JobObjectCpuRateControlInformation = 15

# Win32 Structs
class IO_COUNTERS(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_uint64),
        ("WriteOperationCount", ctypes.c_uint64),
        ("OtherOperationCount", ctypes.c_uint64),
        ("ReadTransferCount", ctypes.c_uint64),
        ("WriteTransferCount", ctypes.c_uint64),
        ("OtherTransferCount", ctypes.c_uint64),
    ]

class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    ]

class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ("IoInfo", IO_COUNTERS),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]

class JOBOBJECT_CPU_RATE_CONTROL_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("ControlFlags", wintypes.DWORD),
        ("CpuRate", wintypes.DWORD),
    ]

class WindowsJobObject:
    def __init__(self, name: str, limits: Optional[JobResourceLimits] = None):
        self.name = name
        self.limits = limits or JobResourceLimits()
        self.handle: Optional[int] = None
        self.assigned_pids: List[int] = []
        self._is_windows = sys.platform == "win32"
        self._init_job()

    def _init_job(self) -> None:
        if not self._is_windows:
            return

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        # Create Job Object
        self.handle = kernel32.CreateJobObjectW(None, f"GracefulOS_Job_{self.name}")
        if not self.handle:
            err = ctypes.get_last_error()
            print(f"Warning: Could not create Job Object {self.name}: Error {err}")
            return

        # Apply Extended Limits
        ext_limits = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        limit_flags = 0
        
        if self.limits.kill_on_job_close:
            limit_flags |= JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if self.limits.max_processes > 0:
            limit_flags |= JOB_OBJECT_LIMIT_ACTIVE_PROCESS
            ext_limits.BasicLimitInformation.ActiveProcessLimit = self.limits.max_processes
        if self.limits.max_memory_mb > 0:
            limit_flags |= JOB_OBJECT_LIMIT_JOB_MEMORY
            ext_limits.JobMemoryLimit = self.limits.max_memory_mb * 1024 * 1024
        if self.limits.per_process_memory_mb > 0:
            limit_flags |= JOB_OBJECT_LIMIT_PROCESS_MEMORY
            ext_limits.ProcessMemoryLimit = self.limits.per_process_memory_mb * 1024 * 1024

        ext_limits.BasicLimitInformation.LimitFlags = limit_flags

        res = kernel32.SetInformationJobObject(
            self.handle,
            JobObjectExtendedLimitInformation,
            ctypes.byref(ext_limits),
            ctypes.sizeof(ext_limits),
        )
        if not res:
            print(f"Warning: SetInformationJobObject failed: {ctypes.get_last_error()}")

    def assign_process(self, pid: int) -> bool:
        """Assign a process PID to this Job Object."""
        self.assigned_pids.append(pid)
        if not self._is_windows or not self.handle:
            return True

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        # Open process handle with PROCESS_SET_QUOTA | PROCESS_TERMINATE
        PROCESS_SET_QUOTA = 0x0100
        PROCESS_TERMINATE = 0x0001
        h_proc = kernel32.OpenProcess(PROCESS_SET_QUOTA | PROCESS_TERMINATE, False, pid)
        if not h_proc:
            return False

        try:
            success = kernel32.AssignProcessToJobObject(self.handle, h_proc)
            return bool(success)
        finally:
            kernel32.CloseHandle(h_proc)

    def terminate_all(self, exit_code: int = 1) -> bool:
        """Terminate all processes in the job object synchronously."""
        if not self._is_windows or not self.handle:
            # Fallback mock/manual kill for assigned PIDs
            for pid in list(self.assigned_pids):
                try:
                    os.kill(pid, 9)
                except Exception:
                    pass
            self.assigned_pids.clear()
            return True

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        success = kernel32.TerminateJobObject(self.handle, exit_code)
        self.assigned_pids.clear()
        return bool(success)

    def query_active_processes_count(self) -> int:
        """Query real Windows kernel for number of active processes in this Job Object."""
        if not self._is_windows or not self.handle:
            return len(self.assigned_pids)

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        class JOBOBJECT_BASIC_ACCOUNTING_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("TotalUserTime", ctypes.c_int64),
                ("TotalKernelTime", ctypes.c_int64),
                ("ThisPeriodTotalUserTime", ctypes.c_int64),
                ("ThisPeriodTotalKernelTime", ctypes.c_int64),
                ("TotalPageFaultCount", wintypes.DWORD),
                ("TotalProcesses", wintypes.DWORD),
                ("ActiveProcesses", wintypes.DWORD),
                ("TotalTerminatedProcesses", wintypes.DWORD),
            ]
        
        info = JOBOBJECT_BASIC_ACCOUNTING_INFORMATION()
        JobObjectBasicAccountingInformation = 1
        res = kernel32.QueryInformationJobObject(
            self.handle,
            JobObjectBasicAccountingInformation,
            ctypes.byref(info),
            ctypes.sizeof(info),
            None,
        )
        if res:
            return info.ActiveProcesses
        return len(self.assigned_pids)

    def close(self) -> None:
        if self._is_windows and self.handle:
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.CloseHandle(self.handle)
            self.handle = None

class JobObjectManager:
    def __init__(self):
        self.jobs: Dict[str, WindowsJobObject] = {}

    def get_or_create_job(self, agent_id: str, limits: Optional[JobResourceLimits] = None) -> WindowsJobObject:
        if agent_id not in self.jobs:
            self.jobs[agent_id] = WindowsJobObject(agent_id, limits)
        return self.jobs[agent_id]

    def terminate_agent_job(self, agent_id: str) -> bool:
        if agent_id in self.jobs:
            job = self.jobs[agent_id]
            res = job.terminate_all()
            return res
        return False

# Global Job Object Manager
job_manager = JobObjectManager()
