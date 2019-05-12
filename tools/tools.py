import ctypes
import psutil
import json

from typing import List

__all__ = ('is_admin', 'clean_processes',)


# noinspection PyBroadException
def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def clean_processes(settings_filename: str) -> None:
    proc_names: List[str] = _get_proc_names(settings_filename)
    active_proc_names: List[str] = _get_active_processes(proc_names)

    total_amount: int = len(proc_names)
    active_amount: int = len(active_proc_names)
    cleaned_amount: int = 0

    print(f'\n{active_amount} out of {total_amount} processes running right now. Following processes will be killed:\n')
    for number, name in enumerate(active_proc_names):
        print(f'{number + 1}. {name}')

    print()

    print(f'Cleaned {cleaned_amount} of {active_amount}', end='\r')

    for name in active_proc_names:
        _delete_process(name)
        cleaned_amount += 1
        print(f'Cleaned {cleaned_amount} of {active_amount}', end='\r')

    print(f'Cleaned {cleaned_amount} of {active_amount}')


def _get_proc_names(settings_filename: str) -> List[str]:
    with open(settings_filename, 'r', encoding='utf8') as settings_file:
        settings = json.load(settings_file)
        return settings['process_names']


def _get_active_processes(proc_names: List[str]) -> List[str]:
    active_processes: List[str] = list()
    for proc in psutil.process_iter():
        if proc.name() in proc_names and proc.name() not in active_processes:
            active_processes.append(proc.name())
    return active_processes


# noinspection PyBroadException
def _delete_process(name: str) -> None:
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == name:
            proc.kill()
