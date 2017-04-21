import os.path
from urllib.parse import urljoin
import re
import requests

from . import factorio_folder
from .config import FACTORIO_BASEURL, FACTORIO_LOGINURL
from .mod import Mod
from .credentials import Keyring, Credentials

class ModPortal(object):
    """Handles factorio mod portal access. Logs in if required."""
    def __init__(self):
        c = Keyring.get_credentials()
        if c:
            self.credentials = c
        else:
            self.credentials = Credentials()
            self.credentials.prompt()
        self.session = requests.Session()

    def login(self, failed_request):
        """Logs in to the Factorio mod portal."""

        # TODO: use BeautifulSoup4 instead of regex parser, especially if updating this
        csrf_token = None

        for input_field in re.findall(r"<input[^>]+>", failed_request.text, re.DOTALL):
            # TODO: check for other fields
            fields = dict(re.findall(r"([a-zA-Z-]+)=\"(.+?)\"", input_field, re.DOTALL))
            if fields.get("type", None) == "hidden" and fields.get("name", None) == "csrf-token":
                csrf_token = fields.get("value", "")

        if not csrf_token:
            print("ERROR: missing csrf-token")
            print("The login page has changed, and we are unable to login.")
            print("Please report this issue to https://github.com/haihala/modman/issues")
            exit(2)

        r = self.session.post(
            FACTORIO_LOGINURL,
            {
                "username": self.credentials.username,
                "password": self.credentials.password,
                "redirect": "https://mods.factorio.com/receive-login",
                "service": "test_service",
                "csrf-token": csrf_token
            },
            headers={"Referer": failed_request.request.url}
        )

        if "Invalid username or password" in r.text:
            print("Invalid username or password")
            exit(2)
        else:
            return r

    def download(self, mod):
        mod_folder = factorio_folder.get()
        self._download_file(mod.download_url, os.path.join(mod_folder, mod.url.rsplit("/", 1)[1]))

    def _download_file(self, url, path):
        r = self.session.get(url, stream=True)
        if r.headers["Content-Type"].strip().startswith("text/html"):
            r = self.login(r)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    def search(self, query, order="updated", n=5):
        assert n > 0 and n <= 25

        # https://mods.factorio.com/api/mods?q=farl&tags=&order=updated&page_size=25&page=1
        r = self.session.get(urljoin(FACTORIO_BASEURL, "/api/mods"), params={
            "q": query,
            "order": order,
            "page": 1,
            "page_size": n
        })

        return [Mod.from_search(result) for result in r.json()["results"]]
