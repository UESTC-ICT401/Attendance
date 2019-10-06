# -*- coding: utf-8 -*-
# @Time    : 2019/10/04 14:08
# @Author  : zwenc
# @File    : course_add.py

from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QGridLayout, QTableWidgetItem, QCheckBox,
                             QPushButton)
from UI.ui_course_add import Ui_course_add
from PyQt5.QtCore import QDate, QTime
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

        # 加载样式表
        with open(Css_path, "r") as css_file:
            self.setStyleSheet(css_file.read())

        # 初始化周数
        for index in range(20):
            self.comboBox_startWeeks.addItem("第 "+str(index + 1) + " 周")
            self.comboBox_endWeeks.addItem("第 "+ str(index + 1) + " 周")
        self.comboBox_startWeeks.setCurrentIndex(0)
        self.comboBox_endWeeks.setCurrentIndex(11)

        for index in range(7):
            self.comboBox_weekDate.addItem("星期 " + str(index + 1))

        # 初始化时间
        self.timeEdit_startTime.setTime(QTime(8,30,0))
        self.timeEdit_startTime.setCalendarPopup(True)
        self.timeEdit_endTime.setTime(QTime(11,50,0))

    def button_register(self, bool):
        if self.lineEdit_course_name.text() == "":
            QMessageBox.information(self, "waring", "please enter course's name")
            return

        if self.lineEdit_course_id.text() == "":
            QMessageBox.information(self, "waring", "please enter course's id")
            return

        print("liuxin 负责编写 数据存储")

    def get_course_info(self):
        if self.course == None:
            QMessageBox.information(self, "waring", "Don't have any info of course !!")
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
