import os.path
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("It looks like requests is not installed.")
    print("Try this: pip3 install requests")
    exit(1)

from . import config

class Mod(object):
    def __init__(self, name, version=None):
        self.name = name
        self.pseudo = (name == "base")
        self.required_version = version # None means newest
        self._info = None

    @property
    def url(self):
        if self.pseudo:
            raise RuntimeError("Pseudo mods do not have urls")
        return urljoin(config.FACTORIO_BASEURL, "/api/mods/"+self.name)

    @property
    def info(self):
        if self.pseudo:
            raise RuntimeError("Pseudo mods do not have info")

        r = requests.get(self.url)
        r.raise_for_status()
        # TODO: check for this ^^
        data = r.json()
        if len(data) == 1:
            assert parsed["detail"] == "Not found."

        self._info = data
        return self._info

    @property
    def exists(self):
        if self.pseudo:
            return True
        return bool(self.info)

    @property
    def release(self):
        """Required release version."""
        if self.pseudo:
            raise RuntimeError("Pseudo mods do not have release")

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
        if self.pseudo:
            return None
        else:
            assert self.exists
            assert ".." not in self.release["download_url"] # too paranoid? never.
            return urljoin(config.FACTORIO_BASEURL, self.release["download_url"])
