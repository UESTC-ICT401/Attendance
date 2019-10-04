# -*- coding: utf-8 -*-
# @Time    : 2019/10/04 14:08
# @Author  : zwenc
# @File    : course_add.py

from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QGridLayout, QTableWidgetItem, QCheckBox,
                             QPushButton)
from UI.ui_course_add import Ui_course_add
from PyQt5.QtCore import QDate
from datetime import datetime
from course import Course

class CourseAdd(QWidget, Ui_course_add):
    def __init__(self):
        super(CourseAdd, self).__init__()

        self.setupUi(self)
        self.init_ui()

        # 储存课程信息
        self.course = None

    def init_ui(self):
        # 借用 注册界面的css文件，懒得重新写过一个了。
        if __name__ == "__main__":
            Css_path = "css/register.css"
        else:
            Css_path = "./UI/css/register.css"

        with open(Css_path, "r") as css_file:
            self.setStyleSheet(css_file.read())

        for index in range(20):
            self.comboBox_weeks.addItem(str(index + 1) + "周")
        self.comboBox_weeks.setCurrentIndex(11)

        dt = datetime.now()
        self.dateEdit_startdate.setDate(QDate(dt.year, dt.month, dt.day))

        for time_item in [self.comboBox_time1, self.comboBox_time2, self.comboBox_time3]:
            for index in range(7):
                if index == 0:
                    time_item.addItem("")
                else:
                    time_item.addItem("第 " + str(2 * index - 1) + "--" + str(2 * index) + " 节课")

        self.comboBox_time1.setCurrentIndex(1)
        self.comboBox_time2.setCurrentIndex(2)
        self.comboBox_time3.setCurrentIndex(0)

    def button_register(self, bool):
        if self.lineEdit_course_name.text() == "":
            QMessageBox(self, "waring", "please enter course's name")
            return

        if self.lineEdit_course_id.text() == "":
            QMessageBox(self, "waring", "please enter course's id")
            return

        print("liuxin 负责编写 数据存储")

    def get_course_info(self):
        if self.course == None:
            QMessageBox(self, "waring", "Don't have any info of course !!")
            return None

        return self.course

    def clear_course_info(self):
        self.course = None

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = CourseAdd()
    ex.show()
    sys.exit(app.exec_())
