#!/usr/bin/env python3

try:
    import requests
except ImportError:
    print("It looks like requests is not installed.")
    print("Try this: pip3 install requests")
    exit(1)

import sys
import subprocess
import os.path
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import mod_manager

Ui_MainWindow, QtBaseClass = uic.loadUiType("gui.ui")

def error(arg):
    """Display an error message."""
    # TODO: show a graphical window
    print(arg)

class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Mod stuff
        self.mod_manager = mod_manager.ModManager()
        self.cache = mod_manager.cache.Cache(mod_manager.factorio_folder.get())

        # UI elements
        # Buttons
        self.add_pack_button.clicked.connect(self.add_pack)
        self.install_pack_button.clicked.connect(self.install_pack)

        # Mods list
        self.mod_list.itemClicked.connect(self.load_mod)

        # Menubar items
        # File
        self.save_button.triggered.connect(self.save)
        self.save_as_button.triggered.connect(self.save_as)
        self.refresh_button.triggered.connect(self.load_packs)

        # Folder
        self.open_mods_button.triggered.connect(self.mods)
        self.open_modpacks_button.triggered.connect(self.modpacks)
        self.open_cache_button.triggered.connect(self.open_cache)

        # Pack
        self.add_empty_pack_button.triggered.connect(self.add_pack)
        self.add_string_pack_button.triggered.connect(self.add_string_pack)
        self.install_pack_button_2.triggered.connect(self.install_pack)
        self.get_pack_string_button.triggered.connect(self.pack_string)

        # Load packs initially
        self.load_packs()

    # Actions
    def save(self):
        if not self.get_selected_pack():
            self.save_as()

        # Get current editor text and transfer it into the currently selected pack file.
        self.get_selected_pack().edit(self.mod_text_edit.toPlainText().replace("\r\n", "\n").split("\n"))
        self.get_selected_pack().save()

    def save_as(self):
        # Get current editor text and open a dialog to name the new modpack that has the following mods.
        self.add_pack()
        self.save()

    def load_mod(self):
        """Fill editor with currently selected modpack."""
        pack = self.get_selected_pack()
        if pack is None:
            # No pack selected
            return
        self.mod_text_edit.setPlainText("\n".join(pack.lines))

    def mods(self):
        """Open mods folder."""
        self.open_folder(mod_manager.factorio_folder.get())

    def modpacks(self):
        # open modpacks folder
        self.open_folder(get_absolute_path("modpacks"))

    def open_cache(self):
        # open cache folder
        self.open_folder(self.cache.check_folder())

    def load_packs(self):
        self.mod_list.clear()
        for pack in self.mod_manager.modpacks:
            tmp = QListWidgetItem()
            tmp.setText(pack.name)
            self.mod_list.addItem(tmp)
        self.mod_list.sortItems()

    def add_pack(self):
        name = self.get_string_popup("Pack name")
        if name:
            self.mod_manager.get_pack(name).save()

            tmp = QListWidgetItem()
            tmp.setText(name)
            self.mod_list.addItem(tmp)
            self.mod_list.setCurrentRow(self.mod_list.count()-1)
            self.mod_list.sortItems()
            self.load_mod()

    def add_string_pack(self):
        name = self.get_string_popup("Digest")
        if name:
            mod_manager.modpack.ModPack.decompress(args[0]).save()
        self.load_packs()

    def install_pack(self):
        pack = self.get_selected_pack()
        if pack is None:
            error("No pack selected")
            return

        self.mod_manager.install_pack(pack)

        # TODO: show progress steps
        # TODO: show message

    def pack_string(self):
        if self.get_selected_pack() is None:
            error("No pack selected")
            return
        print(self.get_selected_pack())
        self.mod_text_edit.setPlainText("# Digest string of " + self.get_selected_pack() + "\n\n" + self.get_selected_pack().compress())
        self.mod_list.clearSelection()

    def get_selected_pack(self):
        current_item = self.mod_list.currentItem()
        if current_item is None:
            return None
        return self.mod_manager.get_pack(current_item.data(0))

    # Helpers
    def open_folder(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def get_string_popup(self, name):
        text, ok = QInputDialog.getText(self, 'Input Dialog', name+':')

        if ok:
            return str(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
