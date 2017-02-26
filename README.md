# modman
Factorio command line mod manager.

## Usage:
After installation, run the script, It will tell you what to do.

## Installation:
### Dependencies:
* Python3
    * Install from https://www.python.org/downloads/
* Python3 requests
    * After installing python3:
        * "pip3 install requests" in terminal/cmd

After you downloaded the repository and installed the dependencies, you only need to specify your mod folder location. If you try to run the script, it will open the config file in your default editor. you need to replace "Change this!" with the location of your factorio mod folder. Once this is done, re-run the script and it will tell you how it works

## Modpack format.

The modpack files stored in the modpack folder are all normal .txt files. The parser ignores empty lines and lines beginning with "#" (comments). All non-comment non-empty lines are interpreted as mod names.

Mod names come from the mod portal. If you for example want to include a mod called Foo made by bar, the mod portal url should be: https://mods.factorio.com/mods/bar/Foo and you should add "Foo" to the modpack file.

There should only be one mod per line and the mod names are case specific.


## Notes
You can freely copy modpack files around, they are just lines of text with mod names.

You can add your own mod files and modify the current ones freely.

Installing a pack deletes all .zip files in your mod folder. This is good to know if you store something in there. This also makes it so, re-installing a pack updates all the mods.

If you want, you can freely reach me on reddit /u/hajhawa. I will gladly respond to any tech problems you might have (I'm sure there will be plenty).

This script was made on linux, but it should work on all modern operating systems if the mod folder is set correctly (Haven't actually tested this, just relying on portability of python and luck).
