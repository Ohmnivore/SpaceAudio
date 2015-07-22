from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui_library import Ui_Form
import os
from scanner import *

class Library(QMainWindow):
    def __init__(self, db_p, db_t, db_a, db_alb, parent):
        super().__init__(parent)
        self.mainwin = parent
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.hook_buttons()
        self.db_p = db_p
        self.db_t = db_t
        self.db_a = db_a
        self.db_alb = db_alb
        self.model = None
        self.show_tree()

    def hook_buttons(self):
        self.ui.Cancel.pressed.connect(self.close)
        self.ui.Ok.pressed.connect(self.do_scan)

    def do_scan(self):
        self.db_p.set_paths(self.model.checked)
        Scanner(self.mainwin, self.model.checked, self.db_t, self.db_a, self.db_alb)
        self.close()

    def show_tree(self):
        #model = MyQDirModel(['C:'])
        self.model = MyQDirModel(self.db_p.get_paths())
        self.ui.Tree.setModel(self.model)

        self.ui.Tree.setColumnHidden(1, True)
        self.ui.Tree.setColumnHidden(2, True)
        self.ui.Tree.setColumnHidden(3, True)
        self.ui.Tree.expandToDepth(0)

# Taken from http://www.riverbankcomputing.com/pipermail/pyqt/2010-May/026739.html
class MyQDirModel(QDirModel):
    def __init__(self, init_folders=[]):
        self.checked = []
        super().__init__()
        for f in init_folders:
            self.setData(self.index(f, 0), Qt.Checked, Qt.CheckStateRole)
            #print(model.index(f).data())

    def data(self, index, role = Qt.DisplayRole):
        if index.isValid() and (index.column() == 0) and (role == Qt.CheckStateRole):
            # the item is checked only if we have stored its path
            if self.filePath(index) in self.checked:
                return Qt.Checked
            else:
                return Qt.Unchecked

        return QDirModel.data(self, index, role)

    def flags(self, index):
        if index.column() == 0: # make the first column checkable
           return QDirModel.flags(self, index) | Qt.ItemIsUserCheckable
        else:
            return QDirModel.flags(self, index)

    def setData(self, index, value, role = Qt.EditRole):
        if index.isValid() and (index.column() == 0) and role == Qt.CheckStateRole:
            # store checked paths, remove unchecked paths
            if (value == Qt.Checked):
                self.checked.append(self.filePath(index))
                return True
            else:
                self.checked.remove(self.filePath(index))
                return True

        else:
            return QDirModel.setData(self, index, value, role);
