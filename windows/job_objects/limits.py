"""
Win32 Job Object Resource Limits Specification
"""

from pydantic import BaseModel

class JobResourceLimits(BaseModel):
    max_processes: int = 10
    max_memory_mb: int = 512
    cpu_rate_percentage: int = 50  # 1-100% of CPU time
    per_process_memory_mb: int = 256
    kill_on_job_close: bool = True
