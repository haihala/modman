from urllib.parse import urljoin
import os.path

try:
    import requests
except ImportError:
    print("It looks like requests is not installed.")
    print("Try this: pip3 install requests")
    exit(1)


FACTORIO_BASEURL = "https://mods.factorio.com/"

def download_file(url, path):
    r = requests.get(url, stream=True, headers={"User-Agent": "factorio"})
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
        return urljoin(FACTORIO_BASEURL, "/api/mods/"+self.name)

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

    def download_to(self, mod_folder):
        if self.pseudo:
            return

        assert self.exists
        url = urljoin(FACTORIO_BASEURL, self.release["download_url"])
        assert ".." not in url # too paranoid? never.
        download_file(url, os.path.join(mod_folder, url.rsplit("/", 1)[1]))

class SearchResult(object):
    def __init__(self, data):
        self.name = data["name"]
        self.title = data["title"]
        self.downloads = data["downloads_count"]
        self.download_url = data["latest_release"]["download_url"]

def search(query, order="updated", n=5):
    assert n > 0 and n <= 25

    # https://mods.factorio.com/api/mods?q=farl&tags=&order=updated&page_size=25&page=1
    r = requests.get(urljoin(FACTORIO_BASEURL, "/api/mods"), {
        "q": query,
        "order": order,
        "page": 1,
        "page_size": n
    })


    return [SearchResult(result) for result in r.json()["results"]]
