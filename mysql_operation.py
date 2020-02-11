# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/9/21 14:47
"""

import threading
import time

import xlwt
import pymysql
from student import Student
from course import Course


class SqlOperate(object):
    """
    the class is used for connect mysql and execute sql command
    """

    __connectcmd__ = \
        {
            'host': '192.168.3.11',
            'user': 'root',
            'passwd': '123',
            'db': 'attendance_schema_401',
            'port': 3306,
            'charset': 'utf8'
        }
    __insertcmd__= "INSERT INTO {table_name}  VALUES ({values})"
    __searchcmd__="SELECT * FROM {table_name}  WHERE {conditions}"
    __updatecmd__=""

    def connect_sql(self):
        """
        connect mysql database
        :return:
        """
        try:
            self.db = pymysql.connect(**self.__connectcmd__) #establish connection
            msg="连接成功"
            return msg,self.db
        except Exception as e:
            self.db =None
            return e,self.db


    def get_db(self):
        return self.db

    def dict2sql(self,dict):
        """
        convert value of dict into sql_values
        :param dict:
        :return:
        """
        dict_value_str = ''
        for key in dict:
            value=dict[key]
            #determine if value is the type of str
            if(isinstance(value,str)):
                dict_value_str += ('\'%s\''%str(value) + ',')
            else:
                dict_value_str += (str(value) + ',')
        dict_value_str = dict_value_str.rstrip(',')
        return dict_value_str

    def insert_data(self,table_name,columns_dict):
        """
        insert data into database
        :param tabelname:
        :param columns_dict:
        :return:
        """
        # get threadlock
        threadLock=threading.Lock()
        threadLock.acquire()
        try:
            cursor = self.db.cursor()
            values =self.dict2sql(columns_dict)
            sql =self.__insertcmd__.format(table_name=table_name,values=values)
            cursor.execute(sql)
            self.db.commit()
            threadLock.release()# release the lock
            return 0,True
        except Exception  as e:
            threadLock.release()# release the lock
            return e,False

    #search data
    def search_data(self,table,*args):
        """
        search the data of table based on args(mysql conditions)
        :param table:
        :param args:
        :return:
        """
        conditions =''
        for i in args:
            if i.isspace() is not True :
                conditions +=(i+' AND ')
        conditions = conditions.rstrip(' AND ')
        try:
            cursor = self.db.cursor()
            sql =self.__searchcmd__.format(table_name=table,conditions=conditions)
            cursor.execute(sql)
            all_fields = cursor.description
            info = cursor.fetchall()
            return info,all_fields,True
        except Exception  as e:
            return e,0,False

    def excute_cmd(self,sql):
        """
        excute any sql
        :param sql:
        :return:
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            info = cursor.fetchall()
            return info,True
        except Exception  as e:
            return e,False

    def close_db(self):
        self.db.close()

########################################################################
class StuInfoOperate(SqlOperate):
    """
    the class is used for connect mysql and execute sql command
    """
    def __init__(self,stu,db=None):
        if db is not None:    #actually, if we didn't create a db object,we need create a new by calling sql_operate.__init__()
            self.db=db
        else:
            super().connect_sql()
        self.stu =stu

    def insert_stu(self):
        """
        insert new student into `stu_info_table`
        :return:
        """
        info,reslut=self.insert_data('stu_info_table',self.stu.stu_dict)
        return info,reslut

    def search_stu(self,stuID=None,rfid=None):
        """
        search the infomation of student based on stuID，（Notice：just return one students）
        :param stuID:
        :return:msg:the info of running
        """
        condition_name=' '
        condition_rfid=' '
        if stuID is not None:
            condition_name="stuID='{}'".format(stuID)
        if rfid is not None:
            condition_rfid="rfID='{}'".format(rfid)
        info,all_fields,reslut=self.search_data('stu_info_table',condition_name,condition_rfid)
        i=0
        if info:
            for key in self.stu.stu_dict:
                self.stu.stu_dict[key] = info[0][i]
                i += 1
            return "commit successful!"
        else:
            return "未找到信息！"


        # return_stu=Student()

##############################################################

class RecordOperate(SqlOperate):
    def __init__(self,stu,db=None):
        if db is not None:    #actually, if we didn't create a db object,we need create a new by calling sql_operate.__init__()
            self.db=db
        else:
            super().connect_sql()
        self.stu =stu
        self.record_dict={'index':0,'stuID':0,'name':0,'team':0,'time':0,'islate':0}
    def get_time(self):
        """
        get nowtime
        :return:
        """
        self.insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    def insert_record(self,islate):
        """
        insert the record of attendance
        :param islate: 0 or 1
        :return:
        """
        self.get_time()
        self.record_dict['stuID']=self.stu['stuID']
        self.record_dict['name'] =self.stu['name']
        self.record_dict['team'] =self.stu['team']
        self.record_dict['time'] =self.insert_time
        self.record_dict['islate']=islate
        info,reslut = self.insert_data('record_table', self.record_dict)
        return info,reslut

    def search_record(self,time_range=None,name=None,team=None,islate=None):
        """
        Search base by criteria.
        :param time_range:
        :param stuID:
        :param name:
        :param team:
        :return:
        """
        condition_time=' '
        condition_name=' '
        condition_team=' '
        condition_islate=' '
        if time_range is not None:
            condition_time="time>='{0}' and time <= '{1}'".format(time_range[0],time_range[1])
        if name is not None:
            condition_name="name='{}'".format(name)
        if team is not None:
            condition_team="team='{}'".format(team)
        if islate is not None:
            condition_islate="islate='{}'".format(islate)
        info,all_fields,returns=self.search_data('record_table',condition_time,condition_name,condition_team,condition_islate)
        return info,all_fields,returns

    def mysql2excel(self,mysql_data=None,all_fields=None,file_name=None):
        excel = xlwt.Workbook()
        table = excel.add_sheet("sheet1")
        row_number = len(mysql_data)
        column_number = len(all_fields)
        for i in range(column_number):
            table.write(0, i, all_fields[i][0])
        for i in range(row_number):
            for j in range(column_number):
                table.write(i + 1, j, mysql_data[i][j])
        excel.save(file_name)

##################################################################
class CourseOperate(SqlOperate):
    """

    """
    def __init__(self,db=None):
        if db is not None:    #actually, if we didn't create a db object,we need create a new by calling sql_operate.__init__()
            self.db=db
        else:
            super().connect_sql()

    def insert_course(self,course):
        info,reslut=self.insert_data('course_table',course.course_dict)
        return info,reslut

    def update_course_effectiveness(self):
        msg,reslut=self.excute_cmd('UPDATE course_table SET effectiveness =0')
        msg,reslut = self.excute_cmd('UPDATE course_table SET effectiveness =1 \
        WHERE DATE(NOW()) BETWEEN start_date AND end_date')
        return msg,reslut

    def search_course(self):
        course_obj_list=[]
        sql='SELECT * FROM course_table'
        info,reslut=self.excute_cmd(sql)
        if reslut:
            for course in info:
                course_obj = Course(course_id=course[0],
                                    course_name=course[1],
                                    start_date=course[2].strftime("%Y-%m-%d"),
                                    end_date=course[3].strftime("%Y-%m-%d"),
                                    lesson_weekday= course[4],
                                    start_time=str(course[5]),
                                    end_time=str(course[6]),
                                    effectiveness=course[7])
                course_obj_list.append(course_obj)
            return course_obj_list,reslut
        else:
            return info,reslut









