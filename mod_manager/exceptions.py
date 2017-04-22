class AuthenticationError(Exception):
    """Could not authenticate to use the mod portal."""

class LoginError(AuthenticationError):
    """Could not log in to the mod portal."""

class ReLoginError(AuthenticationError):
    """Could automatically again to the mod portal after session was expired."""


class InstallationError(Exception):
    """Could not install requested mod or modpack."""

class InstallationVersionConflict(InstallationError):
    """Could not install requested modpack(s), because multiple versions of a mod are required."""


class FactorioFolderNotFound(Exception):
    """Could not find factorio mod folder."""


class CorruptedZipFile(Exception):
    """Mod zip file was corrupted."""
    def __init__(self, filename):
        self.filename = filename
