# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/9/26 19:12
"""

class Student(object):
    """

    """
    def __init__(self,stuID=0,name=0,team=0,rfid=0,permission=0,registered_course=0):
        self.stu_dict={'stuID':0,'name':0,'team':0,'rfid':0,
                       'permission':0,'registered_course':0}
        self.stu_dict['stuID']=stuID
        self.stu_dict['name'] =name
        self.stu_dict['team'] =team
        self.stu_dict['rfid'] =rfid
        self.stu_dict['permission']=permission
        self.stu_dict['registered_course'] = registered_course

    def get_stu_info(self,key):
        return self.stu_dict[key]

    def __str__(self):
        string = "\n" + "stuID:"+ str(self.stu_dict['stuID']) + "\n" + \
            "name:"+ str(self.stu_dict['name']) + "\n" + \
            "team:"+ str(self.stu_dict['team']) + "\n" + \
            "rfid:"+ str(self.stu_dict['rfid']) + "\n" + \
            "permission:"+ str(self.stu_dict['permission']) + "\n" + \
            "registered_course:"+ str(self.stu_dict['registered_course']) + "\n"

        return string




