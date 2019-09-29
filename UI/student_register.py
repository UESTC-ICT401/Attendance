# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 21:18
# @Author  : zwenc
# @File    : student_register.py

from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QGridLayout,QTableWidgetItem,QCheckBox,QPushButton)
from UI.ui_student_register import Ui_student_register
from student import Student
from PyQt5 import QtGui
from log_output import Mylog

log = Mylog("log/student_register.txt")

class student_register(QWidget,Ui_student_register):
    def __init__(self):
        super(student_register, self).__init__()
        self.setupUi(self)
        self.init_layout()
        self.student = None

        with open("./css/register.css","r") as css_file:
            self.setStyleSheet(css_file.read())

    def init_layout(self):
        # self.pushButton_register.setStyleSheet("QPushButton{color:rgb(0,0,0)}" #按键前景色
        #                          "QPushButton{background-color:rgb(126, 255, 126)}"  #按键背景色
        #                          "QPushButton:hover{background-color:rgb(196, 255, 223)}" #光标移动到上面后的前景色
        #                          "QPushButton{border-radius:6px}"  #圆角半径
        #                          "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}" #按下时的样式
        # )
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
        comboBox_permission = 5 - self.comboBox_permission.currentIndex()
        team = self.comboBox_team.currentText()

        course_checked = []
        tablewidget_len = self.tableWidget_class_check.rowCount() - 1

        for i in range(tablewidget_len):
            if self.tableWidget_class_check.cellWidget(i,0).isChecked():
                course_checked.append(i)


        self.student = Student(student_number,student_name,team,student_IdCard,comboBox_permission,course_checked)
        log.info_out(self.student)

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
            QMessageBox.warning(self, "waring", "学生信息填写不完整")
            return

        return self.student
