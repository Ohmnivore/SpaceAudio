from PyQt5.QtCore import *
from popup_two import *

class FileMissingDialog(PopupTwo):
    def __init__(self, parent, path, remove_call, ignore_call):
        super().__init__(parent)
        self.setWindowTitle('Missing file')
        self.ui.Text.setText('The file \'' + path + '\' is missing. What next?')
        self.ui.Left.setText('Remove file from library')
        self.ui.Right.setText('Ignore')
        self.remove_call = remove_call
        self.ignore_call = ignore_call
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.hook_ui()

    def hook_ui(self):
        self.ui.Left.pressed.connect(self.remove_close)
        self.ui.Right.pressed.connect(self.ignore_close)

    def remove_close(self):
        self.close()
        self.remove_call()

    def ignore_close(self):
        self.close()
        self.ignore_call()
