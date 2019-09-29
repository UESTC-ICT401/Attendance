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

    def __init__(self):
        self.__connect_sql()
    def __connect_sql(self):
        """
        connect mysql database
        :return:
        """
        try:
            self.db = pymysql.connect(**self.__connectcmd__) #establish connection
        except Exception as e:
            self.db =None

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
            super().__init__()
        self.stu =stu

    def insert_stu(self):
        """
        insert new student into `stu_info_sheet`
        :return:
        """
        msg=self.insert_data('stu_info_sheet',self.stu.stu_dict)
        return msg

    def search_stu(self,stuID=None,rfID=None):
        """
        search the infomation of student based on stuID，（Notice：just return one students）
        :param stuID:
        :return:msg:the info of running
        """
        condition_name=' '
        condition_rfID=' '
        if stuID is not None:
            condition_name="stuID='{}'".format(stuID)
        if rfID is not None:
            condition_islate="rfID='{}'".format(rfID)
        msg,results,all_fields=self.search_data('stu_info_sheet',condition_name,condition_rfID)
        i=0
        for key in stu.stu_dict:
            stu.stu_dict[key]=results[0][i]
            i+=1
        return msg
        # return_stu=Student()

##############################################################

class RecordOperate(SqlOperate):
    def __init__(self,stu,db=None):
        if db is not None:    #actually, if we didn't create a db object,we need create a new by calling sql_operate.__init__()
            self.db=db
        else:
            super().__init__()
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
        self.record_dict['stuID']=stu['stuID']
        self.record_dict['name'] =stu['name']
        self.record_dict['team'] =stu['team']
        self.record_dict['time'] =self.insert_time
        self.record_dict['islate']=islate
        msg = self.insert_data('record_sheet', self.record_dict)
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
            condition_time="time<'{0}' and time > '{1}'".format(time_range[0],time_range[1])
        if name is not None:
            condition_name="name='{}'".format(name)
        if team is not None:
            condition_team="team='{}'".format(team)
        if islate is not None:
            condition_islate="islate='{}'".format(islate)
        msg,returns,all_fields=self.search_data('record_sheet',condition_time,condition_name,condition_team,condition_islate)
        print(returns)
        return msg,returns,all_fields

    def mysql2excel(self,mysql_data,all_fields):
        excel = xlwt.Workbook()
        sheet = excel.add_sheet("sheet1")
        row_number = len(mysql_data)
        column_number = len(all_fields)
        for i in range(column_number):
            sheet.write(0, i, all_fields[i][0])
        for i in range(row_number):
            for j in range(column_number):
                sheet.write(i + 1, j, str(mysql_data[i][j]))
        excelName = "考勤.xls"
        excel.save(excelName)





stu=Student()
stu_info_operate=StuInfoOperate(stu)
stu_info_operate.search_stu('201922011425')
db=stu_info_operate.get_db()
my =RecordOperate(stu,db)
msg=my.insert_record(islate=0)
msg,mysql_data,all_fileds=my.search_record(team='程建')
my.mysql2excel(mysql_data,all_fileds)