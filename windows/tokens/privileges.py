"""
Windows Privilege & Integrity Level Constants
"""

# Windows Integrity Level SIDs
SECURITY_MANDATORY_UNTRUSTED_RID = 0x0000
SECURITY_MANDATORY_LOW_RID = 0x1000
SECURITY_MANDATORY_MEDIUM_RID = 0x2000
SECURITY_MANDATORY_HIGH_RID = 0x3000
SECURITY_MANDATORY_SYSTEM_RID = 0x4000

# Privileges to strip from untrusted agent tokens
DANGEROUS_PRIVILEGES = [
    "SeDebugPrivilege",
    "SeImpersonatePrivilege",
    "SeTakeOwnershipPrivilege",
    "SeBackupPrivilege",
    "SeRestorePrivilege",
    "SeLoadDriverPrivilege",
    "SeSystemtimePrivilege",
    "SeShutdownPrivilege",
    "SeSecurityPrivilege",
    "SeCreateTokenPrivilege",
    "SeAssignPrimaryTokenPrivilege",
]
