"""
Network Domain / IP Allowlist Manager
"""

from typing import Set

DEFAULT_NETWORK_ALLOWLIST: Set[str] = {
    "127.0.0.1", "localhost", "::1", "pypi.org", "files.pythonhosted.org", "github.com", "api.github.com"
}
