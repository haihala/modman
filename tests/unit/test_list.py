import os
import mod_manager

def test_list():
    mm = mod_manager.ModManager()

    assert [mp.name for mp in mm.modpacks] == [fname.rsplit(".",1)[0] for fname in os.listdir("modpacks")]
