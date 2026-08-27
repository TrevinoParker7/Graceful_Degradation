"""
Windows Data Protection API (DPAPI) and Credential Manager Encrypted Storage
"""

import base64
import sys
from typing import Optional

class WindowsDpapiService:
    def __init__(self):
        self._is_windows = sys.platform == "win32"

    def encrypt_secret(self, plaintext: str) -> str:
        """Encrypt secret using Windows DPAPI (CryptProtectData) or local fallback."""
        if not self._is_windows:
            return base64.b64encode(plaintext.encode("utf-8")).decode("utf-8")

        try:
            import win32crypt
            encrypted = win32crypt.CryptProtectData(plaintext.encode("utf-8"), "GracefulOS_Secret", None, None, None, 0)
            return base64.b64encode(encrypted).decode("utf-8")
        except Exception:
            return base64.b64encode(plaintext.encode("utf-8")).decode("utf-8")

    def decrypt_secret(self, ciphertext_b64: str) -> Optional[str]:
        if not self._is_windows:
            try:
                return base64.b64decode(ciphertext_b64.encode("utf-8")).decode("utf-8")
            except Exception:
                return None

        try:
            import win32crypt
            raw = base64.b64decode(ciphertext_b64.encode("utf-8"))
            description, decrypted = win32crypt.CryptUnprotectData(raw, None, None, None, 0)
            return decrypted.decode("utf-8")
        except Exception:
            try:
                return base64.b64decode(ciphertext_b64.encode("utf-8")).decode("utf-8")
            except Exception:
                return None

dpapi_service = WindowsDpapiService()
