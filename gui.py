#!python
import sys, os, platform, subprocess
from modman import *
from cache import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

qtCreatorFile = "gui.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

def error(arg):
    """Eventually graphical error message display function"""
    print(arg)

def add_pack(name):
    with open(os.path.join(get_absolute_path("modpacks"), name+".txt"), 'a') as f:
        pass

def modify_pack(name, text):
    with open(os.path.join(get_absolute_path("modpacks"), name+".txt"), "w") as f:
        f.write(text)

def get_mods_of_pack(name):
    with open(os.path.join(get_absolute_path("modpacks"), name+".txt"), "r") as f:
        return f.read()

class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Mod stuff
        self.cache = Cache(get_factorio_folder())

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
        if not self.selected_pack():
            self.save_as()
        # Get current editor text and transfer it into the currently selected pack file.
        modify_pack(self.selected_pack(), self.mod_text_edit.toPlainText())

    def save_as(self):
        # Get current editor text and open a dialog to name the new modpack that has the following mods.
        self.add_pack()
        self.save()

    def load_mod(self):
        # Fill editor with currently selected modpack
        self.mod_text_edit.setPlainText(get_mods_of_pack(self.selected_pack()))

    def mods(self):
        # Open mods folder
        self.open_folder(get_factorio_folder())

    def modpacks(self):
        # open modpacks folder
        self.open_folder(get_absolute_path("modpacks"))

    def open_cache(self):
        # open cache folder
        self.open_folder(self.cache.check_folder())

    def load_packs(self):
        self.mod_list.clear()
        for pack in self.shell_exec("list"):
            tmp = QListWidgetItem()
            tmp.setText(pack)
            self.mod_list.addItem(tmp)

    def add_pack(self):
        name = self.get_string_popup("Pack name")
        if name:
            add_pack(name)
            tmp = QListWidgetItem()
            tmp.setText(name)
            self.mod_list.addItem(tmp)
            self.mod_list.setCurrentRow(self.mod_list.count()-1)

    def add_string_pack(self):
        name = self.get_string_popup("Pack hash")
        if name:
            self.shell_exec("decompress " + name)
        self.load_packs()

    def install_pack(self):
        if not self.selected_pack():
            error("No pack selected")
            return
        self.shell_exec("install " + self.selected_pack())

    def pack_string(self):
        if not self.selected_pack():
            error("No pack selected")
            return
        b64 = str(self.shell_exec("compress " + self.selected_pack())[0])[2:-1]
        self.mod_text_edit.setPlainText("# Compressed string of " + self.selected_pack() + "\n\n" + b64)
        self.mod_list.clearSelection()
    # Helpers
    def selected_pack(self):
        return self.mod_list.currentItem().data(0)

    def open_folder(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def shell_exec(self, cmd):
        return [i.strip() for i in os.popen(get_absolute_path("modman.py") + " " + cmd).readlines()]

    def get_string_popup(self, name):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
            name+':')

        if ok:
            return str(text)

if __name__ == "__main__":
    if (get_factorio_folder() == "Change this!"):
        open_file_gui(get_absolute_path("modman.conf"))
        exit(1)
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
