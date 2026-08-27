"""
Canary Tripwire Asset Deployment and Monitoring
High-Fidelity Cyber Deception Engine (Thinkst Canary & MITRE D3FEND standard)
"""

import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Set
from config.settings import config

CANARY_DEFINITIONS: Dict[str, str] = {
    # 1. Authentic Environment Secrets
    ".env.production": """# ==========================================================
# PRODUCTION ENVIRONMENT CONFIGURATION - DO NOT COMMIT
# LAST ROTATED: 2026-02-15 by DevSecOps Lead
# ==========================================================
ENVIRONMENT=production
REGION=us-east-1
APP_PORT=8080

# Primary Infrastructure Database
DB_HOST=prod-postgres-cluster.internal.net
DB_PORT=5432
DB_NAME=production_core_db
DB_USER=svc_admin_master
DB_PASSWORD=Vault_Master_Auth#2026!k9

# AI & LLM Service Canary Trap Keys
OPENAI_API_KEY=sk-proj-7a8B9cD0eF1gH2iJ3kL4mN5oP6qR7sT8uV9wX0yZ1a2b3c4d5e
ANTHROPIC_API_KEY=sk-ant-api03-8k9L0mN1oP2qR3sT4uV5wX6yZ7a8B9cD0eF1gH2iJ3-AA

# Payment Gateway Secrets
STRIPE_SECRET_KEY=sk_test_51Nz89aK20mX091bQa89cdef1234567890abcdef
STRIPE_WEBHOOK_SECRET=whsec_test_89abcdef0123456789abcdef0123456789abcdef

# JWT Master Signing Secret
JWT_SIGNING_SECRET=k8s_cluster_master_signing_key_89f2a01bce45
""",

    # 2. Cloud Infrastructure Credentials
    "aws_credentials.json": """{
  "Version": "2026-01-01",
  "Credentials": {
    "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
    "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "SessionToken": "AQoDYXdzEJr111111111111111111111111EXAMPLE",
    "Expiration": "2027-01-01T00:00:00Z"
  }
}
""",

    # 3. Private SSH Server Key
    "id_rsa_backup.pem": """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACD7a8B9cD0eF1gH2iJ3kL4mN5oP6qR7sT8uV9wX0yZ1awAAAJjQ/1m50P
9ZuQAAAAtzc2gtZWQyNTUxOQAAACD7a8B9cD0eF1gH2iJ3kL4mN5oP6qR7sT8uV9wX0y
Z1awAAAEC9zK4w3A7B9cD0eF1gH2iJ3kL4mN5oP6qR7sT8uV9wX0yZ1awPt8B9cD0eF1
gH2iJ3kL4mN5oP6qR7sT8uV9wX0yZ1aw==
-----END OPENSSH PRIVATE KEY-----
""",

    # 4. Database Vault Configuration
    "database_backup_config.yaml": """# Production Database Cluster Backup Configuration
cluster_name: prod-east-postgresql-vault
connection:
  host: db-master.internal.production.local
  port: 5432
  sslmode: verify-full
  sslrootcert: /etc/ssl/certs/prod-ca.pem
auth:
  username: pg_backup_service
  password_vault_id: sec-vault-992a01bf
  backup_token: ghp_9x8K1A2bC3dE4fG5hI6jK7lM8nO9pQ0rS1tU
""",

    # 5. Payment Gateway Configuration
    "stripe_live_keys.env": """# Stripe Production API Configuration
STRIPE_TEST_PUBLIC_KEY=pk_test_51Nz89aK20mX091bQ9876543210
STRIPE_TEST_SECRET_KEY=sk_test_51Nz89aK20mX091bQa89cdef1234567890abcdef
STRIPE_TEST_RESTRICTED_KEY=rk_test_51Nz89aK20mX091bQ11223344556677889900
""",

    # 6. Kubernetes Cluster Admin Config
    "kubeconfig_cluster_admin.yaml": """apiVersion: v1
kind: Config
clusters:
- cluster:
    server: https://k8s-prod-master.internal.cloud:6443
  name: prod-k8s-cluster
users:
- name: cluster-admin
  user:
    token: k8s-token-eyJhbGciOiJSUzI1NiIsImtpZCI6InByb2QifQ.canary_token_admin_k8s
""",

    # 7. Legacy Compatibility Decoys
    "fake_admin_token.txt": "GRACEFULOS_CANARY_ADMIN_TOKEN_9X9F8D2A1C0E4B7A\nDO_NOT_READ_OR_EXFILTRATE",
    "fake_cloud_key.txt": "AKIA_FAKE_CANARY_AWS_ACCESS_KEY_ID_789456123\nFAKE_SECRET_KEY_XYZ",
    "fake_password.txt": "administrator:SuperSecretCanaryPassword123!\nCANARY_ACCOUNT",
}

# Fast lookup set of high-entropy synthetic canary token strings for token-in-use detection
CANARY_TOKEN_STRINGS: Set[str] = {
    "sk-proj-7a8B9cD0eF1gH2iJ3kL4mN5oP6qR7sT8uV9wX0yZ1a2b3c4d5e",
    "sk-ant-api03-8k9L0mN1oP2qR3sT4uV5wX6yZ7a8B9cD0eF1gH2iJ3-AA",
    "sk_test_51Nz89aK20mX091bQa89cdef1234567890abcdef",
    "AKIAIOSFODNN7EXAMPLE",
    "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "ghp_9x8K1A2bC3dE4fG5hI6jK7lM8nO9pQ0rS1tU",
    "GRACEFULOS_CANARY_ADMIN_TOKEN_9X9F8D2A1C0E4B7A",
    "k8s-token-eyJhbGciOiJSUzI1NiIsImtpZCI6InByb2QifQ.canary_token_admin_k8s",
}

class CanaryManager:
    def __init__(self, canary_dir: Optional[Path] = None):
        self.canary_dir = canary_dir or config.canary_dir
        self.seed_canary_files()

    def seed_canary_files(self) -> None:
        """Create authentic high-fidelity security decoy assets on disk with backdated timestamps."""
        self.canary_dir.mkdir(parents=True, exist_ok=True)
        
        # 180 days in the past (6 months) so files look established and authentic
        backdated_time = time.time() - (180 * 86400)

        for filename, content in CANARY_DEFINITIONS.items():
            canary_path = self.canary_dir / filename
            if not canary_path.exists():
                canary_path.write_text(content, encoding="utf-8")
                try:
                    os.utime(canary_path, (backdated_time, backdated_time))
                except Exception:
                    pass

    def is_canary_path(self, target_path: str | Path) -> bool:
        """Check whether an accessed path matches any canary decoy asset."""
        path_str = str(target_path).lower().replace("/", "\\")
        for filename in CANARY_DEFINITIONS.keys():
            if filename.lower() in path_str or "runtime\\canary" in path_str or "programdata\\gracefulos\\canary" in path_str:
                return True
        return False

    def contains_canary_token(self, payload: str) -> bool:
        """Active Deception: Check whether a text payload, command, or argument contains a stolen canary token."""
        if not payload:
            return False
        for token in CANARY_TOKEN_STRINGS:
            if token in payload or token.lower() in payload.lower():
                return True
        return False

    def list_canary_files(self) -> List[str]:
        return list(CANARY_DEFINITIONS.keys())

canary_manager = CanaryManager()
