import requests
import sys
import tarfile
from os.path import exists, join
from os import remove, mkdir, rename
from shutil import rmtree

# Dirty af, but this'll do for now
server_folder_name = "Modded_server"

def download_file(url):
    dirty_replacement("Downloading server... ")
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print("done")
    return local_filename

def latest_version(experimental=False):
    dirty_replacement("Fetching newest server version... ")
    r = requests.get("https://updater.factorio.com/get-available-versions", timeout=10.0)
    data = r.json()["core-linux_headless64"]

    # TODO: Experimental filter

    version = data[-1]["stable"]
    print("done, it was {}".format(version))
    return version


def create_server(modpacks, experimental, manager, callback):
    version = latest_version(experimental)

    # Suboptimal, fix later.
    # Right, totally will fix this some day.
    if exists("linux64"):
        print("Removing old tar")
        remove("linux64")

    download_file("https://www.factorio.com/get-download/{}/headless/linux64".format(version))

    if exists(server_folder_name):
        print("Removing old modded server, do you want to continue? (Y/n)", end='')
        cont = input()
        if cont.lower() in ["y", "yes", ""]:
            rmtree(server_folder_name)
            print("Old folder removed")
        else:
            print("Terminating installation")
            exit(1)

    unpack_server()
    install_server_mods(modpacks, manager, callback)

def unpack_server():
    assert exists("linux64"), "Downloaded file has vanished. ¯\_(ツ)_/¯"
    assert tarfile.is_tarfile("linux64"), "Downloaded file isn't a tarfile. ¯\_(ツ)_/¯"

    dirty_replacement("Extracting tarball... ")
    with tarfile.open("linux64") as tf:
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tf)
    rename("factorio", server_folder_name)
    print("done")

    mkdir(join(server_folder_name, "mods"))

    dirty_replacement("Removing extracted tar... ")
    remove("linux64")
    print("done")


def install_server_mods(args, mod_manager, callback):
    if args:
        packs = []
        for p in args:
            mp = mod_manager.get_pack(p)
            if mp.exists:
                packs.append(mp)
            else:
                print("Mod pack \"{}\" does not exist.".format(p))
                exit(1)

        mod_manager.install_packs(packs, callback, target=join(server_folder_name, "mods"))
    else:
        print("Invalid argument count")
        exit(1)


def dirty_replacement(message):
    print(message, end="")
    sys.stdout.flush()
