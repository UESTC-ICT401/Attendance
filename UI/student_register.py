# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 21:18
# @Author  : zwenc
# @File    : student_register.py

from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QGridLayout,QTableWidgetItem,QCheckBox,QPushButton)
from UI.ui_student_register import Ui_student_register
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5 import QtGui
from student import Student
from log_output import Mylog
from mysql_operation import *


class StudentRegister(QWidget,Ui_student_register):
    def __init__(self,log,target=None,args=None):
        super(StudentRegister, self).__init__()
        self.setupUi(self)
        self.init_layout()
        self.student = None
        self.log=log
        self.target=target
        self.args=args
        self.rev_signal=pyqtSignal(str)
        with open("./UI/css/register.css","r") as css_file:
            self.setStyleSheet(css_file.read())

    def init_layout(self):
        self.pushButton_register.setFont(QtGui.QFont('Microsoft YaHei', 20))
        self.tableWidget_class_check.setColumnCount(3)
        self.tableWidget_class_check.verticalHeader().setVisible(False)
        self.tableWidget_class_check.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_class_check.setColumnWidth(0,100)
        self.tableWidget_class_check.setColumnWidth(1,200)
        self.tableWidget_class_check.setHorizontalHeaderLabels(["选择","课程名","操作"])

        self.comboBox_permission.addItem("5")
        self.comboBox_permission.addItem("4")
        self.comboBox_permission.addItem("3")
        self.comboBox_permission.addItem("2")
        self.comboBox_permission.addItem("1")
        self.comboBox_permission.setCurrentIndex(2)

    def register(self, bool):
        student_name = self.lineEdit_student_name.text()
        student_number = self.lineEdit_student_number.text()
        student_IdCard = self.lineEdit_student_IdCard.text()
        student_permission = self.comboBox_permission.currentText()
        team = self.comboBox_team.currentText()
        course_checked = '0'
        tablewidget_len = self.tableWidget_class_check.rowCount() - 1

        for i in range(tablewidget_len):
            if self.tableWidget_class_check.cellWidget(i,0).isChecked():
                course_checked.append(i)
        args = Student(student_number,student_name,team,student_permission,student_IdCard,course_checked)
        self.log.info_out(args)
        self.register_stu_sql(args)

    def load_course_info(self, list_course):
        """
        :param list_course: ["语文","数学"]
        :return: error num
        """
        if isinstance(list_course,list) != True:
            return None

        self.tableWidget_class_check.setRowCount(len(list_course) + 1)

        for index,(course_name) in enumerate(list_course):
            checkbox_item = QCheckBox()
            course_name_item = QTableWidgetItem(course_name)
            button_delete_item = QPushButton()
            button_delete_item.setText("删除课程")
            self.tableWidget_class_check.setCellWidget(index,0,checkbox_item)
            self.tableWidget_class_check.setItem(index,1,course_name_item)
            self.tableWidget_class_check.setCellWidget(index,2,button_delete_item)

        button_add_course = QPushButton()
        button_add_course.setText("添加课程")
        self.tableWidget_class_check.setCellWidget(len(list_course),2,button_add_course)

    def load_team_info(self, list_team):
        """
        :param list_team: ["saber","archer","rider"]
        :return:
        """
        for index,(team) in enumerate(list_team):
            self.comboBox_team.addItem(team)

    def get_student_info(self):
        """
        :return: student info
        """
        if self.student == None:
            QMessageBox.warning(self, "warning", "学生信息填写不完整")
            return
        return self.student

    def connect_signal_slot(self):
        """
        connect qt signal and slot
        :return:
        """
        pass

    def read_rfid(self,rfid):
        # print(msg)
        self.lineEdit_student_IdCard.setText(rfid)

    def register_stu_sql(self,args):
        try:
            self.stu_info_operate=StuInfoOperate(args)
        except Exception as e:
            QMessageBox.information(self, "错误!", "数据库连接失败!!!", QMessageBox.Yes)
            self.log.info_out('学生注册：{}'.format(e))
            return
        msg=self.stu_info_operate.insert_stu()
        self.log.info_out('学生注册：{}'.format(msg))
        #close connect of mysql
        self.stu_info_operate.close_db()

