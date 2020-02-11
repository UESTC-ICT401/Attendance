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
from mysql_operation import *
from log_output import Mylog
from global_value import *

class CourseAdd(QWidget, Ui_course_add):
    _weekday_tuple_=('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
    def __init__(self,log):
        super(CourseAdd, self).__init__()
        self.log = log
        self.setupUi(self)
        self.init_ui()
        self.start_week_date =QDate.fromString(FIRST_WEEK_DATE,"yyyy-MM-dd")


    # def set_background(self):
    #
    #     palette1 = QPalette(self)
    #     palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('./UI/picture/ground.jpeg')))   # 设置背景图片
    #     self.setPalette(palette1)

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
        course_name =self.lineEdit_course_name.text()
        course_id = self.lineEdit_course_id.text()
        start_week =self.comboBox_startWeeks.currentIndex()
        start_date = self.start_week_date.addDays(start_week*7).toString("yyyy-MM-dd")
        end_week   = self.comboBox_endWeeks.currentIndex()
        end_date = self.start_week_date.addDays((end_week+1)*7-1).toString("yyyy-MM-dd")
        lesson_weekday=self._weekday_tuple_[self.comboBox_weekDate.currentIndex()]
        start_time =self.timeEdit_startTime.text()
        end_time   =self.timeEdit_endTime.text()
        course =Course(course_id=course_id,course_name=course_name,start_date=start_date,end_date=end_date,lesson_weekday=lesson_weekday,
                 start_time=start_time,end_time=end_time,effectiveness=1)
        for value in course.course_dict.values():
            if not value:
                QMessageBox.information(self, "警告!", "信息填写不完整!!!", QMessageBox.Yes)
                return
        self.register_stu_sql(course)


    def register_stu_sql(self,course):
        try:
            self.course_operate=CourseOperate()
        except Exception as e:
            QMessageBox.information(self, "错误!", "数据库连接失败!!!", QMessageBox.Yes)
            self.log.info_out('课程注册：{}'.format(e))
            return
        info,reslut=self.course_operate.insert_course(course)
        if not reslut:
            self.log.info_out('课程注册：课程插入信息{}'.format(info))
            return
        self.log.info_out('课程注册：成功')
        self.course_operate.close_db()

    def clear_course_info(self):
        self.course = None

# if __name__ == "__main__":
#     import sys
#     log=Mylog("../log/student_register.txt")
#     app = QApplication(sys.argv)
#     ex = CourseAdd(log)
#     ex.show()
#     sys.exit(app.exec_())
