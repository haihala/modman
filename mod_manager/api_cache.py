import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import sqlite3
import time
import json

from .config import FACTORIO_BASEURL, API_CACHE_SECONDS
from .folders import api_cache_folder
from .exceptions import AuthenticationError, LoginError, ReLoginError

class ApiCache(object):
    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False
        self.credentials = None

        self.db = sqlite3.connect(api_cache_folder.file_path("api_cache.db"))

        # create required table
        self.db.execute("CREATE TABLE IF NOT EXISTS json_request_cache (path TEXT PRIMARY KEY, result TEXT, expires INTEGER)")

    def get_csrf_token(self):
        r = self.session.get(urljoin(FACTORIO_BASEURL, "/login"))
        soup = BeautifulSoup(r.text, "lxml")
        return soup.find("input", {"name": "csrf-token"})["value"]

    def login(self, credentials):
        self.credentials = credentials
        r = self.session.post(
            "https://auth.factorio.com/login/process",
            {
                "username": credentials.username,
                "password": credentials.password,
                "redirect": "https://mods.factorio.com/receive-login",
                "service": "test_service",
                "csrf-token": self.get_csrf_token()
            },
            headers={"Referer": "https://www.factorio.com/login"}
        )

        if "Invalid username or password" not in r.text:
            raise LoginError()

        self.logged_in = True
        return self.logged_in

    def reset(self):
        self.db.execute("DELETE FROM json_request_cache")

    def update(self):
        """Removes expired elements from cache."""
        self.db.execute("DELETE FROM json_request_cache WHERE datetime(expires, \"unixepoch\") < datetime(\"now\")")
        self.db.commit()

    def store(self, path, result):
        self.update()
        if API_CACHE_SECONDS:
            self.db.execute("INSERT INTO json_request_cache VALUES (?, ?, ?)", (path, result, int(time.time()+API_CACHE_SECONDS)))
            self.db.commit()

    def fetch(self, path):
        cur = self.db.execute("SELECT result FROM json_request_cache WHERE path=? AND datetime(expires, \"unixepoch\") >= datetime(\"now\")", (path,))
        res = cur.fetchone()
        return res[0] if res else None

    def get(self, url, *args, **kwargs):
        url = urljoin(FACTORIO_BASEURL, url)
        return self.session.get(url, *args, **kwargs)

    def api_get(self, url, *args, **kwargs):
        """Gets an object from factorio mod api."""
        url = urljoin(FACTORIO_BASEURL, url)
        assert url.startswith(urljoin(FACTORIO_BASEURL, "/api")), "Only factorio mods api can be used with this"
        qparams = ""
        if "params" in kwargs:
            qparams = "&".join(key + "=" + str(kwargs["params"][key]) for key in sorted(kwargs["params"].keys()))

        cache_key = urlparse(url).path + "?" + qparams

        res = self.fetch(cache_key)
        if res:
            return json.loads(res)

        data = self.get(url, *args, **kwargs).text
        self.store(cache_key, data)
        return json.loads(data)

    def get_zip(self, url, allow_relogin=True):
        assert self.logged_in, "You must log in first"
        r = self.session.get(url, stream=True)

        if r.headers["Content-Type"].strip().startswith("text/html"):
            # Failed, property our session has expired

            if allow_relogin:
                ok = self.login(self.credentials)
                if not ok:
                    raise ReLoginError()
                return self.get_zip(url, allow_relogin=False)
            raise AuthenticationError()
        return r
