# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/10/2 10:50
"""
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox,QFileDialog, QMainWindow, QGridLayout,QTableWidgetItem,QCheckBox,QPushButton)
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5 import QtGui
from UI.ui_student_swipe import Ui_Stu_Swipe
from student import Student
from log_output import Mylog
from mysql_operation import *
from global_value import *

class StudentSwipe(QWidget,Ui_Stu_Swipe):

    def __init__(self,log,target=None,args=None):
        super(StudentSwipe,self).__init__()
        self.log=log
        self.setupUi(self)
        self.target=target
        self.args=args
        self.connect_signal_slot()
        self.islate=0


    def load_team_info(self, list_team):
        """
        :param list_team: ["saber","archer","rider"]
        :return:
        """
        for index,(team) in enumerate(list_team):
            self.comboBox_team.addItem(team)

    def connect_signal_slot(self):
        """
        connect qt signal and slot
        :return:
        """
        self.pushButton_extract.clicked.connect(self.extract_to_excel)

    def stu_swipe(self, rfid):
        # self.check_late()
        now_localtime=time.localtime()
        now_time = time.strftime("%H:%M",now_localtime )
        if not ((now_time < MORINING_ATTENDANCE_TIME )or (now_time >MORINING_END_TIME and now_time <AFTERNOON_START_TIME) or\
            (now_time >AFTERNOON_END_TIME and now_time <EVENING_START_TIME)):
            self.textBrowser.append('打卡时间已过！你已迟到！')
            return
        self.log.info_out("考勤刷卡读取信息：{}".format(rfid))
        stu = Student()
        try:
            self.stu_info_operate=StuInfoOperate(stu=stu)
        except Exception as e:
            QMessageBox.information(self, "错误!", "数据库连接失败!!!", QMessageBox.Yes)
            self.log.info_out("考勤刷卡读取信息：{}".format(e))
            return
        msg=self.stu_info_operate.search_stu(rfid=rfid)
        self.textBrowser.append(msg)
        self.log.info_out("RFID搜索结果：{}".format(msg))
        if stu['name']:
            record_operate=RecordOperate(stu=stu,db=self.stu_info_operate.db)
            info,reslut=record_operate.insert_record(islate=0)
            if reslut:
                self.textBrowser.append('{},今天要加油哟！'.format(stu['name']))
                self.log.info_out('考勤记录插入：{}'.format(info))
            record_operate.close_db()

    def check_late(self):
        now_localtime = time.localtime()
        now_time = time.strftime("%H:%M", now_localtime)
        now_weekday = time.strftime("%a", now_localtime)
        #######################################################################
        if now_weekday == ('Sunday' or 'Saturday'):
            return
        now_date = time.strftime("%Y-%m-%d ", now_localtime)
        if now_time>MORINING_START_TIME and  now_time<MORINING_START_TIME:
            start_time = now_date + MORINING_START_TIME
            end_time   =now_date +MORINING_END_TIME
        elif now_time>AFTERNOON_START_TIME and now_time<AFTERNOON_END_TIME:
            start_time = now_date + AFTERNOON_START_TIME
            end_time   =now_date +AFTERNOON_END_TIME
        else:
            start_time = now_date + EVENING_START_TIME
            end_time   =now_date +EVENING_END_TIME
        # 这里必须要用中文了：此sql语句求出所有人当中，除了有课的同学以及已经在合理打卡时间段打过卡的同学以外，没有打卡的人
        #也就是迟到的人的学号，姓名，团队。
        sql = '''CREATE TABLE tmp AS  
                (
                    SELECT stuID,name,team FROM stu_info_table
                    WHERE stuID NOT IN
                    (SELECT stuID FROM record_table WHERE time BETWEEN "{0}" AND "{1}") 
                    AND stuID NOT IN
                    (
                        SELECT stuID FROM stu_course_mapping_table WHERE course_id  
                        IN (SELECT course_id FROM course_table WHERE lesson_weekday ='{2}'  
                        AND effectiveness = 1 
                        AND (CURRENT_TIME() BETWEEN start_time AND end_time))
                    )
                )'''.format(start_time,end_time,now_weekday)
        record_operate = RecordOperate(stu=None)
        info,reslut=record_operate.excute_cmd(sql)
        if not reslut:
            self.log.info_out('搜索打卡记录并创建tmp表储存：{}'.format(info))
            return
        else:
            self.log.info_out('搜索打卡记录并创建tmp表储存：成功！')
            sql = '''INSERT INTO record_table (stuID,name,team ) SELECT stuID,name,team FROM tmp'''
            info, reslut = record_operate.excute_cmd(sql)
            if reslut:
                self.log.info_out('tmp表插入考勤记录：成功！')
            else:
                self.log.info_out('tmp表插入考勤记录：{}'.format(info))
                return

            sql = '''DROP TABLE tmp;'''
            info, reslut = record_operate.excute_cmd(sql)

            sql = '''UPDATE record_table SET time=NOW(),islate=1 WHERE islate IS NULL;'''
            info, reslut = record_operate.excute_cmd(sql)
            if reslut:
                self.log.info_out('完善迟到信息：成功！')
            else:
                self.log.info_out('完善迟到信息：失败！')






    def check_course_effectiv(self):
        """
        check courses if effectivly
        :return:
        """
        course_operate = CourseOperate(stu=None)
        sql='UPDATE course_table SET effectiveness = 0'
        info, reslut = course_operate.excute_cmd(sql)
        sql = 'UPDATE course_table SET effectiveness =1 WHERE DATE(NOW()) BETWEEN start_date AND end_date'
        info, reslut = course_operate.excute_cmd(sql)
        if reslut:
            self.log.info_out("查验课程有效性:成功!")
        else:
            self.log.info_out("查验课程有效性:{}".format(info))


    def read_rfid(self,rfid):
        """
        :param rfid:
        :return:
        """
        self.stu_swipe(rfid)

    def extract_to_excel(self):
        """
        extract attendance record to exel file
        :return:
        """
        student_name = self.lineEd_stuID.text()
        if not student_name:
            student_name=None
        student_team = self.comboBox_team.currentText()
        if not student_team:
            student_team=None
        start_time = self.dateEdit_starttime.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        end_time   = self.dateEdit_endtime.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        try:
            record_operate = RecordOperate(stu=None, db=None)
            self.log.info_out('提取数据：连接数据成功')
        except Exception as e:
            self.log.debuf_out('提取数据:{}'.format(e))
        msg,mysql_data,all_fileds= record_operate.search_record(time_range=(start_time,end_time),name=student_name,
                                                                team=student_team,islate=0)
        self.log.info_out(msg)
        record_operate.close_db()
        file_name =time.strftime("%Y-%m-%d", time.localtime())+'.xls'
        try:
            record_operate.mysql2excel(mysql_data,all_fileds,file_name)
            QMessageBox.information(self, "消息", "提取成功！", QMessageBox.Yes)
            self.log.info_out('提取数据：成功！')
        except Exception as e:
            QMessageBox.information(self, "错误!", "错误原因：{}".format(e), QMessageBox.Yes)
            self.log.debuf_out('提取数据:.{}'.format(e))