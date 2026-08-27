"""
SQLite-backed Append-Only Cryptographic Audit Ledger
"""

import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from config.settings import config
from .hasher import GENESIS_HASH, compute_record_hash
from .models import AuditRecord, IncidentRecord, ApprovalRequest

class AuditLedger:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or config.db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Audit records table (append-only hash chained)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_id TEXT UNIQUE NOT NULL,
                    timestamp TEXT NOT NULL,
                    agent_id TEXT,
                    event_type TEXT NOT NULL,
                    action_name TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    risk_score_before REAL NOT NULL,
                    risk_score_after REAL NOT NULL,
                    degradation_state TEXT NOT NULL,
                    details_json TEXT NOT NULL,
                    prev_hash TEXT NOT NULL,
                    current_hash TEXT NOT NULL
                )
            """)
            
            # Incidents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    incident_id TEXT UNIQUE NOT NULL,
                    timestamp TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    status TEXT NOT NULL,
                    trigger_rule TEXT NOT NULL,
                    risk_score REAL NOT NULL,
                    summary TEXT NOT NULL,
                    details_json TEXT NOT NULL,
                    snapshot_path TEXT,
                    resolved_by TEXT,
                    resolved_at TEXT
                )
            """)

            # Approval requests table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS approval_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id TEXT UNIQUE NOT NULL,
                    timestamp TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    tool_name TEXT NOT NULL,
                    action_description TEXT NOT NULL,
                    parameters_json TEXT NOT NULL,
                    risk_score REAL NOT NULL,
                    status TEXT NOT NULL,
                    reviewed_by TEXT,
                    reviewed_at TEXT,
                    reviewer_notes TEXT
                )
            """)

            # Agents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agents (
                    agent_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    mission TEXT NOT NULL,
                    model TEXT NOT NULL,
                    trust_score REAL NOT NULL,
                    risk_score REAL NOT NULL,
                    degradation_state TEXT NOT NULL,
                    registered_at TEXT NOT NULL,
                    last_active_at TEXT NOT NULL,
                    job_object_name TEXT,
                    status TEXT NOT NULL,
                    descriptor_json TEXT NOT NULL
                )
            """)
            
            conn.commit()

    def get_latest_hash(self) -> str:
        """Fetch the current head hash from the ledger chain."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT current_hash FROM audit_records ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            return row["current_hash"] if row else GENESIS_HASH

    def append_record(
        self,
        event_type: str,
        action_name: str,
        decision: str,
        risk_score_before: float,
        risk_score_after: float,
        degradation_state: str,
        agent_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditRecord:
        """Atomically append a tamper-evident record to the audit chain."""
        details = details or {}
        record_id = f"aud-{uuid.uuid4().hex[:12]}"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT current_hash FROM audit_records ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            prev_hash = row["current_hash"] if row else GENESIS_HASH
            
            timestamp = details.get("timestamp") or AuditRecord(
                record_id=record_id,
                event_type=event_type,
                action_name=action_name,
                decision=decision,
                risk_score_before=risk_score_before,
                risk_score_after=risk_score_after,
                degradation_state=degradation_state,
                prev_hash=prev_hash,
                current_hash="",
            ).timestamp

            current_hash = compute_record_hash(
                record_id=record_id,
                timestamp=timestamp,
                agent_id=agent_id,
                event_type=event_type,
                action_name=action_name,
                decision=decision,
                risk_score_before=risk_score_before,
                risk_score_after=risk_score_after,
                degradation_state=degradation_state,
                details=details,
                prev_hash=prev_hash,
            )

            cursor.execute(
                """
                INSERT INTO audit_records (
                    record_id, timestamp, agent_id, event_type, action_name,
                    decision, risk_score_before, risk_score_after,
                    degradation_state, details_json, prev_hash, current_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    timestamp,
                    agent_id,
                    event_type,
                    action_name,
                    decision,
                    risk_score_before,
                    risk_score_after,
                    degradation_state,
                    json.dumps(details),
                    prev_hash,
                    current_hash,
                ),
            )
            conn.commit()

            return AuditRecord(
                id=cursor.lastrowid,
                record_id=record_id,
                timestamp=timestamp,
                agent_id=agent_id,
                event_type=event_type,
                action_name=action_name,
                decision=decision,
                risk_score_before=risk_score_before,
                risk_score_after=risk_score_after,
                degradation_state=degradation_state,
                details=details,
                prev_hash=prev_hash,
                current_hash=current_hash,
            )

    def verify_chain_integrity(self) -> Dict[str, Any]:
        """Validate every block in the hash chain to prove ledger has not been tampered with."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM audit_records ORDER BY id ASC")
            rows = cursor.fetchall()
            
            if not rows:
                return {"valid": True, "total_records": 0, "status": "EMPTY_LEDGER"}

            expected_prev = GENESIS_HASH
            for idx, row in enumerate(rows):
                details = json.loads(row["details_json"])
                calculated_hash = compute_record_hash(
                    record_id=row["record_id"],
                    timestamp=row["timestamp"],
                    agent_id=row["agent_id"],
                    event_type=row["event_type"],
                    action_name=row["action_name"],
                    decision=row["decision"],
                    risk_score_before=row["risk_score_before"],
                    risk_score_after=row["risk_score_after"],
                    degradation_state=row["degradation_state"],
                    details=details,
                    prev_hash=row["prev_hash"],
                )

                if row["prev_hash"] != expected_prev:
                    return {
                        "valid": False,
                        "broken_at_id": row["id"],
                        "record_id": row["record_id"],
                        "reason": f"prev_hash mismatch at row {idx+1}. Expected {expected_prev}, got {row['prev_hash']}",
                    }

                if row["current_hash"] != calculated_hash:
                    return {
                        "valid": False,
                        "broken_at_id": row["id"],
                        "record_id": row["record_id"],
                        "reason": f"current_hash corrupt at row {idx+1}. Calculated {calculated_hash}, stored {row['current_hash']}",
                    }

                expected_prev = row["current_hash"]

            return {
                "valid": True,
                "total_records": len(rows),
                "head_hash": expected_prev,
                "status": "VERIFIED_TAMPER_FREE",
            }

    def list_records(self, limit: int = 100, agent_id: Optional[str] = None) -> List[AuditRecord]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if agent_id:
                cursor.execute(
                    "SELECT * FROM audit_records WHERE agent_id = ? ORDER BY id DESC LIMIT ?",
                    (agent_id, limit),
                )
            else:
                cursor.execute("SELECT * FROM audit_records ORDER BY id DESC LIMIT ?", (limit,))
            
            rows = cursor.fetchall()
            return [
                AuditRecord(
                    id=row["id"],
                    record_id=row["record_id"],
                    timestamp=row["timestamp"],
                    agent_id=row["agent_id"],
                    event_type=row["event_type"],
                    action_name=row["action_name"],
                    decision=row["decision"],
                    risk_score_before=row["risk_score_before"],
                    risk_score_after=row["risk_score_after"],
                    degradation_state=row["degradation_state"],
                    details=json.loads(row["details_json"]),
                    prev_hash=row["prev_hash"],
                    current_hash=row["current_hash"],
                )
                for row in rows
            ]

    def record_incident(
        self,
        agent_id: str,
        severity: str,
        trigger_rule: str,
        risk_score: float,
        summary: str,
        details: Optional[Dict[str, Any]] = None,
        snapshot_path: Optional[str] = None,
    ) -> IncidentRecord:
        incident_id = f"inc-{uuid.uuid4().hex[:8]}"
        details = details or {}
        record = IncidentRecord(
            incident_id=incident_id,
            agent_id=agent_id,
            severity=severity,
            status="CONTAINED" if risk_score >= 95 else "ACTIVE",
            trigger_rule=trigger_rule,
            risk_score=risk_score,
            summary=summary,
            details=details,
            snapshot_path=snapshot_path,
        )

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO incidents (
                    incident_id, timestamp, agent_id, severity, status,
                    trigger_rule, risk_score, summary, details_json, snapshot_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.incident_id,
                    record.timestamp,
                    record.agent_id,
                    record.severity,
                    record.status,
                    record.trigger_rule,
                    record.risk_score,
                    record.summary,
                    json.dumps(record.details),
                    record.snapshot_path,
                ),
            )
            conn.commit()
            record.id = cursor.lastrowid
            return record

    def list_incidents(self, limit: int = 50) -> List[IncidentRecord]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM incidents ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [
                IncidentRecord(
                    id=row["id"],
                    incident_id=row["incident_id"],
                    timestamp=row["timestamp"],
                    agent_id=row["agent_id"],
                    severity=row["severity"],
                    status=row["status"],
                    trigger_rule=row["trigger_rule"],
                    risk_score=row["risk_score"],
                    summary=row["summary"],
                    details=json.loads(row["details_json"]),
                    snapshot_path=row["snapshot_path"],
                    resolved_by=row["resolved_by"],
                    resolved_at=row["resolved_at"],
                )
                for row in rows
            ]

    def create_approval_request(
        self,
        agent_id: str,
        tool_name: str,
        action_description: str,
        parameters: Dict[str, Any],
        risk_score: float,
    ) -> ApprovalRequest:
        request_id = f"apr-{uuid.uuid4().hex[:8]}"
        req = ApprovalRequest(
            request_id=request_id,
            agent_id=agent_id,
            tool_name=tool_name,
            action_description=action_description,
            parameters=parameters,
            risk_score=risk_score,
            status="PENDING",
        )
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO approval_requests (
                    request_id, timestamp, agent_id, tool_name, action_description,
                    parameters_json, risk_score, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    req.request_id,
                    req.timestamp,
                    req.agent_id,
                    req.tool_name,
                    req.action_description,
                    json.dumps(req.parameters),
                    req.risk_score,
                    req.status,
                ),
            )
            conn.commit()
            req.id = cursor.lastrowid
            return req

    def list_approvals(self, status: Optional[str] = None) -> List[ApprovalRequest]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute(
                    "SELECT * FROM approval_requests WHERE status = ? ORDER BY id DESC",
                    (status,),
                )
            else:
                cursor.execute("SELECT * FROM approval_requests ORDER BY id DESC")
            rows = cursor.fetchall()
            return [
                ApprovalRequest(
                    id=row["id"],
                    request_id=row["request_id"],
                    timestamp=row["timestamp"],
                    agent_id=row["agent_id"],
                    tool_name=row["tool_name"],
                    action_description=row["action_description"],
                    parameters=json.loads(row["parameters_json"]),
                    risk_score=row["risk_score"],
                    status=row["status"],
                    reviewed_by=row["reviewed_by"],
                    reviewed_at=row["reviewed_at"],
                    reviewer_notes=row["reviewer_notes"],
                )
                for row in rows
            ]

    def resolve_approval(
        self, request_id: str, approved: bool, reviewer: str = "administrator", notes: str = ""
    ) -> Optional[ApprovalRequest]:
        import datetime
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        status = "APPROVED" if approved else "REJECTED"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE approval_requests
                SET status = ?, reviewed_by = ?, reviewed_at = ?, reviewer_notes = ?
                WHERE request_id = ?
                """,
                (status, reviewer, now, notes, request_id),
            )
            conn.commit()
            cursor.execute("SELECT * FROM approval_requests WHERE request_id = ?", (request_id,))
            row = cursor.fetchone()
            if row:
                return ApprovalRequest(
                    id=row["id"],
                    request_id=row["request_id"],
                    timestamp=row["timestamp"],
                    agent_id=row["agent_id"],
                    tool_name=row["tool_name"],
                    action_description=row["action_description"],
                    parameters=json.loads(row["parameters_json"]),
                    risk_score=row["risk_score"],
                    status=row["status"],
                    reviewed_by=row["reviewed_by"],
                    reviewed_at=row["reviewed_at"],
                    reviewer_notes=row["reviewer_notes"],
                )
            return None

# Global audit ledger instance
audit_ledger = AuditLedger()
