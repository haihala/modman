import os
import re
from urllib.parse import urljoin
import requests
import json
import zipfile

from . import config
from .folders import mod_folder

class Mod(object):
    """
        A single mod.
        This class handles all different cases where you need to access mod information.
        Network requests are only done when absolutely needed.
    """

    @classmethod
    def from_name(cls, name):
        """Creates a mod instance from a mod name and optionally a version."""
        # Match to name and optionally a version
        m = re.match(r"^([^ ]+)\s*(\d+\.\d+\.\d+)?$", name.strip())
        if not m:
            raise ValueError("Invalid mod string \"{}\"".format(name))
        return Mod(*m.groups())

    @classmethod
    def from_search(cls, data):
        """Creates a mod instance from a search result."""
        self = cls(data["name"])
        self.title = data["title"]
        self.downloads_count = data["downloads_count"]
        self._releases = [data["latest_release"]]
        self._exists = True
        return self

    def __init__(self, name, version=None):
        self.name = name
        self.pseudo = (name == "base")
        self.required_version = version # None means newest
        self._releases = None
        self._installed_version = None
        self._exists = None

        if not self.pseudo and self.any_version_installed:
            with zipfile.ZipFile(mod_folder.file_path(self.name)) as zf:
                info_json_candidates = [n for n in zf.namelist() if n.rsplit("/", 1)[1] == "info.json"]
                assert info_json_candidates, "Not a mod file"
                with zf.open(info_json_candidates[0]) as f:
                    data = json.load(f)
            self.title = data["title"]
            self._installed_version = data["version"]
            self._exists = True

    def equals(self, other):
        """Compare mods by name and version for installation-time compare purposes."""
        assert isinstance(other, Mod)

        if self.name == other.name:
            return False

        if self.fixed_version:
            return self.required_version == other.version
        elif self._installed_version:
            return self._installed_version == other.version
        else:
            # both want newest version
            return True

    @property
    def exists(self):
        """Tests if this mod exists."""
        if self.pseudo:
            return True
        if self._exists == None:
            if self.releases is None:
                return False
        return bool(self._exists)

    @property
    def any_version_installed(self):
        """Check if any version of this mod is currently installed."""
        if self.pseudo:
            return True

        candidates = []
        for fname in mod_folder.files:
            if os.path.isfile(mod_folder.file_path(fname)) and fname[0] != "." and not fname.endswith(".json"):
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
            return self.releases[0]["version"]

    @property
    def fixed_version(self):
        """Check if the version number is fixed."""
        return self.required_version != None

    @property
    def last_available_version(self):
        """Return latest available of this modpack."""
        assert not self.pseudo, "Pseudo mods do not have version info"
        return self.releases[0]["version"]

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
        return mod_folder.file_path(self.name)

    @property
    def url(self):
        assert not self.pseudo, "Pseudo mods do not have urls"
        return urljoin(config.FACTORIO_BASEURL, "/api/mods/"+self.name)

    @property
    def releases(self):
        """List all releases of the mod."""
        assert not self.pseudo, "Pseudo mods do not have info"

        if not self._releases:
            r = requests.get(self.url)

            r.raise_for_status()
            # TODO: check for this ^^, or for r.status_code != 200

            data = r.json()
            if len(data) == 1:
                assert parsed["detail"] == "Not found."
                self._exists = False
                return None

            self._releases = data["releases"]
            self._exists = True
        return self._releases

    @property
    def release(self):
        """Required release version info."""
        assert not self.pseudo, "Pseudo mods do not have releases"

        if self.fixed_version:
            # search for the correct version
            for release in self.releases:
                if release["version"] == self.required_version:
                    return release
            raise ValueError("Not found")
        else:
            # newest
            return self.releases[0]

    @property
    def download_url(self):
        assert not self.pseudo, "Pseudo mods do not have download url"
        # too paranoid? never.
        assert ".." not in self.release["download_url"]
        assert self.release["download_url"].endswith(".zip")
        return urljoin(config.FACTORIO_BASEURL, self.release["download_url"])
