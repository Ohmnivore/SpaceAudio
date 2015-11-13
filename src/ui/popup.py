from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui_base.ui_popup import Ui_Form

class Popup(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.mainwin = parent
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.hook_buttons()

    def hook_buttons(self):
        self.ui.Ok.pressed.connect(self.close)
