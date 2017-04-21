from .config import FACTORIO_BASEURL
from getpass import getpass

class Credentials(object):
    """User credentials for mod portal. Prompts for credentials only when needed."""

    # Found by trying to create account
    USERNAME_MIN = 2
    PASSWORD_MIN = 5

    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password

    @property
    def username(self):
        if self._username is None:
            self.prompt()
        return self._username

    @property
    def password(self):
        if self._password is None:
            self.prompt()
        return self._password

    def prompt(self):
        print("\n")
        print("#"*80)
        print("Logging in to {}:".format(FACTORIO_BASEURL))
        while self._username is None or len(self.username) < self.USERNAME_MIN:
            self._username = input("Username: ")
        while self._password is None or len(self.password) < self.PASSWORD_MIN:
            self._password = getpass("Password: ")
