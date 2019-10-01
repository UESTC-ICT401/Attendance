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

    def __getitem__(self, item):
        return self.stu_dict[item]

    def __str__(self):
        string="\nstuID:{0}\nname:{1}\nteam:{2}\nrfid:{3}\npermission:{4}\nregistered_course:\n".format(
            self.stu_dict['stuID'],self.stu_dict['name'],self.stu_dict['team'],self.stu_dict['rfid'],
            self.stu_dict['permission'],self.stu_dict['registered_course']
        )
        return string




