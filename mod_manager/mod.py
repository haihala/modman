import os
import re
from urllib.parse import urljoin
import requests

from . import config, factorio_folder

class Mod(object):
    @classmethod
    def from_search(self, search_result):
        self = cls(data["name"])
        self.title = data["title"]
        self.downloads = data["downloads_count"]
        self._info = {"releases": [data["latest_release"]]}
        return self

    def __init__(self, name, version=None):
        self.name = name
        self.pseudo = (name == "base")
        self.required_version = version # None means newest
        self._info = None

    @property
    def exists(self):
        """Tests if this mod exists."""
        if self.pseudo:
            return True
        return bool(self.info)

    @property
    def installed(self):
        """Test if this mod is currently installed."""
        if self.pseudo:
            return True

        files = [fname.rsplit(".", 1) for fname in os.listdir(factorio_folder.get()) if fname.endswith(".zip")]
        name_version_regex = re.compile(r"^" + re.escape(self.name) + r"_\d+\.\d+\.\d+$")
        candidates = [fname.rsplit("_", 1) for fname in files if name_version_regex.match(self.name)]
        if not candidates:
            return False

        print(candidates)
        exit()

    @property
    def version(self):
        """Return current version of this modpack."""
        assert not self.pseudo, "Pseudo mods do not have version info"

        if self.required_version is None:
            return self.info["releases"][0]["version"] + " (floating)"
        else:
            return self.required_version + " (fixed)"

    @property
    def last_available_version(self):
        """Return latest available of this modpack."""
        assert not self.pseudo, "Pseudo mods do not have version info"
        return self.info["releases"][0]["version"]

    @property
    def can_be_updated(self):
        """Checks if this mod can be updated to a newer version."""
        return self.version == self.last_available_version

    @property
    def url(self):
        assert not self.pseudo, "Pseudo mods do not have urls"
        return urljoin(config.FACTORIO_BASEURL, "/api/mods/"+self.name)

    @property
    def info(self):
        assert not self.pseudo, "Pseudo mods do not have info"

        r = requests.get(self.url)

        r.raise_for_status()
        # TODO: check for this ^^, or for r.status_code != 200

        data = r.json()
        if len(data) == 1:
            assert parsed["detail"] == "Not found."

        self._info = data
        return self._info

    @property
    def release(self):
        """Required release version info."""
        assert not self.pseudo, "Pseudo mods do not have releases"

        if self.required_version is None:
            # newest
            return self.info["releases"][0]
        else:
            # search for the correct version
            for release in self.info["releases"]:
                if release["version"] == self.required_version:
                    return release
            raise ValueError("Not found")

    @property
    def download_url(self):
        assert not self.pseudo, "Pseudo mods do not have download url"
        assert ".." not in self.release["download_url"] # too paranoid? never.
        return urljoin(config.FACTORIO_BASEURL, self.release["download_url"])
