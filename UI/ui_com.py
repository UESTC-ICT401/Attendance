# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_com.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Com_Form(object):
    def setupUi(self, Com_Form):
        Com_Form.setObjectName("Com_Form")
        Com_Form.resize(267, 130)
        Com_Form.setMinimumSize(QtCore.QSize(7, 0))
        self.horizontalLayoutWidget = QtWidgets.QWidget(Com_Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 231, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_com = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboBox_com.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_com.setObjectName("comboBox_com")
        self.horizontalLayout.addWidget(self.comboBox_com)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 7)
        self.pushButton_ok = QtWidgets.QPushButton(Com_Form)
        self.pushButton_ok.setGeometry(QtCore.QRect(90, 90, 93, 28))
        self.pushButton_ok.setObjectName("pushButton_ok")

        self.retranslateUi(Com_Form)
        QtCore.QMetaObject.connectSlotsByName(Com_Form)

    def retranslateUi(self, Com_Form):
        _translate = QtCore.QCoreApplication.translate
        Com_Form.setWindowTitle(_translate("Com_Form", "Form"))
        self.label.setText(_translate("Com_Form", "COM:"))
        self.pushButton_ok.setText(_translate("Com_Form", "OK"))

