# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 21:02
# @Author  : zwenc
# @File    : mainWin.py

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QGridLayout)
import sys
from UI.ui_mainWin import Ui_MainWindow
from UI.student_register import student_register

class Windows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Windows, self).__init__()
        self.setupUi(self)
        self.student_register = student_register()
        self.student_register.load_course_info(["adsfa","asdfasdf","asdf","asdfaf","asdfasdf"])
        self.student_register.load_team_info(["saber","archer","rider"])

        self.gridLayout_widget.addWidget(self.student_register)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Windows()
    ex.show()
    sys.exit(app.exec_())