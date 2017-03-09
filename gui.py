#!python
import sys
from PyQt5 import QtCore, QtWidgets, uic

qtCreatorFile = "gui.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Buttons
        self.add_pack_button.clicked.connect(self.add_pack)
        self.install_pack_button.clicked.connect(self.install_pack)

        # Menubar items
        # File
        self.save_button.triggered.connect(self.save)
        self.save_as_button.triggered.connect(self.save_as)
        self.refresh_button.triggered.connect(self.load_packs)

        # Folder
        self.open_mods_button.triggered.connect(self.mods)
        self.open_modpacks_button.triggered.connect(self.modpacks)
        self.open_cache_button.triggered.connect(self.cache)

        # Pack
        self.add_empty_pack_button.triggered.connect(self.add_pack)
        self.add_string_pack_button.triggered.connect(self.add_string_pack)
        self.install_pack_button_2.triggered.connect(self.install_pack)
        self.get_pack_string_button.triggered.connect(self.pack_string)

        # Load packs initially
        self.load_packs()

    def save(self):
        print("Save")

    def save_as(self):
        print("Save as")

    def mods(self):
        print("Mods")

    def modpacks(self):
        print("Modpacks")

    def cache(self):
        print("Cache")

    def load_packs(self):
        print("(re)Loading packs")

    def add_pack(self, ):
        print("Add pack")

    def add_string_pack(self):
        print("Add pack string")

    def install_pack(self):
        print("Install pack")

    def pack_string(self):
        print("Pack string")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
