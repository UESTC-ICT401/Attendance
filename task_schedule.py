# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/10/4 15:37
"""
import schedule
import time
import threading

class TaskSchedule(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self)
        self.task_list=[]

    def add_weekday_task(self,task_name,target=None):
        """
        add weekday task to schedule and task_list
        :param tsak_name: the name of task
        :param target: callback function
        :return:
        """
        schedule.every().friday.at('16:00').do(target,task_name=task_name)
        self.task_list.append(task_name)

    def add_everyday_task(self,task_name,time='8:30',target=None):
        """
        add everyday task to schedule and task_list
        :param task_name:
        :param time:
        :param target:
        :return:
        """
        schedule.every().day.at(time).do(target,task_name=task_name)
        self.task_list.append(task_name)
    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(20)





