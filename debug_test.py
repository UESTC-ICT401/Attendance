# -*- coding: utf-8 -*-

"""
@author: liuxin
@contact: xinliu1996@163.com
@Created on: 2019/9/20 22:16
"""
import serial #导入模块
try:
    portx="COM3"
    bps=115200
    #超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
    timex=None
    ser=serial.Serial(portx,bps,timeout=timex)
    print("串口详情参数：", ser)

    #十六进制的发送
    result=ser.write(chr(0x06).encode("utf-8"))#写数据
    print("写总字节数:",result)


    #十六进制的读取
    while True:
        print(ser.read().hex())#读一个字节

    print("---------------")
    ser.close()#关闭串口

except Exception as e:
    print("---异常---：",e)