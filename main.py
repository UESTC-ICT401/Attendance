# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/9/20 20:51
"""

import log_output
import queue
import serial_read

rfid_q=queue.Queue(12)

myserial = serial_read.Serial(rfid_q)
port_name=myserial.search_port()[0][0]
print(port_name)
myserial.port_init(str(port_name))
myserial.start()
while True:
    data=rfid_q.get()
    print(data)





