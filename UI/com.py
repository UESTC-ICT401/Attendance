# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/10/2 10:52
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QGridLayout)
import sys
from UI.ui_mainWin import Ui_MainWindow
from UI.student_register import StudentRegister
from UI.ui_com import Ui_Com_Form
from log_output import Mylog
from serial_read import Serial
from mysql_operation import *



class ComWindows(QWidget,Ui_Com_Form):
    def __init__(self,target,args=None):
        super(ComWindows,self).__init__()
        self.target=target
        self.args=args
        self.setupUi(self)
        self.signal_slot_connect()

    def put_com_list(self,com_list):
        """
        input the list of com name
        :param com_list:
        :return:
        """
        for port in com_list:
            self.comboBox_com.addItem(port[0])


    def signal_slot_connect(self):
        """
        connect signals and slots of Qt
        :return: chioced combox name
        """
        self.pushButton_ok.clicked.connect(self.call_fun)

    def call_fun(self):
        self.args = str(self.comboBox_com.currentText())
        self.target(self.args)
