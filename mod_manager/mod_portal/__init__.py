import os.path

try:
    import requests
except ImportError:
    print("It looks like requests is not installed.")
    print("Try this: pip3 install requests")
    exit(1)

from mod_manager import factorio_folder

class ModPortal(object):
    def __init__(self):
        self.credentials = None

    def download(self, mod):
        mod_folder = factorio_folder.get()
        self._download_file(mod.url, os.path.join(mod_folder, mod.url.rsplit("/", 1)[1]))

    def _download_file(self, url, path):
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
