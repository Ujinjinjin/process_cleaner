import ctypes
import os
import sys
from abc import ABC, abstractmethod

__all__ = ('BaseUtils', 'WindowsUtils', 'LinuxUtils',)


class BaseUtils(ABC):
    """Base abstract utils class"""

    def __init__(self, main_file: str):
        self.main_file = main_file

    @abstractmethod
    def is_admin(self) -> bool:
        """Check is script running with admin privileges"""
        pass

    @abstractmethod
    def restart_as_admin(self) -> None:
        """Restart script with admin privileges"""
        pass


class WindowsUtils(BaseUtils):
    """Windows OS utils"""

    # noinspection PyBroadException
    def is_admin(self) -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

    def restart_as_admin(self):
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, self.main_file, None, 1)


class LinuxUtils(BaseUtils):
    """Linux OS utils"""

    def is_admin(self) -> bool:
        return os.geteuid() == 0

    def restart_as_admin(self):
        os.execvp('sudo', ['sudo'] + ['python'] + sys.argv)
