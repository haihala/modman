#!/usr/bin/env.exe python
import os, glob, re, json, urllib, sys, subprocess, base64

if sys.version_info[0] != 3:
    print("This program requires Python 3.")
    print("You can get it from https://www.python.org/downloads/")
    exit(1)

try:
    import requests
except ImportError:
    print("It looks like requests is not installed.")
    print("Try this: pip3 install requests")
    exit(1)

# Helpers
def open_file_gui(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def get_absolute_path(fname):
    return os.path.join(os.path.split(os.path.realpath(__file__))[0], fname)

def get_factorio_folder():
    with open(get_absolute_path("modman.conf")) as f:
        ret = [i for i in f.readlines() if i[0] != "#" and i != ""][0].strip()

        if not ret.endswith(os.sep):
            ret += os.sep

    if not os.path.isdir(ret):
        print("Could not find your factorio directory!")
        print("Remember to set it on modman.conf")
        exit(1)

    return ret

def get_saves():
    saves = {}
    for fname in glob.glob(get_absolute_path("modpacks") + "/*"):
        with open(fname) as f:
            saves[os.path.split(fname)[-1][:-4]] = [i.strip() for i in f.readlines() if i != "" and i[0] != "#"]
    return saves

def download_file(url, folder):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(folder + local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


# Help function
def get_help(subj):
    if subj == [] or subj == ["help"]:
        print ("""Usage: ./modman.py [action]

Actions:
    'help' <action> : If action is present, prints detailed information of the action, otherwise this help message is printed
    'list' or 'listpacks': Lists all available
    'edit' <modpack name> : Opens the specified pack in default text editor
    'compress' <modpack name> : Makes a base64 hash of the mentioned modpack
    'decompress' <base64 modpack provided by compress> : Unpacks the base64 modpack into modpack folder. It now works like the rest of them. Warning: Overrides existing modpacks with the same name.
    'install' <modpack name>: Despite what is in the mod folder, downloads the newest mods into the specified folder""")
    elif subj == ["list"] or subj == ["listpacks"]:
        print("""LIST:
Lists all modpack files in modpacks by name.
If an argument is provided, ill list all mods in the specified pack or return "No such pack".""")
    elif subj == ["edit"]:
        print("""EDIT:
Takes a modpack as an argument. Opens the corresponding modpack file in modpacks/<modpack>.txt. If file doesn't exits, a default 'template' will be created and opened.""")
    elif subj == ["compress"]:
        print("""COMPRESS:
Takes a modpack(s) as an argument. Will provide the user with a base64 representation of the modpack. This base64 can be used to decompress it to a real modpack.""")
    elif subj == ["decompress"]:
        print("""DECOMPRESS:
Takes a base64 modpack representation as an argument. Will unpack the modpack and save it into the modpack folder. If a pack with the same name exists, will override it.""")
    elif subj == ["install"]:
        print("""INSTALL:
Takes a modpack(s) as an argument. Will delete all ".zip" files in the designated mod folder and download newes versions of the mods specified in the pack file(s).""")


# List function
def listpacks(args):
    if args == []:
        for i in get_saves():
            print(i)

    packs = get_saves()
    for pack in args:
        print(pack)
        if (pack in packs):
            for mod in packs[pack]:
                print ("\t" + mod)
        else:
            print("No such pack")

# Edit function
def edit(arg):
    if (arg not in get_saves()):
        with open(os.path.join(get_absolute_path("modpacks"), arg+".txt"), "w") as f:
            f.write("# Comments are allowed\n# Mods are listed in any order by name in mods.factorio.com url")
    open_file_gui(os.path.join(get_absolute_path("modpacks") , arg+".txt"))

# Compression function
def compress(name):
    for fname in glob.glob(get_absolute_path("modpacks") + "/*"):
        pack = os.path.split(fname)[-1][:-4]
        if pack == name:
            with open(fname, "rb") as f:
                print(base64.b64encode(bytes(pack, "UTF-8")+bytes('\n', "UTF-8")+f.read()))
            break
    else:
        print("No such pack: " + name)

def decompress(base64name):
    bt = str(base64.b64decode(base64name))
    name = str(bt.split("\\n")[0])[2:]
    content = str("\n".join(bt.split("\\n")[1:]))[:-1]
    with open(os.path.join(get_absolute_path("modpacks"), name+".txt"), "w"):
        f.write(content)
    print("Succesfully wrote to modpack " + name)

# Install function
def install(args):
    modsFolder = get_factorio_folder()
    # Delete old mods
    print("Deleting mods in: " + modsFolder)
    for i in glob.glob(modsFolder + "*.zip"):
        os.remove(i)

    # Install new mods
    packs = get_saves()
    installs = set()
    for pack in args:
        if (pack in packs):
            for mod in packs[pack]:
                installs.add(mod)
        else:
            print("No such pack: " + pack)

    print("Preparing to install: ", end='')
    print(installs)

    for i in installs:
        r = requests.get("https://mods.factorio.com/api/mods/" + i)
        parsed = json.loads(r.text)
        if len(parsed.keys()) == 1:
            if parsed["detail"] == "Not found.":
                print("Mod '" + i + "' could not be found.")
                continue
        url = parsed["releases"][0]["download_url"]
        url = "https://mods.factorio.com" + url
        print("Downloading: " + url)
        download_file(url, modsFolder)


def main():
    if (get_factorio_folder() == "Change this!"):
        open_file_gui(get_absolute_path("modman.conf"))
        return

    cmds = sys.argv[1:]
    if len(cmds) >= 2:
        cmd = cmds[0]
        if cmd == "help":
            get_help(cmds[1:])
        elif cmd == "list" or cmd == "listpacks":
            listpacks(cmds[1:])
        elif cmd == "edit":
            edit(cmds[1])
        elif cmd == "compress":
            compress(cmds[1])
        elif cmd == "decompress":
            decompress(cmds[1])
        elif cmd == "install":
            install(cmds[1:])
        else:
            get_help([])
    else:
        if len(cmds) == 1 and (cmds[0] == "list" or cmds[0] == "listpacks"):
            listpacks([])
        else:
            get_help([])

if __name__ == '__main__':
    main()
