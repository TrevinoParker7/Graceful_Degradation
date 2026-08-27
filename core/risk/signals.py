"""
Risk Signal Definitions and Base Penalty Values
"""

from typing import Dict

# Standardized signal codes and associated default delta points
RISK_SIGNALS: Dict[str, Dict[str, float | str]] = {
    # Normal operations
    "NORMAL_ACTION": {
        "delta": 0.0,
        "description": "Legitimate mission-aligned action performed within approved scope.",
    },
    # Prompt injection and untrusted input
    "PROMPT_INJECTION_DETECTED": {
        "delta": 28.0,
        "description": "Guardian AI or heuristics detected prompt injection payload in untrusted content.",
    },
    "SUSPICIOUS_PROMPT_PATTERN": {
        "delta": 15.0,
        "description": "Heuristic match for jailbreak or evasion syntax.",
    },
    # PowerShell & Process execution
    "DANGEROUS_SHELL_COMMAND": {
        "delta": 30.0,
        "description": "PowerShell command containing dangerous cmdlets, recursive delete, or encoding.",
    },
    "UNAPPROVED_EXECUTABLE": {
        "delta": 20.0,
        "description": "Attempt to launch an unapproved binary outside designated allowlist.",
    },
    "REPEATED_BLOCKED_COMMAND": {
        "delta": 15.0,
        "description": "Multiple sequential attempts to execute denied tool calls.",
    },
    # Filesystem & Path traversal
    "PATH_TRAVERSAL_ATTEMPT": {
        "delta": 35.0,
        "description": "Attempt to escape workspace boundary or access sensitive system directories.",
    },
    "PROTECTED_FILE_ACCESS": {
        "delta": 30.0,
        "description": "Attempted read/write of Windows system files or user profile configurations.",
    },
    # Canary tripwires & Credentials
    "CANARY_TRIPWIRE_TOUCHED": {
        "delta": 60.0,
        "description": "Agent accessed an intentional decoy credential or token file.",
    },
    "CREDENTIAL_STORE_ACCESS": {
        "delta": 25.0,
        "description": "Unsolicited attempt to query DPAPI, SAM, or Credential Manager.",
    },
    # Network anomalies
    "UNKNOWN_NETWORK_DESTINATION": {
        "delta": 20.0,
        "description": "Outbound connection attempt to non-allowlisted IP/Domain.",
    },
    "NETWORK_SCANNING_DETECTED": {
        "delta": 40.0,
        "description": "Port scanning or subnet discovery activity.",
    },
    # Blast radius violations
    "BLAST_RADIUS_EXCEEDED": {
        "delta": 30.0,
        "description": "Agent exceeded configured budget for file modifications, deletions, or process spawns.",
    },
    # Tampering & Escalation
    "SERVICE_TAMPER_ATTEMPT": {
        "delta": 50.0,
        "description": "Attempt to modify GracefulOS policies, databases, or terminate core service.",
    },
    "PRIVILEGE_ESCALATION_ATTEMPT": {
        "delta": 50.0,
        "description": "Attempt to alter token privileges, bypass Job Object, or inject into host processes.",
    },
}

def get_signal_delta(signal_code: str) -> float:
    return float(RISK_SIGNALS.get(signal_code, {}).get("delta", 10.0))

def get_signal_description(signal_code: str) -> str:
    return str(RISK_SIGNALS.get(signal_code, {}).get("description", "Unknown security anomaly."))
