"""
GracefulOS CLI Entrypoint
Windows 11 Local-Only Agentic AI Security Control Plane
"""

import argparse
import asyncio
import sys
import uvicorn
from config.settings import config
from core.audit.ledger import audit_ledger
from core.recovery.manager import recovery_manager
from core.risk.engine import risk_engine
from core.risk.state_machine import DegradationState
from simulations.flagship_attack_chain import run_flagship_demo
from windows.filesystem.canary import canary_manager
from windows.job_objects.limits import JobResourceLimits

def cmd_start(args):
    print(f"Starting GracefulOS Control Plane on http://{config.host}:{config.port} ...")
    uvicorn.run("core.gateway.app:app", host=config.host, port=config.port, log_level="info", reload=False)

def cmd_attack_demo(args):
    asyncio.run(run_flagship_demo())

def cmd_verify_ledger(args):
    res = audit_ledger.verify_chain_integrity()
    print("=" * 60)
    print("AUDIT LEDGER INTEGRITY REPORT")
    print("=" * 60)
    print(f"Valid: {res['valid']}")
    print(f"Status: {res['status']}")
    print(f"Total Blocks: {res['total_records']}")
    if 'head_hash' in res:
        print(f"Head Hash: {res['head_hash']}")
    print("=" * 60)

def cmd_seed_canaries(args):
    canary_manager.seed_canary_files()
    print(f"Seeded canary decoy tripwires in {config.canary_dir}:")
    for f in canary_manager.list_canary_files():
        print(f" - {f}")

def cmd_release(args):
    res = recovery_manager.release_agent_containment(
        agent_id=args.agent_id,
        admin_token=args.token,
        target_state=DegradationState.WATCH,
        notes="Admin released via CLI",
    )
    print(f"Agent {args.agent_id} released: {res}")

def cmd_run(args):
    """Automatically launches and protects any script, AI bot, or command inside GracefulOS."""
    import subprocess, time, uuid, os
    from windows.job_objects.job import WindowsJobObject
    from core.capabilities.manager import capability_manager
    from core.capabilities.descriptor import WindowsAgentSecurityDescriptor, AgentCapabilities
    
    agent_id = f"auto-agent-{uuid.uuid4().hex[:6]}"
    target_cmd = args.target
    print(f"[*] Auto-Protecting target command: '{' '.join(target_cmd)}'")
    print(f"[*] Registered Agent ID: {agent_id}")

    # Auto-register agent descriptor
    desc = WindowsAgentSecurityDescriptor(
        id=agent_id,
        name="Auto-Protected Process",
        mission=f"Execute: {' '.join(target_cmd)}",
        model="auto-detected"
    )
    capability_manager.register_agent_descriptor(desc)

    # Bind to Win32 Job Object
    limits = JobResourceLimits(max_memory_mb=512, kill_on_job_close=True)
    job = WindowsJobObject(f"GracefulOS_Job_{agent_id}", limits=limits)
    
    env = os.environ.copy()
    env["GRACEFULOS_AGENT_ID"] = agent_id
    env["GRACEFULOS_ENDPOINT"] = f"http://{config.host}:{config.port}"

    proc = subprocess.Popen(target_cmd, env=env)
    job.assign_process(proc.pid)
    print(f"[OK] Process spawned (PID {proc.pid}) and attached to Windows Job Object.")

    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n[!] Stopping auto-protected process...")
        job.terminate_all(exit_code=1)
    finally:
        job.close()

def cmd_test(args):
    import subprocess
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    res = subprocess.run(cmd)
    sys.exit(res.returncode)

def main():
    parser = argparse.ArgumentParser(description="GracefulOS Windows 11 Security Control Plane CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # start
    sub_start = subparsers.add_parser("start", help="Start the GracefulOS Control Plane and Dashboard")
    sub_start.set_defaults(func=cmd_start)

    # run (auto-protect)
    sub_run = subparsers.add_parser("run", help="Auto-protect and sandbox any script or command inside GracefulOS")
    sub_run.add_argument("target", nargs=argparse.REMAINDER, help="Target script or command (e.g. python agent.py)")
    sub_run.set_defaults(func=cmd_run)

    # attack-demo
    sub_demo = subparsers.add_parser("attack-demo", help="Run the Flagship 5-Stage Attack Chain demo")
    sub_demo.set_defaults(func=cmd_attack_demo)

    # verify-ledger
    sub_ledger = subparsers.add_parser("verify-ledger", help="Verify cryptographic SHA-256 hash chain of audit ledger")
    sub_ledger.set_defaults(func=cmd_verify_ledger)

    # seed-canaries
    sub_canary = subparsers.add_parser("seed-canaries", help="Deploy decoy canary credential tripwires")
    sub_canary.set_defaults(func=cmd_seed_canaries)

    # release
    sub_release = subparsers.add_parser("release", help="Release an agent from CONTAINED state")
    sub_release.add_argument("agent_id", help="Target agent identifier")
    sub_release.add_argument("--token", default="ADMIN_LOCAL_SECRET_KEY", help="Administrator authorization token")
    sub_release.set_defaults(func=cmd_release)

    # test
    sub_test = subparsers.add_parser("test", help="Run all automated unit, integration, and security tests")
    sub_test.set_defaults(func=cmd_test)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
