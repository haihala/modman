import os
import base64

import mod_manager

def test_compress():
    import time

    mm = mod_manager.ModManager()
    mp = mm.get_pack("test")
    mp.save()
    compressed = mp.compress()
    data = base64.b64decode(compressed)

    name, *lines = data.decode().split("\n")

    assert name == "test"
    assert mp.path.endswith("modpacks/test.txt")

    with open(mp.path) as f:
        assert lines == [line.strip() for line in f.readlines()]
