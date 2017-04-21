from .config import APP_NAME, FACTORIO_BASEURL
from getpass import getuser, getpass

import keyring

class Keyring(object):
    """
        Manages OS credetial storage.
        This is a bit hacky, because we don't want to store usernames separately.
        Fields:
        * username: system username from getpass
        * password: newline-separated username-password pair
    """
    @staticmethod
    def keyring_name():
        return keyring.get_keyring().name

    @staticmethod
    def clear():
        try:
            keyring.delete_password(APP_NAME, getuser())
        except keyring.errors.PasswordDeleteError:
            # Password did not exist, or we have no rights to access it
            # We can just silently ignore this
            pass

    @property
    @staticmethod
    def credentials_stored():
        return Keyring.get_credentials() != None

    @staticmethod
    def get_credentials():
        pair = keyring.get_password(APP_NAME, getuser())
        if pair is None:
            return None
        assert "\n" in pair
        return Credentials(*pair.split("\n", 1))

    @staticmethod
    def set_credentials(cred):
        assert isinstance(cred, Credentials)
        return keyring.set_password(APP_NAME, getuser(), "\n".join([cred.username, cred.password]))

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

    @property
    def ok(self):
        un = self._username and len(self._username) >= self.USERNAME_MIN
        pw = self._password and len(self._password) >= self.PASSWORD_MIN
        return un and pw

    def prompt(self):
        print("")
        print("Logging in to {}:".format(FACTORIO_BASEURL))
        print("Password will not be displayed.")
        while self._username is None or len(self.username) < self.USERNAME_MIN:
            self._username = input("Username: ")
        while self._password is None or len(self.password) < self.PASSWORD_MIN:
            self._password = getpass("Password: ")
        print("")
