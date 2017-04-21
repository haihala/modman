class Credentials(object):
    # Found by trying to create account
    USERNAME_MIN = 2
    PASSWORD_MIN = 5

    """User credentials for mod portal."""
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password

    @property
    def username(self):
        while self._username is None or len(self.username) < self.USERNAME_MIN:
            self._username = input("Username: ")
        return self._username

    @property
    def password(self):
        while self._username is None or len(self.username) < self.USERNAME_MIN:
            self._username = input("Username: ")
        return self._username
