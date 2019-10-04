# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/9/21 14:47
"""

import threading
import time
import pymysql
import xlwt
from student import Student

class SqlOperate(object):
    """
    the class is used for connect mysql and execute sql command
    """

    __connectcmd__ = \
        {
            'host': 'localhost',
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
            return "commit succeful!"
        except Exception  as e:
            threadLock.release()# release the lock
            return e

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
            results = cursor.fetchall()
            return "commit succeful!",results,all_fields
        except Exception  as e:
            return e,0

    # close database
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
        msg=self.insert_data('stu_info_table',self.stu.stu_dict)
        return msg

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
        msg,results,all_fields=self.search_data('stu_info_table',condition_name,condition_rfid)
        i=0
        if results:
            for key in self.stu.stu_dict:
                self.stu.stu_dict[key] = results[0][i]
                i += 1
            return msg
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
        msg = self.insert_data('record_table', self.record_dict)
        return msg

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
            condition_time="time>'{0}' and time < '{1}'".format(time_range[0],time_range[1])
        if name is not None:
            condition_name="name='{}'".format(name)
        if team is not None:
            condition_team="team='{}'".format(team)
        if islate is not None:
            condition_islate="islate='{}'".format(islate)
        msg,returns,all_fields=self.search_data('record_table',condition_time,condition_name,condition_team,condition_islate)
        return msg,returns,all_fields

    def mysql2excel(self,mysql_data=None,all_fields=None,file_name=None):
        excel = xlwt.Workbook()
        table = excel.add_sheet("table1")
        row_number = len(mysql_data)
        column_number = len(all_fields)
        for i in range(column_number):
            table.write(0, i, all_fields[i][0])
        for i in range(row_number):
            for j in range(column_number):
                table.write(i + 1, j, str(mysql_data[i][j]))
        excel.save(file_name)

##################################################################
class CourseOperate(SqlOperate):
    """

    """
    def __init__(self,course,db=None):
        if db is not None:    #actually, if we didn't create a db object,we need create a new by calling sql_operate.__init__()
            self.db=db
        else:
            super().connect_sql()
        self.course =course

    def insert_course(self):
        msg=self.insert_data('stu_course_mapping_table',self.course)
        # return msg



