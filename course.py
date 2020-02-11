# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/10/3 15:54
"""
class Course(object):
    """
    the class is used for saving courses infomations
    """
    def __init__(self,course_id=None,course_name=None,start_date=None,end_date=None,lesson_weekday=None,
                 start_time=None,end_time=None,effectiveness=1):
        self.course_dict = {'course_id': 0, 'course_name': 0, 'start_date': 0, 'end_date': 0,
                         'lesson_weekday': 0, 'start_time': 0,'end_time': 0, 'effectiveness': 0}
        self.course_dict['course_id'] = course_id
        self.course_dict['course_name'] = course_name
        self.course_dict['start_date'] = start_date
        self.course_dict['end_date'] = end_date
        self.course_dict['lesson_weekday'] = lesson_weekday
        self.course_dict['start_time'] = start_time
        self.course_dict['end_time'] = end_time
        self.course_dict['effectiveness'] = effectiveness

    def __getitem__(self, item):
        return self.course_dict[item]
