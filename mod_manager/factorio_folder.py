import sys
import os.path

from .cache_utils import cache_result

def default_folder():
    if sys.platform.startswith("win32"):
        return os.path.expanduser(r"~\AppData\Roaming\Factorio\mods")
    elif sys.platform.startswith("darwin"):
        return os.path.expanduser("~/Library/Application Support/factorio/mods")
    elif sys.platform.startswith("linux"):
        return os.path.expanduser("~/.factorio/mods")
    else:
        return None

def is_factorio_mods_folder(path):
    """Checks if the given folder is factorio mods folder."""
    if not os.path.isdir(path):
        return False
    return "mod-list.json" in os.listdir(path)

def is_factorio_main_folder(path):
    """Checks if the given folder is factorio main folder (config should have mods folder instead)."""
    PROBABLY_CONTAINS = ["cache", "temp", "saves", "config", "mods"]
    if not os.path.isdir(path):
        return False
    contents = os.listdir(path)
    return sum([fnanme in contents for fnanme in PROBABLY_CONTAINS]) >= len(PROBABLY_CONTAINS)/2

@cache_result
def get():
    config_exists = os.path.isfile("modman.conf")

    factorio_folder = default_folder()

    # config overwrites default folder if it exists
    if config_exists:
        # Just let possible errors upwards
        with open("modman.conf") as f:
            factorio_folder = [i for i in f.readlines() if i[0] != "#" and i != ""][0].strip()

        # append mods to get mods folder if needed
        if is_factorio_main_folder(factorio_folder):
            factorio_folder = os.path.join(factorio_folder, "mods")

    if is_factorio_mods_folder(factorio_folder):
        return factorio_folder
    else:
        print("Could not determine factorio folder")
        exit(1)
