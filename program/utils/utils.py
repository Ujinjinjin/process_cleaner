import ctypes
import sys
import os
from abc import ABC, abstractmethod

__all__ = ('BaseUtils', 'WindowsUtils', 'LinuxUtils',)


class BaseUtils(ABC):
    """Doc"""
    def __init__(self, main_file: str):
        self.main_file = main_file

    @abstractmethod
    def is_admin(self) -> bool:
        """Doc"""
        pass

    @abstractmethod
    def restart_as_admin(self) -> None:
        """Doc"""
        pass


class WindowsUtils(BaseUtils):
    """Doc"""
    # noinspection PyBroadException
    def is_admin(self) -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

    def restart_as_admin(self):
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, self.main_file, None, 1)


class LinuxUtils(BaseUtils):
    """Doc"""
    def is_admin(self) -> bool:
        return os.geteuid() == 0

    def restart_as_admin(self):
        os.execvp('sudo', ['sudo'] + ['python'] + sys.argv)
