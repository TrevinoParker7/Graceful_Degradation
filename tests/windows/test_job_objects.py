"""
Windows 11 Job Object Integration Tests
Verifies Win32 Job Object creation, limits assignment, and process tree termination.
"""

import sys
import pytest
from windows.job_objects.job import job_manager, WindowsJobObject
from windows.job_objects.limits import JobResourceLimits

def test_job_object_creation_and_limits():
    limits = JobResourceLimits(max_processes=5, max_memory_mb=128)
    job = job_manager.get_or_create_job("test-job-agent-001", limits)
    assert job is not None

def test_job_object_kill_switch():
    job = job_manager.get_or_create_job("test-job-agent-kill")
    # Terminate all should execute cleanly
    res = job.terminate_all()
    assert res is True
