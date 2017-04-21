import os
import subprocess as sp
import base64


def test_crash():
    CLI_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../cli.py")

    # Test that commands don't crash crashes
    assert 0 == sp.call([CLI_FILE, "help"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    assert 0 == sp.call([CLI_FILE, "list"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    assert 0 == sp.call([CLI_FILE, "contents", "vanilla"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    assert 0 == sp.call([CLI_FILE, "contents", "vanilla+"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    data = base64.b64encode("test\n# test\nrso-mod".encode()).decode()
    assert 0 == sp.call([CLI_FILE, "decompress", data], stdout=sp.DEVNULL, stderr=sp.DEVNULL)

    # TODO: test match somehow (are there popular public servers?)
    # TODO: test install when we have credentials

    assert 0 == sp.call([CLI_FILE, "enabled"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    assert 0 == sp.call([CLI_FILE, "search", "farl"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    assert 0 == sp.call([CLI_FILE, "cache", "list"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    assert 0 == sp.call([CLI_FILE, "cache", "clear"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)

    # We don't want to clear stored credentials so we can't test that yet

    # test that invalid commands crash
    assert 0 != sp.call([CLI_FILE, "<<INVALID_COMMAND>>"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    assert 0 != sp.call([CLI_FILE, "credentials", "set", "a", "b"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
