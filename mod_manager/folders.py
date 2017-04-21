import os
import sys
import shutil

def default_folder():
    """Returns default factorio mod folder for the current OS."""
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

def get_factorio_folder():
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

def get_cache_folder():
    cache_path = os.path.join(mod_folder.path, "cache")
    if not os.path.isdir(cache_path):
        os.makedirs(cache_path)

    return os.path.join(mod_folder.path, "cache")


class _MetaFolder(type):
    @property
    def files(cls):
        """List of all files in this folder."""
        return os.listdir(cls.path)

class Folder(object, metaclass=_MetaFolder):
    @classmethod
    def file_path(cls, filename):
        """Return full path for a file"""
        return os.path.join(cls.path, filename)

    @classmethod
    def _file_action(cls, action, filename, target):
        assert isinstance(filename, str)

        if isinstance(target, Folder):
            target = target.path

        assert isinstance(target, str)

        action(cls.file_path(filename), target)

    @classmethod
    def move_file(cls, *args):
        """Move a file to another folder."""
        cls._file_action(shutil.move, *args)

    @classmethod
    def copy_file(cls, *args):
        """Copy a file to another folder."""
        cls._file_action(shutil.copy, *args)

class mod_folder(Folder):
    """Factorio mod folder."""
    path = get_factorio_folder()

class cache_folder(Folder):
    """Mod cache folder."""
    path = get_cache_folder()

class modpack_folder(Folder):
    """Application modpack folder."""
    # TODO: absolute path
    path = "modpacks"
