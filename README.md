# modman
A Factorio mod manager.

## Usage

Before use, install dependencies. See Installation for more information.

For graphical application, double click `gui.py` file. Help on how to use the tool can be found in this document.

For command line tool, run `cli.py`. This will print the help message, describing everything you can do.

## Installation

Install everything the program is dependent on. After installing dependencies, you should be able to run everything. Installer coming soon™.

### Dependencies

#### Both CLI and GUI

* Python3
    * Install from https://www.python.org/downloads/
* Python3 requests
    * After installing python3:
        * Run `pip3 install requests` in terminal/cmd

#### For the GUI

* Python3 PyQt5
    * After installing python3:
        * Run `pip3 install PyQt5` in terminal/cmd

## Modpack format

The modpack files stored in the modpack folder are all normal .txt files. The parser ignores empty lines and lines beginning with "#" (comments). All non-comment non-empty lines are interpreted as mod names.

Mod names come from the mod portal. If you for example want to include a mod called Foo made by bar, the mod portal url should be: https://mods.factorio.com/mods/bar/Foo and you should add "Foo" to the modpack file.

There should only be one mod per line and the mod names are case specific.

## GUI tutorial

When one opens the GUI, one can see two fields, two buttons and a top bar with a few more buttons. More pictures coming later.

![Image of GUI](http://i.imgur.com/SjUg1P2.png)

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
Behavior is identical to the "Install" button below mod list.

##### Get as string
Forms a hash of currently selected pack and changes the text in mod content box to show the user this hash.

## Notes
You can freely copy modpack files around, they are just lines of text with mod names.

You can add your own mod files and modify the current ones freely.

Installing a pack deletes or caches all .zip files in your mod folder. This is good to know if you store something in there. This also makes it so, re-installing a pack updates all the mods.

If you want, you can freely reach me on reddit /u/hajhawa. I will gladly respond to any tech problems you might have (I'm sure there will be plenty). Alternatively, you could [open an issue on GitHub](https://github.com/haihala/modman/issues/new).

## Development

### Tests
You can run automated tests by `python3 -m pytest`.
You need pytest for this. It can be installed by `python3 -m pip install pytest`.
