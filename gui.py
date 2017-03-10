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

class String_popup(QWidget):
    def __init__(self, name, parent):
        super().__init__()
        self.name = name
        self.setWindowTitle(name)
        layout = QGridLayout(self)
        self.textBox = QLineEdit()
        self.textBox.returnPressed.connect(self.submit)
        layout.addWidget(self.textBox)

    def submit(self):
        print(self.textBox.text())

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
        self.mod_list.currentItemChanged.connect(self.load_mod)

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
        # Get current editor text and transfer it into the currently selected pack file.
        print("Save")

    def save_as(self):
        # Get current editor text and open a dialog to name the new modpack that has the following mods.
        print("Save as")

    def load_mod(self):
        # Fill editor with currently selected modpack
        print("Load modpack " + self.selected_pack())

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
        print("Add pack")
        self.get_string_popup("Pack name")

    def add_string_pack(self):
        print("Add pack string")

    def install_pack(self):
        if not self.selected_pack():
            error("No pack selected")
            return
        print("Install pack " + self.selected_pack())

    def pack_string(self):
        print("Pack string")
        print(self.shell_exec("list"))

    # Helpers
    def selected_pack(self):
        return self.mod_list.currentItem().data(0)

    def mods_in_pack(self, nxt = ""):
        # If nxt is default argument, function is a getter, otherwise it is setter
        if nxt == "":
            # Get mods in current packs
            pass
        else:
            # Set mods to current pack
            pass

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
        self.strPopup = String_popup(name, self)
        self.strPopup.show()


if __name__ == "__main__":
    if (get_factorio_folder() == "Change this!"):
        open_file_gui(get_absolute_path("modman.conf"))
        exit(1)
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
