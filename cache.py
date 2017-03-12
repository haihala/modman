import glob, os, shutil

class Cache():
    """Cache is a folder in the modfolder. Cache is primarily used to store uninstalled mods in case user wants to re-install them."""
    def __init__(self, path):
        self.modsFolder = path

    def cache(self, modnames):
        """Stores wanted mods in the cache. Deletes old versions, only holds the newest ones."""
        fold = self.check_folder()
        for mod in modnames:
            mod_info = mod[:-4].split("_")  # List, first part is name, second part is version
            cached_mod_infos = sorted([os.path.split(i)[1][:-4].split("_") for i in glob.glob(os.path.join(fold, mod))], key=lambda i: -int("".join(i[1].split("."))))  # list of -''- sorted by version
            # ^ Truely beautiful

            # Change versions to ints for easier comparing
            mod_info[1] = int("".join(mod_info[1].split(".")))
            cached_mod_infos = [[i[0], int("".join(i[1].split("."))), i[0]+"_"+i[1]+".zip"] for i in cached_mod_infos]


            found = False
            for cached_mod_info in cached_mod_infos:
                # Check if older mod exists in cache
                if cached_mod_info[1] < mod_info[1]:
                    # cached mod is old.
                    os.remove(os.path.join(fold, cached_mod_info[2]))

                # Check if this mod is in cache
                if cached_mod_info[1] == mod_info[1]:
                    found = True
                    # delete the mod from modsFolder.
                    os.remove(os.path.join(self.modsFolder, mod))
                    break
            if not found:
                # A version of the mod needs to be added to cache
                # Add this mod to cache
                os.rename(os.path.join(self.modsFolder, mod), os.path.join(fold, mod))

    def check_folder(self):
        """Checks if cache folder exists. If it doesn't, creates one."""
        cache_path = os.path.join(self.modsFolder, "cache")

        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        return os.path.join(self.modsFolder, "cache")

    def version(self, modname, version):
        """Returns eighter True if a mod called `modname` with version `version` exists in the cache. False is returned otherwise"""
        # Get the folder content
        cache = glob.glob(os.path.join(self.check_folder(), modname+"_*"))

        mods = []
        for i in cache:
            mod = i[:-4].split("_")
            mods.append(mod)

        if len(mods) == 0:
            return False  # No such mod found

        mods.sort(key=lambda tup: -int("".join(i for i in tup[1].split("."))))  # sorts in place

        # Remove surely old versions
        for i in mods[1:]:
            os.remove(os.path.join(self.check_folder(), i))

        if mods[0][1] == version:
            return True

        # Newest cached version is old as well.
        os.remove(mods[0][0]+"_"+mods[0][1]+".zip")
        return False

    def fetch(self, modname):
        """Gets a mod from the cache and copies it to the mod folder."""
        # Get the folder content
        cache = glob.glob(os.path.join(self.check_folder(), modname+"_*"))

        mods = []
        for i in cache:
            mod = i[:-4].split("_")
            mods.append(mod)

        mods.sort(key=lambda tup: -int("".join(i for i in tup[1].split("."))))  # sorts in place

        # Remove surely old versions
        for i in mods[1:]:
            os.remove(os.path.join(self.check_folder(), "_".join(newest)+".zip"))

        newest = mods[0]
        fname = "_".join(newest)+".zip"
        print("Fetching from cache: " + fname)
        shutil.copy(os.path.join(self.check_folder(), fname), self.modsFolder)

if __name__ == '__main__':
    c = Cache("C:\\Users\\revol\\AppData\\Roaming\\Factorio\\mods")
    print(c.check_folder())
