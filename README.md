# modman
A mod manager for [Factorio](https://www.factorio.com/).

This tool allows you to:
* Match to a mod configuration of a running server with a single command
* Manage sets of mods, called modpacks
* Enable and disable single mods
* Easily share mod configuration to other players

Hopefully this will become completely obsolete at some point as Factorio evolves, but until that this will be useful.

This is **not** an offical Factorio product, just a useful tool developed by a few Factorio-addicted players.


## Installation

Install Python 3 from https://www.python.org/downloads/.
After installing Python 3 run

```
pip3 install requests lxml bs4 keyring appdirs
```

in terminal or cmd.
If you want to use the GUI too, you must also run

```
pip3 install PyQt5
```

## Usage

Before use, install dependencies. See above for more information.

### Graphical application

For graphical application, double click `gui.py` file. If you are using GUI, you should look at **[GUI Tutorial](gui_tutorial.md)**.

### Command line tool

#### Login credentials
Run `./cli.py credentials set` to save your factorio portal login information.


#### Text editor

On Unix-like systems, including Linux and macOS, the command line text editor can be set by using `EDITOR` environment variable. Most likely you want to set this in your `~/.bashrc` with `export EDITOR=vim` (you can of course use other editors than vim, e.g. nano).


#### Usage

 Running `./cli.py help` will display a list of available commands.

## Modpack format

The modpack files stored in the modpack folder are all normal .txt files. The parser ignores empty lines and lines beginning with "#" (comments). All non-comment non-empty lines are interpreted as mod names. You can also require specific versions by adding their version number to after the mod name. These mods are not updated with other mods.

```
# Comments are allowed
# Mods are listed in any order by name in mods.factorio.com url

# Newest version of EvoGUI
EvoGUI

# Version 2.3.4 of RSO
rso-mod 2.3.4
```

Mod names come from the mod portal. If you for example want to include a mod called Foo made by bar, the mod portal url should be: https://mods.factorio.com/mods/bar/Foo and you should add "Foo" to the modpack file.

There should only be one mod per line and the mod names are case specific.

## Notes
You can freely copy modpack files around, they are just lines of text with mod names.

You can add your own mod files and modify the current ones freely.

Installing a pack deletes or caches all .zip files in your mod folder. This is good to know if you store something in there. This also makes it so, re-installing a pack updates all the mods.

If you want, you can freely reach me on reddit /u/hajhawa. I will gladly respond to any tech problems you might have (I'm sure there will be plenty). Alternatively, you could [open an issue on GitHub](https://github.com/haihala/modman/issues/new).

## Development

### Tests
You can run automated tests by `python3 -m pytest`.
You need pytest for this. It can be installed by `pip3 install pytest`.
