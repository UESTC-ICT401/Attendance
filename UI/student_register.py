# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 21:18
# @Author  : zwenc,liuxin
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
        student_ID = self.lineEdit_student_number.text()
        student_IdCard = self.lineEdit_student_IdCard.text()
        student_permission = self.comboBox_permission.currentText()
        team = self.comboBox_team.currentText()
        course_checked = []
        tablewidget_len = self.tableWidget_class_check.rowCount() - 1

        for i in range(tablewidget_len):
            if self.tableWidget_class_check.cellWidget(i,0).isChecked():
                course_checked.append(i)
        stu = Student(stuID=student_ID,
                      name=student_name,
                      team=team,
                      rfid=student_IdCard,
                      permission=student_permission,
                      registered_course=str(course_checked))
        self.log.info_out(stu)
        if not self.check_student_info(stu):#if infomation is no
            return
        self.register_stu_sql(stu,course_checked)

    def load_course_info(self):
        """
        :param list_course: ["语文","数学"]
        :return: error num
        """
        course_list=[]
        course_operate = CourseOperate()
        self.course_obj_list, result = course_operate.search_course()

        if result:
            self.log.info_out("注册：导入课程表")
            for corse_obj in self.course_obj_list:
                course_list.append(corse_obj['course_name'])
        else:
            self.log.info_out("注册：{}".format(result))
            return
        if isinstance(course_list,list) != True:
            return None

        self.tableWidget_class_check.setRowCount(len(course_list) + 1)

        for index,(course_name) in enumerate(course_list):
            checkbox_item = QCheckBox()
            course_name_item = QTableWidgetItem(course_name)
            button_delete_item = QPushButton()
            button_delete_item.setText("删除课程")
            self.tableWidget_class_check.setCellWidget(index,0,checkbox_item)
            self.tableWidget_class_check.setItem(index,1,course_name_item)
            self.tableWidget_class_check.setCellWidget(index,2,button_delete_item)

        button_add_course = QPushButton()
        button_add_course.setText("添加课程")
        self.tableWidget_class_check.setCellWidget(len(course_list),2,button_add_course)

    def load_team_info(self, list_team):
        """
        :param list_team: ["saber","archer","rider"]
        :return:
        """
        for index,(team) in enumerate(list_team):
            self.comboBox_team.addItem(team)

    def check_student_info(self,stu):
        """
        :return: student info
        """
        for value in stu.stu_dict.values():
            if not value:
                QMessageBox.warning(self, "warning", "学生信息填写不完整")
                return False
        return True

    def connect_signal_slot(self):
        """
        connect qt signal and slot
        :return:
        """
        pass

    def read_rfid(self,rfid):
        # print(msg)
        self.lineEdit_student_IdCard.setText(rfid)

    def register_stu_sql(self,stu,course_checked):
        try:
            self.stu_info_operate=StuInfoOperate(stu)
        except Exception as e:
            QMessageBox.information(self, "错误!", "数据库连接失败!!!", QMessageBox.Yes)
            self.log.info_out('学生注册：{}'.format(e))
            return
        info,reslut=self.stu_info_operate.insert_stu()
        if not reslut:
            self.log.info_out('学生注册：学生插入信息{}'.format(info))
            return
        values_list = []
        if course_checked:
            for i in course_checked:
                values_tuple = (stu['stuID'], stu['name'],
                                self.course_obj_list[i]['course_id'],
                                self.course_obj_list[i]['course_name'])
                values_list.append(values_tuple)
            VALUES=",".join(str(i) for i in values_list)
            sql ='INSERT INTO stu_course_mapping_table (stuID,name,course_id,course_name) VALUES {}'.format(VALUES)
            #sql="INSERT INTO stu_course_mapping_table (stuID,name,course_id,course_name) VALUES ('201922011425', '刘鑫', '1255', 'python程序设计'),('201922011425', '刘鑫', '1245', 'C++程序设计')"
            info,reslut=self.stu_info_operate.excute_cmd(sql)
            if reslut:
                self.log.info_out('学生注册：注册成功')
            else:
                QMessageBox.information(self, "错误!", "插入失败!!!{}".format(info), QMessageBox.Yes)
        #close connect of mysql
        self.stu_info_operate.close_db()

