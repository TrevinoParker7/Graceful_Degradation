"""
Blast Radius Budget Enforcement Tests
"""

import pytest
from core.risk.blast_radius import BlastRadiusTracker, BlastRadiusBudget

def test_blast_radius_limits():
    budget = BlastRadiusBudget(max_files_modified=3, max_powershell_commands=2)
    tracker = BlastRadiusTracker("test-agent-blast", budget)

    # File modifications
    assert tracker.record_file_modification() is True
    assert tracker.record_file_modification() is True
    assert tracker.record_file_modification() is True
    assert tracker.record_file_modification() is False  # Exceeded!

    # Within budget check
    ok, reason = tracker.is_within_budget()
    assert ok is False
    assert "Files modified" in reason
