import os

from . import factorio_folder, autodetect
from .modpack import ModPack
from .mod_portal import ModPortal
from .mod import Mod
from .cache import Cache

class ModManager(object):
    def __init__(self):
        self.mod_portal = ModPortal()
        self.cache = Cache(factorio_folder.get())

    def get_pack(self, pack_name):
        return ModPack(pack_name)

    @property
    def modpacks(self):
        """A list of all available modpacks."""
        return [ModPack.from_filename(fname) for fname in os.listdir("modpacks") if fname.endswith(".txt")]

    @property
    def installed_mods(self):
        """A list of all installed mods."""
        mods = []
        ff = factorio_folder.get()
        for fname in os.listdir(ff):
            if os.path.isfile(os.path.join(ff, fname)) and fname[0] != "." and not fname.endswith(".json"):
                mods.append(Mod(fname))
        return mods

    def install_mod(self, mod):
        """Installs a mod."""
        if mod.pseudo:
            return

        if self.cache.contains(mod):
            self.cache.fetch(mod)
        else:
            self.mod_portal.download(mod)
            # TODO: process faults ^^

    def set_mods(self, mods):
        """
            Installs listed mods and disables others.
            Periodically yields Mods and Nones. Yielding a Mod means that the installation is stating, and None means that it completed.
        """
        self.cache.cache_all()
        for mod in mods:
            assert mod.exists
            yield mod
            self.install_mod(mod)
            yield None

    def install_packs(self, modpacks):
        """
            Installs all mods in given packages, disabling other mods.
            If mulitple versions of a mod are required, exit with an error message.
        """
        mods = []
        for modpack in modpacks:
            for mod in modpack.contents:
                assert mod.exists

                for m in mods:
                    if mod.name == m.name:
                        if not mod.equals(m):
                            print("Error: Conflicting versions")
                            exit(2)

                        # already added
                        continue
                mods.append(mod)
        return self.set_mods(mods)

    def install_matching(self, server):
        """Autodetect packages on a server, and install matching mods locally."""
        # retrieve mod list here, so we can crash before altering cache if needed
        mods = autodetect.detect_server_packages(server)

        return self.set_mods([Mod(name, version) for name, version in mods])
