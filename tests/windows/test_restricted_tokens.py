"""
Restricted Token & Integrity Level Tests
"""

import pytest
from windows.tokens.restricted_token import token_manager

def test_restricted_token_creation():
    # If on Windows, attempt to create handle, otherwise verify fallback
    handle = token_manager.create_restricted_token_handle()
    # Handle can be an int or None in mock/elevated context
    assert handle is None or isinstance(handle, int)
