# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\maya_Tools\src\developer\main\assetContent\assetbrowser\widget\ui\loginUI.ui'
#
# Created: Thu Oct 23 16:43:10 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(471, 334)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(268, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.cbbHost = QtGui.QComboBox(self.centralwidget)
        self.cbbHost.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.cbbHost.setObjectName(_fromUtf8("cbbHost"))
        self.cbbHost.addItem(_fromUtf8(""))
        self.horizontalLayout_4.addWidget(self.cbbHost)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.edtPort = QtGui.QLineEdit(self.centralwidget)
        self.edtPort.setText(_fromUtf8(""))
        self.edtPort.setObjectName(_fromUtf8("edtPort"))
        self.verticalLayout_2.addWidget(self.edtPort)
        self.edtUserName = QtGui.QLineEdit(self.centralwidget)
        self.edtUserName.setObjectName(_fromUtf8("edtUserName"))
        self.verticalLayout_2.addWidget(self.edtUserName)
        self.edtPassWord = QtGui.QLineEdit(self.centralwidget)
        self.edtPassWord.setEchoMode(QtGui.QLineEdit.Password)
        self.edtPassWord.setObjectName(_fromUtf8("edtPassWord"))
        self.verticalLayout_2.addWidget(self.edtPassWord)
        self.cbbWorkSpaces = QtGui.QComboBox(self.centralwidget)
        self.cbbWorkSpaces.setObjectName(_fromUtf8("cbbWorkSpaces"))
        self.verticalLayout_2.addWidget(self.cbbWorkSpaces)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.pushButton.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/arrow-right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(10, 10))
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_3.addWidget(self.pushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout_3.addWidget(self.textEdit)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnLogin = QtGui.QPushButton(self.centralwidget)
        self.btnLogin.setObjectName(_fromUtf8("btnLogin"))
        self.horizontalLayout_2.addWidget(self.btnLogin)
        self.btnLoginNoSC = QtGui.QPushButton(self.centralwidget)
        self.btnLoginNoSC.setObjectName(_fromUtf8("btnLoginNoSC"))
        self.horizontalLayout_2.addWidget(self.btnLoginNoSC)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Asset Login", None))
        self.cbbHost.setItemText(0, _translate("MainWindow", "Connect to", None))
        self.label_4.setText(_translate("MainWindow", "Host", None))
        self.label.setText(_translate("MainWindow", "UserName", None))
        self.label_2.setText(_translate("MainWindow", "Password", None))
        self.label_3.setText(_translate("MainWindow", "Workspaces", None))
        self.edtPort.setPlaceholderText(_translate("MainWindow", "-- Ip server --", None))
        self.edtUserName.setPlaceholderText(_translate("MainWindow", "-- username --", None))
        self.edtPassWord.setPlaceholderText(_translate("MainWindow", "-- password --", None))
        self.pushButton.setText(_translate("MainWindow", "Show more info", None))
        self.btnLogin.setText(_translate("MainWindow", "Log In", None))
        self.btnLoginNoSC.setText(_translate("MainWindow", "Log In Without SC", None))
        self.checkBox.setText(_translate("MainWindow", "Remember me", None))

import developer.main.source.IconResource_rc
