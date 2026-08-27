"""
Unit Tests for SQLite Cryptographic Audit Ledger
"""

import pytest
from pathlib import Path
from core.audit.ledger import AuditLedger

def test_audit_hash_chain_integrity(tmp_path):
    db_file = tmp_path / "test_audit.db"
    ledger = AuditLedger(db_path=db_file)

    # 1. Append records
    r1 = ledger.append_record("TEST", "action_1", "ALLOW", 0.0, 10.0, "NORMAL")
    r2 = ledger.append_record("TEST", "action_2", "DENY", 10.0, 35.0, "WATCH")
    r3 = ledger.append_record("TEST", "action_3", "KILL", 35.0, 100.0, "CONTAINED")

    # 2. Verify chain
    assert r2.prev_hash == r1.current_hash
    assert r3.prev_hash == r2.current_hash

    integrity = ledger.verify_chain_integrity()
    assert integrity["valid"] is True
    assert integrity["total_records"] == 3
