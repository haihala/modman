import shutil
import os.path

from .mod import Mod

def parse_version(ver):
    assert ver.count(".") == 2
    return [int(x) for x in ver.split(".")]

class Cache(object):
    """Cache is a folder in the modfolder. Cache is primarily used to store uninstalled mods in case user wants to re-install them."""
    def __init__(self, path):
        self.mod_folder = path

    @property
    def cache_folder(self):
        """Checks if cache folder exists. If it doesn't, creates one."""
        cache_path = os.path.join(self.mod_folder, "cache")
        if not os.path.isdir(cache_path):
            os.makedirs(cache_path)

        return os.path.join(self.mod_folder, "cache")

    @property
    def files(self):
        return os.listdir(os.path.join(self.cache_folder))

    def query(self, q):
        """Returns filenamename and version of the first mod with name q in the cache folder."""
        for fname in self.files:
            mod_name, mod_version = fname.rsplit(".", 1)[0].rsplit("_", 1)
            if mod_name == q:
                return fname, parse_version(mod_version)
        return None

    def clear(self):
        """Clears all files from cache."""
        for filename in os.listdir(self.cache_folder):
            assert filename.endswith(".zip"), "Cache folder is supposed to contain only zip files"
            os.remove(os.path.join(self.cache_folder, filename))

    def cache(self, mod, update=True):
        """Stores wanted mod to the cache. Deletes old versions, only holds the newest one."""
        if os.path.exists(os.path.join(self.cache_folder, mod.name)):
            os.remove(os.path.join(self.mod_folder, mod.name))
        else:
            shutil.move(
                os.path.join(self.mod_folder, mod.name),
                os.path.join(self.cache_folder, "_".join([mod.name, mod.version])+".zip")
            )

        if update:
            self.update()

    def cache_all(self):
        for fname in os.listdir(self.mod_folder):
            if os.path.isfile(os.path.join(self.mod_folder, fname)) and fname[0] != "." and not fname.endswith(".json"):
                self.cache(Mod(fname), update=False)
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
        os.remove(os.path.join(self.cache_folder, filename))
        return False

    def fetch(self, mod):
        """Gets a mod from the cache and copies it to the mod folder."""
        self.update()

        q = self.query(mod.name)
        if q is None:
            raise ValueError("Did not found the given mod")

        shutil.copy(os.path.join(self.cache_folder, q[0]), self.mod_folder)

    def update(self):
        """Removes old versions of mods from the cache folder."""
        mods = {}
        for fname in self.files:
            # Drop extension and take chars after "_" to get the version number
            mod_name, mod_version = fname.rsplit(".", 1)[0].rsplit("_", 1)
            if mod_name not in mods:
                mods[mod_name] = []
            mods[mod_name].append((fname, parse_version(mod_version)))

        for mod_name in mods:
            # sorts in place from newest to oldest
            mods[mod_name].sort(key=lambda m: m[1], reverse=True)

            for fname, version in mods[mod_name][1:]:
                os.remove(os.path.join(self.cache_folder, fname))
