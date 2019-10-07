# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/10/4 15:37
"""
import schedule
import time
import threading
from  global_value import *

class TaskSchedule(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self)
        self.task_list=[]
        self.stop_signal = False

    def stop(self):
        self.stop_signal=True

    def add_weekday_task(self,task_name,target=None):
        """
        add weekday task to schedule and task_list
        :param tsak_name: the name of task
        :param target: callback function
        :return:
        """
        schedule.every().monday.at(CHECK_TIME).do(target,task_name=task_name)
        self.task_list.append(task_name)

    def add_everyday_task(self,task_name,time=None,target=None):
        """
        add everyday task to schedule and task_list
        :param task_name:
        :param time:
        :param target:
        :return:
        """
        schedule.every().day.at(time).do(target,task_name)
        self.task_list.append(task_name,)
    def run(self):
        while True:
            if self.stop_signal:
                return
            schedule.run_pending()
            time.sleep(20)




