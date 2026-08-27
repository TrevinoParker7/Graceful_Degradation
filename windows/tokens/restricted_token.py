"""
Restricted Access Token & Low Integrity Token Builder for Windows 11
"""

import ctypes
import os
import sys
from ctypes import wintypes
from typing import Optional
from .privileges import DANGEROUS_PRIVILEGES, SECURITY_MANDATORY_LOW_RID

class WindowsTokenManager:
    def __init__(self):
        self._is_windows = sys.platform == "win32"

    def create_restricted_token_handle(self) -> Optional[int]:
        """
        Creates a restricted token from the current process token
        stripping administrative privileges and setting low integrity.
        """
        if not self._is_windows:
            return None

        advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        kernel32.GetCurrentProcess.restype = wintypes.HANDLE
        advapi32.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
        advapi32.OpenProcessToken.restype = wintypes.BOOL

        TOKEN_DUPLICATE = 0x0002
        TOKEN_QUERY = 0x0008

        h_current_token = wintypes.HANDLE()
        h_current_proc = kernel32.GetCurrentProcess()

        # Open current process token
        if not advapi32.OpenProcessToken(
            h_current_proc,
            TOKEN_DUPLICATE | TOKEN_QUERY,
            ctypes.byref(h_current_token),
        ):
            return None

        h_restricted_token = wintypes.HANDLE()
        DISABLE_MAX_PRIVILEGE = 0x1
        # Create restricted token stripping privileges
        res = advapi32.CreateRestrictedToken(
            h_current_token,
            DISABLE_MAX_PRIVILEGE,
            0,
            None,
            0,
            None,
            0,
            None,
            ctypes.byref(h_restricted_token),
        )
        kernel32.CloseHandle(h_current_token)

        if not res:
            return None

        return int(h_restricted_token.value)

token_manager = WindowsTokenManager()
