# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/9/20 20:50
"""
import serial
import threading
import queue
import serial.tools.list_ports

class Serial(threading.Thread):
    """
    @this class is used for searching serial port
    and creating a thread for listening it.

    @Attributes:
    q:the queue of recv
    """
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.q = q

    def search_port(self):
        """
        search the all of ports of this device
        :return port_list: list of ports
        """
        port_list = list(serial.tools.list_ports.comports())
        return port_list

    def port_init(self,port_name,bps=115200,timeout=None):
        """
        initialize the serial port
        :param port_name:
        :param bps: bounding rate,default = 115200
        :param timeout: default = 0
        :return str.format(ser):the describ of the port
        """
        self.ser = serial.Serial(port_name, bps, timeout=timeout)
        str='specification of serial port：{0}'
        return self.ser,str.format(self.ser)

    def run(self):
        """
        the thread of listening
        :return:
        """
        while True:
            try:
                msg = self.ser.read().hex()
                self.q.put(msg)
            except Exception as e:
                return e

