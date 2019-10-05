# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/10/4 20:42
"""
import time,datetime

now_localtime = time.localtime()
now_date = time.strftime("%Y-%m-%d ", now_localtime)
start_time=now_date+"8:30:00"
print(start_time)