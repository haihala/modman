# modman
Factorio command line mod manager.

## Usage:
After installation, run eihter "gui.py" or "modman.py", where the latter is a text based user interface that will tell you what to do. Gui tutorial is below. Gui can be started by double clicking gui.py after python3 and requests have been installed.

## Installation:

### Dependencies:
* Python3
    * Install from https://www.python.org/downloads/
* Python3 requests
    * After installing python3:
        * "pip3 install requests" in terminal/cmd

#### for gui
* Python3 PyQt5
    * After installing python3:
        * "pip3 install PyQt5" in terminal/cmd

After you downloaded the repository and installed the dependencies, you only need to specify your mod folder location. If you try to run the script, it will open the config file in your default editor. you need to replace "Change this!" with the location of your factorio mod folder. Once this is done, re-run the script and it will tell you how it works

## Modpack format.

The modpack files stored in the modpack folder are all normal .txt files. The parser ignores empty lines and lines beginning with "#" (comments). All non-comment non-empty lines are interpreted as mod names.

Mod names come from the mod portal. If you for example want to include a mod called Foo made by bar, the mod portal url should be: https://mods.factorio.com/mods/bar/Foo and you should add "Foo" to the modpack file.

There should only be one mod per line and the mod names are case specific.

## GUI tutorial

When one opens the gui, one can see two fields, two buttons and a top bar with a few buttons. Here I will go through what everything does, so every user can learn to use the tool.

### Mod list:
The list on the left. Lists the modpacks curretly installed in the modpacks folder.

### Mod content:
The text field on the right. If a mod is clicked from the mod list, the contents of the mod can be seen in the mod content text field.

### Top bar
#### File
##### Save
Save writes the text from the mod content view into the mod file in the modpacks folder.

##### Save as
Asks for a name and saves the mod content text into the corresponding pack. If pack doesn't exist, it is created.

##### Open folder
Open the mods/modpacks/cache folders in windows explorer or equivalent. Useful for manual mod insertion for example.

##### Refresh
Re-loads modpack files from the modpacks folder.

#### Packs
##### Add pack
###### Empty
Behavior is identical to the "Add a pack" button below mod list

###### From string
Decompress a pack compressed with "get as string". Useful for sharing packs.

##### Install
Behavior is identical to the "Install" button below mod list

##### get as string
Formes a hash of currently selected pack and changes the text in mod content box to show the user this hash.

## Notes
You can freely copy modpack files around, they are just lines of text with mod names.

You can add your own mod files and modify the current ones freely.

Installing a pack deletes or caches all .zip files in your mod folder. This is good to know if you store something in there. This also makes it so, re-installing a pack updates all the mods.

If you want, you can freely reach me on reddit /u/hajhawa. I will gladly respond to any tech problems you might have (I'm sure there will be plenty).
