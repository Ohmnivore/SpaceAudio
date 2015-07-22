# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\library.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(320, 240)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(320, 240))
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 9, 302, 222))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Ok = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Ok.setObjectName("Ok")
        self.horizontalLayout.addWidget(self.Ok)
        self.Cancel = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout.addWidget(self.Cancel)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.Tree = QtWidgets.QTreeView(self.gridLayoutWidget)
        self.Tree.setObjectName("Tree")
        self.gridLayout.addWidget(self.Tree, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Manage Library"))
        self.Ok.setText(_translate("Form", "Scan into library"))
        self.Cancel.setText(_translate("Form", "Cancel"))

