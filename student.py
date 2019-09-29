# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/9/26 19:12
"""

from enum import Enum

class Student(object):
    """
    student class

    Notice:in python3.6+ ,dict can keep its order when we try to access it
    """
    def __init__(self,stuID=0,name=0,team=0,rfid=0,permission=0,registered_course=0):
        self.stu_dict={'stuID':0,'name':0,'team':0,'rfid':0,'permission':0,'registered_course':0}
        self.stu_dict['stuID']=stuID
        self.stu_dict['name'] =name
        self.stu_dict['team'] =team
        self.stu_dict['rfid'] =rfid
        self.stu_dict['permission']=permission
        self.stu_dict['registered_course'] = registered_course

    def __setitem__(self, key, value):
        self.stu_dict[key]=value

    def __getitem__(self, item):
        return self.stu_dict[item]



