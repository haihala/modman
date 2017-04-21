import sys, os.path; sys.path.insert(1, os.path.join(sys.path[0], '..'))

import mod_manager

mm = mod_manager.ModManager()

assert [mp.name for mp in mm.modpacks] == [fname.rsplit(".",1)[0] for fname in os.listdir("modpacks")]
