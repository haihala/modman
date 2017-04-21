import os.path
from urllib.parse import urljoin

from . import config

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
    def installed(self):
        """Test if this mod is currently installed."""
        if self.pseudo:
            return True
        return bool(self.info)

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
        print("#\n")
        print(data)
        print("\n\n#")
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
