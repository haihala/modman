import os.path
import bisect

from .folders import mod_folder, mod_cache_folder

def parse_version(ver):
    assert ver.count(".") == 2
    return [int(x) for x in ver.split(".")]

class CachedMod(object):
    def __init__(self, filename):
        self.filename = filename

        modname, metadata = filename.rsplit(".", 1)[0].rsplit("_", 1)
        metadata_parts = metadata.split("-")
        assert len(metadata_parts) in [1,2]

        self.name = modname
        self.version = metadata_parts[0]
        self.timestamp = metadata_parts[1] if len(metadata) == 2 else None

    @property
    def path(self):
        return mod_cache_folder.file_path(self.filename)

    def __str__(self):
        return "CachedMod({}, {})".format(self.name, self.version)


class ModCache(object):
    """Cache is a folder in the modfolder. Cache is primarily used to store uninstalled mods in case user wants to re-install them."""
    def __init__(self, mod_manager):
        self.mod_manager = mod_manager

    @property
    def mods(self):
        """List of all files in the cache folder."""
        return [CachedMod(fname) for fname in mod_cache_folder.files]

    def reset(self):
        """Clears all files from cache."""
        for filename in mod_cache_folder.files:
            assert filename.endswith(".zip"), "Cache folder is supposed to contain only zip files"
            os.remove(mod_cache_folder.file_path(filename))

    def cache(self, mod, delete=True, update=True):
        """
            Stores wanted mod to the cache.
            If delete is true, deletes the mod from the mod folder.
            If delete is true, performs automatic cleaup on cached mods.
        """
        if os.path.exists(mod_cache_folder.file_path(mod.name)): # FIXME
            if delete:
                os.remove(mod_folder.file_path(mod.name))
        else:
            # TODO: timestamp
            target = mod_cache_folder.file_path("_".join([mod.name, mod.version])+".zip")
            action = mod_folder.move_file if delete else mod_folder.copy_file
            action(mod.name, target)

        if update:
            self.update()

    def cache_all(self, delete=True, update=True):
        """Caches all files in the mod folder."""
        for mod in self.mod_manager.installed_mods:
            self.cache(mod, delete=delete, update=False)

        if update:
            self.update()

    def contains(self, mod):
        """Checks if a mod with correct version exists in the cache."""
        for cmod in self.mods:
            if cmod.name == mod.name and cmod.version == mod.version:
                return True
        return False

    def fetch(self, mod):
        """Gets a mod from the cache and copies it to the mod folder."""
        self.update()

        for cmod in self.mods:
            if cmod.name == mod.name and cmod.version == mod.version:
                mod_cache_folder.copy_file(cmod.filename, mod_folder)
                return

        raise ValueError("Did not found the given mod")

    def update(self):
        """Removes unused old versions of mods from the cache folder."""
        all_mods = set([(m.name, m.required_version) for mp in self.mod_manager.modpacks for m in mp.contents])

        mods = {}
        for cmod in self.mods:
            if not cmod.name in mods:
                mods[cmod.name] = []
            # keep the version list sorted
            bisect.insort(mods[cmod.name], parse_version(cmod.version))

        for name, versions in mods.items():
            newest = "{}.{}.{}".format(*versions[0])
            all_versions = {"{}.{}.{}".format(*v) for v in versions}

            candidates = {v for n, v in all_mods if n == name and v}

            # preserve all mods that are a part of avalable modpack
            preserve = {v for v in all_versions if v in candidates}

            # preserve newest version of each mod
            preserve.add(newest)

            for version in (all_versions - preserve):
                cmod = CachedMod(name, version)
                assert os.path.exists(cmod.path)
                os.remove(cmod.path)
