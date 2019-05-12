from tools.tools import *

__all__ = ('Program',)


class Program:
    # noinspection PyBroadException
    @staticmethod
    def start(settings_filename: str):
        print('Starting to clean processes...')
        try:
            clean_processes(settings_filename)
            print('Alright we are done!')
            input('Press Enter to continue...')
        except Exception:
            print('Something went wrong. I dunno what exactly, cuz I do not log any operations...')
