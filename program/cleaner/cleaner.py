import json
from typing import List

import psutil

__all__ = ('Cleaner',)


class Cleaner:
    """Process cleaner"""

    def __init__(self, settings_filename: str):
        self.processes: List[str] = list()
        self.active_processes: List[str] = list()

        self._get_processes(settings_filename)
        self._get_active_processes()

    def clean_processes(self) -> None:
        """Clean system processes by killing those from settings file"""
        total_amount: int = len(self.processes)
        active_amount: int = len(self.active_processes)
        cleaned_amount: int = 0

        print(
            f'\n{active_amount} out of {total_amount} processes running right now. Following processes will be killed:\n')
        for number, name in enumerate(self.active_processes):
            print(f'{number + 1}. {name}')

        print()

        print(f'Cleaned {cleaned_amount} of {active_amount}', end='\r')

        for name in self.active_processes:
            self._kill_process(name)
            cleaned_amount += 1
            print(f'Cleaned {cleaned_amount} of {active_amount}', end='\r')

        print(f'Cleaned {cleaned_amount} of {active_amount}')

    def _get_processes(self, settings_filename: str) -> None:
        """Get process names from settings file"""
        with open(settings_filename, 'r', encoding='utf8') as settings_file:
            settings = json.load(settings_file)
            self.processes = settings['processes']

    def _get_active_processes(self) -> None:
        """Filter inactive processes from process list"""
        active_processes: List[str] = list()
        for proc in psutil.process_iter():
            if proc.name() in self.processes and proc.name() not in active_processes:
                active_processes.append(proc.name())
        self.active_processes = active_processes

    # noinspection PyBroadException
    @staticmethod
    def _kill_process(name: str) -> None:
        """Kill process by name"""
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == name:
                proc.kill()
