import os
import re
from urllib.parse import urljoin
import requests
import json
import zipfile

from . import config, factorio_folder

class Mod(object):
    @classmethod
    def from_name(cls, name):
        # Match to name and optionally a version
        m = re.match(r"^([^ ]+)\s*(\d+\.\d+\.\d+)?$", name.strip())
        if not m:
            raise ValueError("Invalid mod string \"{}\"".format(name))
        return Mod(*m.groups())

    @classmethod
    def from_search(self, search_result):
        self = cls(data["name"])
        self._title = data["title"]
        self._downloads = data["downloads_count"]
        self._info = {"releases": [data["latest_release"]]}
        return self

    def __init__(self, name, version=None):
        self.name = name
        self.pseudo = (name == "base")
        self.required_version = version # None means newest
        self._info = None
        self._installed_version = None

        if not self.pseudo and self.any_version_installed:
            with zipfile.ZipFile(os.path.join(factorio_folder.get(), self.name)) as zf:
                info_json_candidates = [n for n in zf.namelist() if n.rsplit("/", 1)[1] == "info.json"]
                assert info_json_candidates, "Not a mod file"
                with zf.open(info_json_candidates[0]) as f:
                    data = json.load(f)
            self._title = data["title"]
            self._installed_version = data["version"]

    @property
    def exists(self):
        """Tests if this mod exists."""
        if self.pseudo:
            return True
        return bool(self.info)

    @property
    def any_version_installed(self):
        """Check if any version of this mod is currently installed."""
        if self.pseudo:
            return True

        candidates = []
        ff = factorio_folder.get()
        for fname in os.listdir(ff):
            if os.path.isfile(os.path.join(ff, fname)) and fname[0] != "." and not fname.endswith(".json"):
                candidates.append(fname)

        return self.name in candidates

    @property
    def installed(self):
        """Check if the exact version of this mod is currently installed."""
        if self.pseudo:
            return True

        return self.any_version_installed and self._installed_version == self.version

    @property
    def version(self):
        """Return current version of this modpack."""
        assert not self.pseudo, "Pseudo mods do not have version info"

        if self.fixed_version:
            return self.required_version
        elif self._installed_version:
            return self._installed_version
        else:
            return self.info["releases"][0]["version"]

    @property
    def fixed_version(self):
        """Check if the version number is fixed."""
        return self.required_version != None

    @property
    def last_available_version(self):
        """Return latest available of this modpack."""
        assert not self.pseudo, "Pseudo mods do not have version info"
        return self.info["releases"][0]["version"]

    @property
    def can_be_updated(self):
        """Checks if this mod can be updated to a newer version."""
        if self.fixed_version:
            return False
        return self.version == self.last_available_version

    @property
    def path(self):
        assert not self.pseudo, "Pseudo mods do not have path"
        assert self.installed, "Only installed mods have path"
        return os.path.join(factorio_folder.get(), self.name)

    @property
    def url(self):
        assert not self.pseudo, "Pseudo mods do not have urls"
        return urljoin(config.FACTORIO_BASEURL, "/api/mods/"+self.name)

    @property
    def info(self):
        assert not self.pseudo, "Pseudo mods do not have info"

        if not self._info:
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

        if self.fixed_version:
            # search for the correct version
            for release in self.info["releases"]:
                if release["version"] == self.required_version:
                    return release
            raise ValueError("Not found")
        else:
            # newest
            return self.info["releases"][0]

    @property
    def download_url(self):
        assert not self.pseudo, "Pseudo mods do not have download url"
        # too paranoid? never.
        assert ".." not in self.release["download_url"]
        assert self.release["download_url"].endswith(".zip")
        return urljoin(config.FACTORIO_BASEURL, self.release["download_url"])
