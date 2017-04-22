import os.path

from . import autodetect
from .modpack import ModPack
from .mod_portal import ModPortal
from .mod import Mod
from .mod_cache import ModCache
from .folders import mod_folder, modpack_folder
from .exceptions import InstallationVersionConflict

class ModManager(object):
    def __init__(self):
        self.mod_portal = ModPortal(self)
        self.mod_cache = ModCache(self)

    def get_pack(self, pack_name):
        return ModPack(self, pack_name)

    @property
    def modpacks(self):
        """A list of all available modpacks."""
        return [ModPack.from_filename(self, fname) for fname in modpack_folder.files if fname.endswith(".txt")]

    @property
    def installed_mods(self):
        """A list of all installed mods."""
        mods = []
        for fname in mod_folder.files:
            if os.path.isfile(mod_folder.file_path(fname)) and fname[0] != "." and not fname.endswith(".json"):
                mods.append(Mod(self.mod_portal.api_cache, fname))
        return mods

    def decompress_modpack(self, data):
        return ModPack.decompress(self, data)

    def install_mod(self, mod):
        """Installs a mod."""
        if mod.pseudo:
            return

        if self.mod_cache.contains(mod):
            self.mod_cache.fetch(mod)
        else:
            self.mod_portal.login()

            self.mod_portal.download(mod)
            # TODO: process faults ^^

    def set_mods(self, mods):
        """
            Installs listed mods and disables others.
            Periodically yields Mods and Nones. Yielding a Mod means that the installation is stating, and None means that it completed.
        """
        self.mod_cache.cache_all()
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
                            raise InstallationVersionConflict()

                        # already added
                        continue
                mods.append(mod)
        return self.set_mods(mods)

    def install_matching(self, server):
        """Autodetect packages on a server, and install matching mods locally."""
        # retrieve mod list here, so we can crash before altering cache if needed
        mods = autodetect.detect_server_packages(server)

        return self.set_mods([Mod(self.mod_portal.api_cache, name, version) for name, version in mods])
