import os.path

from .folders import mod_folder, cache_folder
from .mod import Mod

def parse_version(ver):
    assert ver.count(".") == 2
    return [int(x) for x in ver.split(".")]

class ModCache(object):
    """Cache is a folder in the modfolder. Cache is primarily used to store uninstalled mods in case user wants to re-install them."""
    @property
    def files(self):
        """List of all files in the cache folder."""
        return cache_folder.files

    def query(self, name):
        """Returns filenamename and version of the first mod with the given name in the cache folder."""
        for fname in self.files:
            mod_name, mod_version = fname.rsplit(".", 1)[0].rsplit("_", 1)
            if mod_name == name:
                return fname, mod_version
        return None

    def clear(self):
        """Clears all files from cache."""
        for filename in cache_folder.files:
            assert filename.endswith(".zip"), "Cache folder is supposed to contain only zip files"
            os.remove(cache_folder.file_path(filename))

    def cache(self, mod, delete=True, update=True):
        """
            Stores wanted mod to the cache.
            If delete is true, deletes the mod from the mod folder.
            If delete is true, performs automatic cleaup on cached mods.
        """
        if os.path.exists(cache_folder.file_path(mod.name)):
            if delete:
                os.remove(mod_folder.file_path(mod.name))
        else:
            target = cache_folder.file_path("_".join([mod.name, mod.version])+".zip")
            action = mod_folder.move_file if delete else mod_folder.copy_file
            action(mod.name, target)

        if update:
            self.update()

    def cache_all(self, delete=True, update=True):
        """Caches all files in the mod folder."""
        for fname in mod_folder.files:
            if os.path.isfile(mod_folder.file_path(fname)) and fname[0] != "." and not fname.endswith(".json"):
                self.cache(Mod(fname), delete=delete, update=False)

        if update:
            self.update()

    def contains(self, mod):
        """Checks if a mod with correct version exists in the cache."""
        self.update()

        q = self.query(mod.name)
        if q is None:
            return False  # No such mod found

        filename, cached_mod_version = q

        if cached_mod_version == mod.version:
            return True

        # Newest cached version is old as well
        os.remove(cache_folder.file_path(filename))
        return False

    def fetch(self, mod):
        """Gets a mod from the cache and copies it to the mod folder."""
        self.update()

        q = self.query(mod.name)
        if q is None:
            raise ValueError("Did not found the given mod")

        cache_folder.copy_file(q[0], mod_folder)

    def update(self):
        """Removes old versions of mods from the cache folder."""
        mods = {}
        for fname in self.files:
            # Drop extension and take chars after "_" to get the version number
            mod_name, mod_version = fname.rsplit(".", 1)[0].rsplit("_", 1)
            if mod_name not in mods:
                mods[mod_name] = []
            mods[mod_name].append((fname, mod_version))

        for mod_name in mods:
            # sorts in place from newest to oldest
            mods[mod_name].sort(key=lambda m: parse_version(m[1]), reverse=True)

            for fname, version in mods[mod_name][1:]:
                os.remove(cache_folder.file_path(fname))
