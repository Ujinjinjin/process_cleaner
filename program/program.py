import platform
from program.cleaner.cleaner import *
from program.utils.utils import *
from typing import Dict, Type

__all__ = ('Program',)


class Program:
    """Doc"""
    def __init__(self, main_file: str, settings_filename: str):
        self.main_file: str = main_file
        self.utils: BaseUtils = self._get_utils()
        self.settings_filename: str = settings_filename

    def start(self):
        """Doc"""
        if self.utils.is_admin():
            self._start()
        else:
            self.utils.restart_as_admin()

    # noinspection PyBroadException
    def _start(self):
        """Doc"""
        print('Starting to clean processes...')
        try:
            clean_processes(self.settings_filename)
            print('Alright we are done!')
            input('Press Enter to continue...')
        except Exception:
            print('Something went wrong. I dunno what exactly, cuz I do not log any operations...')

    def _get_utils(self) -> BaseUtils:
        """Doc"""
        cleaners_by_system: Dict[str, Type[BaseUtils]] = {
            'Linux': LinuxUtils,
            'Windows': WindowsUtils
        }
        platform_name: str = platform.system()
        if platform_name in cleaners_by_system.keys():
            return cleaners_by_system[platform_name](self.main_file)
        else:
            raise OSError(f'Your OS currently not supported. '
                          f'Program works on following systems: {", ".join(cleaners_by_system.keys())}')
