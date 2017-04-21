import sys

if sys.version_info[0] != 3:
    print("This program requires Python 3.")
    print("You can get it from https://www.python.org/downloads/")
    exit(1)


# Re-export this
from .mod_manager import ModManager
