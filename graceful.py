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
