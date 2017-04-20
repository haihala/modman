import sys

import modman

ACTIONS = [
    "help [action]",
    "list [package]",
    "edit <packname>",
    "compress <packname>",
    "decompress <base64>",
    "install <packname>",
    "search <query>"
]

HELP = {
    "help": "If action is present, prints detailed information of the action, otherwise this help message is printed",
    "list": "Lists all installed packages",
    "edit": "Opens the specified pack in default text editor",
    "compress": "Makes a base64 digest of the mentioned modpack",
    "decompress": "Unpacks a mod from base64 digest (overrides existing modpacks with the same name)",
    "install": "Despite what is in the mod folder, downloads the newest mods into the specified folder",
    "search": "Search for mods"
}

def get_action_names():
    return [a.split()[0] for a in ACTIONS]

def cmd_help(args):
    if args == []:
        print("")
        print("Usage: ./modman.py [action] [args]")
        print("")
        maxlen = max(map(len,ACTIONS))
        for action in ACTIONS:
            print("  "+action+" "*(maxlen-len(action)+2)+HELP[action.split()[0]])
        print("")
    elif args[0] in get_action_names():
        print(args[0]+":  "+HELP[args[0].split()[0]])
    else:
        print("Invalid action \"{}\"").format(action)
        exit(1)

def cmd_list(args):
    if args == []:
        for p in modman.modpacks():
            print(p.name)
    else:
        packs = {p.name: p for p in modman.modpacks()}
        for arg in args:
            if arg in packs:
                pack = packs[arg]
                print(pack.name)
                if pack.contents == []:
                    print("  (no mods)")
                else:
                    for mod in pack.contents:
                        print(" "*2 + mod)
            else:
                print("Mod pack \"{}\" does not exist.".format(pack.name))
                exit(1)

def cmd_compress(args):
    if len(args) != 1:
        print("Invalid argument count")
        exit(1)

    mp = modman.ModPack(args[0])
    if mp.exists:
        print(mp.compress())
    else:
        print("Mod pack \"{}\" does not exist.".format(args[0]))
        exit(1)


def cmd_decompress(args):
    if len(args) != 1:
        print("Invalid argument count")
        exit(1)

    modman.ModPack.decompress(args[0]).save()

def cmd_install(args):
    if args:
        for p in args:
            mp = modman.ModPack(p)
            if mp.exists:
                mp.install()
            else:
                print("Mod pack \"{}\" does not exist.".format(p))
                exit(1)
    else:
        print("Invalid argument count")
        exit(1)

def cmd_search(args):
    results = modman.mod_portal.search(" ".join(args))

    for i,s in enumerate(results):
        print("{}. {}: {} ({} downloads)".format(i+1, s.name, s.title, s.downloads))

def run(cmd):
    if cmd == []:
        cmd = ["help"]

    if cmd[0] in get_action_names():
        try:
            # get function in this folder named "cmd_<action>"
            fn = getattr(sys.modules[__name__], "cmd_"+cmd[0])
        except AttributeError:
            print("Action not implemented yet.")
            exit(1)

        fn(cmd[1:])
    else:
        print("Invalid action \"{}\"").format(cmd[0])
        exit(1)

def main():
    run(sys.argv[1:])

if __name__ == '__main__':
    main()
