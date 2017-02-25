#!/usr/bin/env python3
import os, glob, re, requests, json, urllib, sys, subprocess

# Helpers
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

def getPathSeparator():
    if sys.platform == "win32":
        return "\\"
    else:
        return "/"

def getPath(fname):
    ps = getPathSeparator()
    return ps.join([*os.path.realpath(__file__).split(ps)[:-1], fname])

def getFolder():
    f = open(getPath("modman.conf"))
    ret = [i for i in f.readlines() if i[0] != "#" and i != ""][0].strip()

    ps = getPathSeparator()
    if ret[-1] != ps:
        ret += ps
    f.close()
    return ret

def getSaves():
    saves = {}
    for fname in glob.glob(getPath("modpacks") + "/*"):
        f = open(fname)
        saves[fname.split(getPathSeparator())[-1][:-4]] = [i.strip() for i in f.readlines() if i != "" and i[0] != "#"]
        f.close()
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
def getHelp(subj):
    if subj == [] or subj == ["help"]:
        print ("""Usage: ./modman.py [action]

Actions:
    'help' <action> : If action is present, prints detailed information of the action, otherwise this help message is printed
    'list' or 'listpacks': Lists all available
    'edit' <modpack name> : Opens the specified pack in default text editor
    'install' <modpack name: Despite what is in the mod folder, downloads the newest mods into the specified folder""")
    elif subj == ["list"] or subj == ["listpacks"]:
        print("""LIST:
Lists all modpack files in modpacks by name.
If an argument is provided, ill list all mods in the specified pack or return "No such pack".""")
    elif subj == ["edit"]:
        print("""EDIT:
Takes a modpack as an argument. Opens the corresponding modpack file in modpacks/<modpack>.txt. If file doesn't exits, a default 'template' will be created and opened.""")
    elif subj == ["install"]:
        print("""INSTALL:
Takes a modpack(s) as an argument. Will delete all ".zip" files in the designated mod folder and download newes versions of the mods specified in the pack file(s).""")


# List function
def listpacks(args):
    if args == []:
        for i in getSaves():
            print(i)

    packs = getSaves()
    for pack in args:
        print(pack)
        if (pack in packs):
            for mod in packs[pack]:
                print ("\t" + mod)
        else:
            print("No such pack")

# Edit function
def edit(arg):
    ps = getPathSeparator()
    if (arg not in getSaves()):
        f = open(ps.join([getPath("modpacks") , arg+".txt"]), "w")
        f.write("""# Comments are allowed
# Mods are listed in any order by name in mods.factorio.com url
""")
        f.close()
    open_file(ps.join([getPath("modpacks") , arg+".txt"]))


# Install function
def install(args):
    modsFolder = getFolder()
    # Delete old mods
    print("Deleting mods in: " + modsFolder)
    for i in glob.glob(getFolder() + "*.zip"):
        os.remove(i)

    # Install new mods
    packs = getSaves()
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
        if r.status_code != 200:
            break
        parsed = json.loads(r.text)
        url = parsed["releases"][0]["download_url"]
        url = "https://mods.factorio.com" + url
        print("Downloading: " + url)
        download_file(url, modsFolder)


def main():
    if (getFolder() == "Change this!"):
        open_file(getPath("modman.conf"))
        return

    cmds = sys.argv[1:]
    if len(cmds) >= 2:
        cmd = cmds[0]
        if cmd == "help":
            getHelp(cmds[1:])
        elif cmd == "list" or cmd == "listpacks":
            listpacks(cmds[1:])
        elif cmd == "edit":
            edit(cmds[1])
        elif cmd == "install":
            install(cmds[1:])
        else:
            getHelp([])
    else:
        if len(cmds) == 1 and (cmds[0] == "list" or cmds[0] == "listpacks"):
            listpacks([])
        else:
            getHelp([])

if __name__ == '__main__':
    main()
