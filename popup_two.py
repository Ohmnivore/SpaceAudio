from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui_popup_two import Ui_Form

class PopupTwo(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.mainwin = parent
        self.ui = Ui_Form()
        self.ui.setupUi(self)
