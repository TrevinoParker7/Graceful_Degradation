"""
AppContainer Isolation Manager via Win32 Userenv API
"""

import ctypes
import sys
from ctypes import wintypes
from typing import Dict, Optional
from .profile import AppContainerProfile

class AppContainerManager:
    def __init__(self):
        self.profiles: Dict[str, AppContainerProfile] = {}
        self._is_windows = sys.platform == "win32"

    def create_or_get_profile(self, container_name: str, display_name: str = "") -> AppContainerProfile:
        if container_name in self.profiles:
            return self.profiles[container_name]

        profile = AppContainerProfile(
            container_name=container_name,
            display_name=display_name or f"GracefulOS_{container_name}",
        )

        if self._is_windows:
            try:
                userenv = ctypes.WinDLL("userenv", use_last_error=True)
                # CreateAppContainerProfile(pszAppContainerName, pszDisplayName, pszDescription, pCapabilities, dwCapabilityCount, ppSidAppContainerSid)
                # If already exists, HRESULT is usually S_OK or HRESULT_FROM_WIN32(ERROR_ALREADY_EXISTS)
                pp_sid = ctypes.c_void_p()
                hr = userenv.CreateAppContainerProfile(
                    profile.container_name,
                    profile.display_name,
                    profile.description,
                    None,
                    0,
                    ctypes.byref(pp_sid),
                )
                profile.sid = f"S-1-15-2-GracefulOS-{container_name}"
            except Exception as e:
                profile.sid = f"S-1-15-2-MOCK-{container_name}"
        else:
            profile.sid = f"S-1-15-2-MOCK-{container_name}"

        self.profiles[container_name] = profile
        return profile

    def delete_profile(self, container_name: str) -> bool:
        if not self._is_windows:
            self.profiles.pop(container_name, None)
            return True

        try:
            userenv = ctypes.WinDLL("userenv", use_last_error=True)
            hr = userenv.DeleteAppContainerProfile(container_name)
            self.profiles.pop(container_name, None)
            return hr == 0
        except Exception:
            return False

appcontainer_manager = AppContainerManager()
