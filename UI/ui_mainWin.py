# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainWin.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(705, 427)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("picture/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_widget = QtWidgets.QGridLayout()
        self.gridLayout_widget.setHorizontalSpacing(0)
        self.gridLayout_widget.setObjectName("gridLayout_widget")
        self.horizontalLayout.addLayout(self.gridLayout_widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 705, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.actionregister = QtWidgets.QAction(MainWindow)
        self.actionregister.setObjectName("actionregister")
        self.actionCOM = QtWidgets.QAction(MainWindow)
        self.actionCOM.setObjectName("actionCOM")
        self.menu.addAction(self.actionregister)
        self.menu.addAction(self.actionCOM)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.menu_2.setTitle(_translate("MainWindow", "帮助"))
        self.actionregister.setText(_translate("MainWindow", "register"))
        self.actionCOM.setText(_translate("MainWindow", "COM"))

