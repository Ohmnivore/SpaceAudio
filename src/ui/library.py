from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui_base.ui_library import Ui_LibForm
import os

class Library(QDialog):
    def __init__(self, db_p, db_t, db_a, db_alb, parent):
        super().__init__(parent)
        self.mainwin = parent
        self.ui = Ui_LibForm()
        self.ui.setupUi(self)
        self.hook_buttons()
        self.db_p = db_p
        self.db_alb = db_alb

        self.model = None
        self.show_tree()
        self.ui.Tree.header().hide()

    def hook_buttons(self):
        self.ui.Cancel.pressed.connect(self.close)
        self.ui.Ok.pressed.connect(self.do_scan)

    def do_scan(self):
        self.db_p.set_paths(self.model.checked)
        self.close()
        self.mainwin.scanner.scan(self.model.checked)

    def show_tree(self):
        self.model = MyQDirModel(self.ui.Tree, self.db_p.get_paths())
        self.ui.Tree.setModel(self.model)
        self.ui.Tree.setItemDelegate(MyDelegate())

        self.ui.Tree.setColumnHidden(1, True)
        self.ui.Tree.setColumnHidden(2, True)
        self.ui.Tree.setColumnHidden(3, True)
        self.ui.Tree.expandToDepth(0)

class MyDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    def paint(self, painter, option, index):
        painter.save()

        # set background color
        is_checked = index.data(Qt.CheckStateRole)
        is_parent = index.data(16)
        is_child = index.data(17)
        painter.setPen(QPen(Qt.NoPen))
        if not (option.state & QStyle.State_Selected):
            painter.setBrush(QBrush(Qt.white))
        if is_checked:
            painter.setBrush(QBrush(QColor(236, 180, 71)))
        if is_parent:
            painter.setBrush(QBrush(QColor(89, 145, 170)))
        if is_child:
            painter.setBrush(QBrush(QColor(117, 192, 149)))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(QColor(204, 88, 63)))
        painter.drawRect(option.rect)

        # draw checkboxes
        if not is_child:
            check_box_style_option = QStyleOptionButton()
            check_box_style_option.state |= QStyle.State_Enabled
            if is_checked:
                check_box_style_option.state |= QStyle.State_On
            else:
                check_box_style_option.state |= QStyle.State_Off
            check_box_style_option.rect = QRect(option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height())
            QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)
            option.rect.setX(option.rect.x() + 16)

        # set text color
        painter.setPen(QPen(Qt.black))
        value = index.data(Qt.DisplayRole)
        text = value
        painter.drawText(option.rect, Qt.AlignLeft, text)

        painter.restore()

# Taken from http://www.riverbankcomputing.com/pipermail/pyqt/2010-May/026739.html
class MyQDirModel(QDirModel):
    def __init__(self, tree, init_folders=[]):
        self.init_folders = init_folders
        self.tree = tree
        self.checked = []
        self.parents = []
        self.children = []
        super().__init__()
        self.setFilter(QDir.Drives | QDir.NoDotAndDotDot | QDir.Readable | QDir.Dirs)
        for f in init_folders:
            index = self.index(f, 0)
            self.setData(index, Qt.Checked, Qt.CheckStateRole)

    def highlightParent(self, index):
        par = index.parent()
        while par.isValid():
            self.setData(par, QVariant(True), 16)
            par = par.parent()
    def unHighlightParent(self, index):
        par = index.parent()
        while par.isValid():
            self.setData(par, QVariant(False), 16)
            par = par.parent()

    def highlightChildren(self, index):
        i = 0
        child = index.child(i, 0)
        while child.isValid():
            self.setData(child, QVariant(True), 17)
            self.highlightChildren(child)
            i += 1
            child = index.child(i, 0)
    def unHighlightChildren(self, index):
        i = 0
        child = index.child(i, 0)
        while child.isValid():
            self.setData(child, QVariant(False), 17)
            self.unHighlightChildren(child)
            i += 1
            child = index.child(i, 0)

    def data(self, index, role = Qt.DisplayRole):
        if index.isValid() and (index.column() == 0) and (role == Qt.CheckStateRole):
            # the item is checked only if we have stored its path
            if self.filePath(index) in self.checked:
                return Qt.Checked
            else:
                return Qt.Unchecked
        if index.isValid() and role == 16:
            return index in self.parents
        if index.isValid() and role == 17:
            return index in self.children

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
                self.highlightParent(index)
                self.highlightChildren(index)
                return True
            else:
                path = self.filePath(index)
                self.checked.remove(path)
                self.unHighlightParent(index)
                self.unHighlightChildren(index)
                return True
            self.tree.viewport().update()
            self.tree.viewport().repaint()
            self.tree.verticalScrollBar().setValue(0)
        if index.isValid() and role == 16:
            if (value == True):
                self.parents.append(index)
            else:
                self.parents.remove(index)
        if index.isValid() and role == 17:
            if (value == True):
                self.children.append(index)
            else:
                self.children.remove(index)

        else:
            return QDirModel.setData(self, index, value, role);
