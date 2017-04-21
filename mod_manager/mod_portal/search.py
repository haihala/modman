from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("It looks like requests is not installed.")
    print("Try this: pip3 install requests")
    exit(1)

from . import config

class SearchResult(object):
    def __init__(self, data):
        self.name = data["name"]
        self.title = data["title"]
        self.downloads = data["downloads_count"]
        self.download_url = data["latest_release"]["download_url"]

def search(query, order="updated", n=5):
    assert n > 0 and n <= 25

    # https://mods.factorio.com/api/mods?q=farl&tags=&order=updated&page_size=25&page=1
    r = requests.get(urljoin(config.FACTORIO_BASEURL, "/api/mods"), {
        "q": query,
        "order": order,
        "page": 1,
        "page_size": n
    })

    return [SearchResult(result) for result in r.json()["results"]]
