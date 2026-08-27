# GOS-010: Windows Job Objects & Process Management

## Objective
Implement Win32 Job Object lifecycle management using Windows APIs (`CreateJobObjectW`, `SetInformationJobObject`, `AssignProcessToJobObject`, `TerminateJobObject`) to constrain CPU/memory and terminate entire process trees.

## Deliverables
1. `windows/job_objects/job.py` wrapping Win32 ctypes calls for Windows Job Objects.
2. Resource limit configuration (CPU rate, commit memory limits, active process limits).
3. Sandboxed process launcher in `windows/process/launcher.py`.
4. Integration tests in `tests/windows/test_job_objects.py`.
