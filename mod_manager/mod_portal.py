import os.path
from urllib.parse import urljoin
import requests

from . import factorio_folder
from .mod import Mod

class ModPortal(object):
    def __init__(self):
        self.credentials = None

    def download(self, mod):
        mod_folder = factorio_folder.get()
        self._download_file(mod.url, os.path.join(mod_folder, mod.url.rsplit("/", 1)[1]))

    def _download_file(self, url, path):
        # r = requests.get(url, stream=True, headers={"User-Agent": "factorio"})
        r = requests.get(url, stream=True)
        if r.headers["Content-Type"].strip().startswith("text/html"):
            # login required
            exit("LOGIN REQUIRED")
            return False
        else:
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
            return True

    def search(query, order="updated", n=5):
        assert n > 0 and n <= 25

        # https://mods.factorio.com/api/mods?q=farl&tags=&order=updated&page_size=25&page=1
        r = requests.get(urljoin(config.FACTORIO_BASEURL, "/api/mods"), {
            "q": query,
            "order": order,
            "page": 1,
            "page_size": n
        })

        return [Mod.from_search(result) for result in r.json()["results"]]
