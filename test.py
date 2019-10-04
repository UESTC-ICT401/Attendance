# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/10/4 20:42
"""
import time,datetime

date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(date)
day= time.strftime("%A", time.localtime())
if day !=('Sunday' or 'Saturday'):
    print('周末')