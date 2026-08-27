"""
Adversarial Tests: PowerShell Command Obfuscation & Evasion
"""

import pytest
from brokers.powershell.analyzer import powershell_analyzer

def test_powershell_obfuscation_detection():
    # 1. Base64 Encoded Command
    res = powershell_analyzer.analyze_command("powershell -enc SUVYIChOZXctT2JqZWN0IE5ldC5XZWJDbGllbnQp")
    assert res["is_dangerous"] is True
    assert "Base64" in res["reason"]

    # 2. Dynamic Expression Evaluation (IEX)
    res = powershell_analyzer.analyze_command("iex (Get-Content payload.ps1)")
    assert res["is_dangerous"] is True
    assert "IEX" in res["reason"]

    # 3. Recursive Profile Deletion
    res = powershell_analyzer.analyze_command("Remove-Item C:\\Users\\Administrator -Recurse -Force")
    assert res["is_dangerous"] is True
    assert "Recursive deletion" in res["reason"]
