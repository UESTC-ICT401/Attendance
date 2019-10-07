# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/9/20 20:50
"""
import serial
import threading
import serial.tools.list_ports


class Serial(threading.Thread):
    """
    @this class is used for searching serial port
    and creating a thread for listening it.

    @Attributes:
    q:the queue of recv
    """
    def __init__(self,target=None,args=None):
        threading.Thread.__init__(self)
        self.target=target
        self.args  =args
        self.stop_signal = False

    def search_port(self):
        """
        search the all of ports of this device
        :return port_list: list of ports
        """
        port_list = list(serial.tools.list_ports.comports())
        return port_list

    def port_init(self,port_name,bps=115200,timeout=0.5):
        """
        initialize the serial port
        :param port_name:
        :param bps: bounding rate,default = 115200
        :param timeout: default = 0.5,if timeout=0,reading will be set Blocking
        :return str.format(ser):the describ of the port
        """
        self.args=''
        self.ser_port = serial.Serial(port_name, bps, timeout=timeout)
        if not self.ser_port.is_open:
            self.open()
        msg='specification of serial port：{0}'
        return msg.format(self.ser_port.port)

    def close(self):
        self.ser_port.close()

    def stop(self):
        self.stop_signal=True

    def open(self):
        self.ser_port.open()

    def run(self):
        """
        the thread of listening
        :return:
        """
        while True:
            if  self.stop_signal:
                return
            try:
                self.args=self.ser_port.read(30).hex()
                if self.target and self.args:
                    self.target(self.args)
            except Exception as e:
                pass
