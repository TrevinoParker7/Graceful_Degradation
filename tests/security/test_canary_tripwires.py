"""
Canary Tripwire Tests
"""

import pytest
from windows.filesystem.canary import canary_manager
from brokers.filesystem.path_guard import path_guard

def test_canary_detection():
    # 1. Normal file
    allowed, is_canary, _ = path_guard.check_path_access("test-agent", "src/main.py")
    assert is_canary is False

    # 2. Canary fake admin token
    allowed, is_canary, _ = path_guard.check_path_access("test-agent", "runtime/canary/fake_admin_token.txt")
    assert is_canary is True
    assert allowed is False
