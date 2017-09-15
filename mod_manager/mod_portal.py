import os
from urllib.parse import urljoin

from .folders import mod_folder
from .mod import Mod
from .api_cache import ApiCache
from .credentials import Keyring, Credentials
from .exceptions import AuthenticationError, LoginError


class ModPortal(object):
    """Handles factorio mod portal access. Logs in if required."""
    def __init__(self, manager):
        self.manager = manager
        self.api_cache = ApiCache()

    @property
    def logged_in(self):
        return self.api_cache.logged_in

    def login(self, credentials=None):
        """Logs in to the mod portal."""
        if self.logged_in:
            return True

        if not credentials:
            keyring_credentials = Keyring.get_credentials()
            if keyring_credentials is None:
                raise AuthenticationError
            credentials = keyring_credentials

        if not credentials.ok:
            raise LoginError()
        self.api_cache.login(credentials)

    def releases(self, mod):
        """List all releases of the mod."""
        assert not mod.pseudo, "Pseudo mods do not have info"

        data = self.api_cache.api_get(mod.url)

        if len(data) == 1:
            assert data["detail"] == "Not found."
            return None

        return data["releases"]

    def download(self, mod):
        self._download_file(mod.download_url, mod_folder.file_path(mod.download_url.rsplit("/", 1)[1]))

    def _download_file(self, url, path):
        r = self.api_cache.get_zip(url)
        try:
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
        except:
            # the file is now closed, but we must clear the mod file too; it contains a broken zip file
            print("\nDownload cancelled, removing file...")
            os.remove(path)
            print("removed")
            raise

    def search(self, query, order="updated", n=5):
        assert n > 0 and n <= 25

        # https://mods.factorio.com/api/mods?q=farl&tags=&order=updated&page_size=25&page=1
        data = self.api_cache.api_get("/api/mods", params={
            "q": query,
            "order": order,
            "page": 1,
            "page_size": n
        })

        return [Mod.from_search(self.manager, result) for result in data["results"]]
