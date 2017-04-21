import sys

if sys.version_info[0] != 3:
    print("This program requires Python 3.")
    print("You can get it from https://www.python.org/downloads/")
    exit(1)

import os
from mod_manager.cache import *

from . import factorio_folder, autodetect
from .modpack import ModPack
from .mod_portal import ModPortal
from .mod import Mod

class ModManager(object):
    def __init__(self):
        self.mod_portal = mod_portal.ModPortal()

    def get_pack(self, pack_name):
        return ModPack(pack_name)

    @property
    def modpacks(self):
        return [ModPack.from_filename(fname) for fname in os.listdir("modpacks") if fname.endswith(".txt")]

    @property
    def installed_mods(self):
        files = [fname.rsplit(".", 1) for fname in os.listdir(factorio_folder.get()) if fname.endswith(".zip")]
        print(factorio_folder.get())
        print(os.listdir(factorio_folder.get()))
        return [Mod(fname.rsplit("_", 1)) for fname in files]

    def install_pack(self, modpack):
        mod_folder = factorio_folder.get()

        # Initialize the cache
        cache = Cache(mod_folder)

        # Handle old mods
        cache.cache_all()

        # Install new mods
        for mod in modpack.contents:
            if mod.exists:
                if cache.contains(mod):
                     # If mod is in cache, get it.
                    cache.fetch(mod)
                else:
                    yield "Downloading: " + mod.name + "..."
                    self.mod_portal.download(mod)
                    # TODO: process faults ^^
                    yield " done\n"
            else:
                # TODO: do something about this!
                pass

    def install_matching(self, server):
        """Autodetect packages on a server, and install matching mods locally."""
        # retrieve mod list here, so we can crash before altering cache if needed
        mods = autodetect.detect_server_packages(server)

        # chache old packages
        mod_folder = factorio_folder.get()

        # Initialize the cache
        cache = Cache(mod_folder)

        # Handle old mods
        cache.cache_all()

        for name, version in mods:
            mod = Mod(name, version)
            if not mod.pseudo:
                yield "Downloading: " + mod.name + "..."
                self.mod_portal.download(mod)
                yield " done\n"
