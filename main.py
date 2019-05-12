import ctypes
import sys

from tools.tools import *
from program import Program


if __name__ == '__main__':
    if is_admin():
        # Run program
        Program.start('settings.json')
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)