"""
Browser Automation Guard and URL Allowlist
"""

from typing import Set

BROWSER_ALLOWLIST: Set[str] = {
    "http://127.0.0.1:7777",
    "http://localhost:7777",
    "https://docs.python.org",
    "https://pypi.org",
}
