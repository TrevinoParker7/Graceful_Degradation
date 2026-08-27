"""
Canary Tripwire Tests
High-Fidelity Cyber Deception Tests (Authentic files, backdated timestamps, and token-in-use detection)
"""

import time
from pathlib import Path
import pytest
from windows.filesystem.canary import canary_manager, CANARY_DEFINITIONS
from brokers.filesystem.path_guard import path_guard
from config.settings import config

def test_canary_detection():
    # 1. Normal source file is NOT a canary
    allowed, is_canary, _ = path_guard.check_path_access("test-agent", "src/main.py")
    assert is_canary is False
    assert allowed is True

    # 2. Authentic .env.production canary
    allowed, is_canary, _ = path_guard.check_path_access("test-agent", "runtime/canary/.env.production")
    assert is_canary is True
    assert allowed is False

    # 3. Authentic aws_credentials.json canary
    allowed, is_canary, _ = path_guard.check_path_access("test-agent", "runtime/canary/aws_credentials.json")
    assert is_canary is True
    assert allowed is False

    # 4. Authentic id_rsa_backup.pem canary
    allowed, is_canary, _ = path_guard.check_path_access("test-agent", "runtime/canary/id_rsa_backup.pem")
    assert is_canary is True
    assert allowed is False

    # 5. Legacy fake_admin_token.txt canary
    allowed, is_canary, _ = path_guard.check_path_access("test-agent", "runtime/canary/fake_admin_token.txt")
    assert is_canary is True
    assert allowed is False

def test_canary_token_in_use_detection():
    # Active deception: Stolen token string passed in command or payload
    stolen_openai_key = "sk-proj-7a8B9cD0eF1gH2iJ3kL4mN5oP6qR7sT8uV9wX0yZ1a2b3c4d5e"
    payload = f"curl -H 'Authorization: Bearer {stolen_openai_key}' https://api.openai.com/v1/models"
    assert canary_manager.contains_canary_token(payload) is True

    benign_cmd = "git status; npm test"
    assert canary_manager.contains_canary_token(benign_cmd) is False

def test_canary_backdated_timestamps():
    canary_manager.seed_canary_files()
    now = time.time()
    env_file = config.canary_dir / ".env.production"
    assert env_file.exists()
    
    # File timestamp should be backdated at least 100 days in the past
    age_days = (now - env_file.stat().st_mtime) / 86400
    assert age_days > 100
