import base64

from .mod import Mod
from .folders import modpack_folder
from .mod_cache import *
from .config import MODPACK_INHERITANCE_PREFIX

MODPACK_TEMPLATE = "# Comments are allowed\n# Mods are listed in any order by name in mods.factorio.com url\n\n"

class ModPack(object):
    """A mod pack. Lazily loads contents when required."""

    @staticmethod
    def clean_name(name):
        """Sanitize string to be used with modpack name."""
        FORBIDDEN_CHARS = list("./\\# \t\n")
        return "".join(["_" if c in FORBIDDEN_CHARS else c for c in name])

    @classmethod
    def from_filename(cls, manager, filename):
        """Create a ModPack object from filename."""
        return cls(manager, os.path.basename(filename).rsplit(".", 1)[0])

    def __init__(self, manager, name):
        self.manager = manager
        self.name = ModPack.clean_name(name)
        self._lines = None

    @property
    def exists(self):
        """Checks if the modpack is saved on disk."""
        return self.name+".txt" in os.listdir("modpacks")

    @property
    def lines(self):
        """All lines in the modpack file."""
        if self._lines is None:
            self._load()
        return self._lines

    @property
    def contents(self):
        """List of modpacks in this package."""
        mods = []
        for line in self.lines:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            if line.startswith(MODPACK_INHERITANCE_PREFIX):
                submodpack_name = line.rsplit(MODPACK_INHERITANCE_PREFIX, 1)[1]
                submodpack = ModPack(self.manager, submodpack_name)
                mods.extend(submodpack.contents)
                continue
            try:
                mods.append(Mod.from_name(self.manager, line))
            except ValueError:
                # incorrect line, ignored
                # TODO: Should we show an error message?
                continue
            # TODO: Should we remove duplicates? If there are different versions of the same mod, which one should we keep?
        return mods

    @property
    def empty(self):
        """Checks if this modpack doesn't contain any mods."""
        return self.contents == []

    @property
    def path(self):
        """Path for the modpack file."""
        return modpack_folder.file_path(self.name+".txt")

    def _load(self):
        if self.exists:
            with open(self.path) as f:
                self._lines = [line.strip() for line in f.readlines()]
        else:
            self._lines = MODPACK_TEMPLATE.split("\n")

    def edit(self, lines):
        """Changes lines of this modpack. NOTE: Does not save to disk."""
        self._lines = lines

    def save(self):
        """Saves contents of this modpack to disk."""
        # This must be before open call, so file gets created with template
        data = "\n".join(self.lines)
        with open(self.path, "w") as f:
            f.write(data)

    def compress(self):
        """Compresses this modpack to a base64 string."""
        data = "\n".join([self.name] + self.lines)
        return base64.b64encode(data.encode()).decode()

    @classmethod
    def decompress(cls, manager, data):
        """Creates a new instance fron base64 string created by compress."""
        info = base64.b64decode(data.encode()).decode()
        name, contents = info.split("\n", 1)
        self = cls(manager, name)
        self._lines = contents.split("\n")
        return self

    def __str__(self):
        return "ModPack({})".format(self.name)
