from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui_base.ui_info import Ui_Form

class Info(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.mainwin = parent
        self.ui = Ui_Form()
        self.ui.setupUi(self)
