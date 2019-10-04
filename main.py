from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QGridLayout)
from PyQt5.QtCore import Qt,pyqtSignal
import sys
import time
from UI.ui_mainWin import Ui_MainWindow
from UI.student_register import StudentRegister
from UI.com import ComWindows
from UI.student_swipe import StudentSwipe
from log_output import Mylog
from serial_read import Serial
from task_schedule import TaskSchedule
from global_value import *



class Windows(QMainWindow, Ui_MainWindow):
    #this signal is very important for communication between serial thread and UI thread
    recv_signal = pyqtSignal(str)
    task_signal =pyqtSignal(str)

    def __init__(self):
        super(Windows, self).__init__()
        self.setupUi(self)
        self.log=Mylog("log/student_register.txt")
        self.log.info_out('初始化：开始运行')
        self.signal_slot_connect()
        #init com window
        self.init_com_obj()
        #default wiget is the swipe wiget
        self.open_swipe_windows()

    def signal_slot_connect(self):
        """
        connect signals and slots of Qt
        :return:
        """
        #record the connecting slot
        self.serial_connect_slot=None
        self.actionRegister.triggered.connect(self.open_register_windows)
        self.actionCOM.triggered.connect(self.open_com_windows)
        self.actionSwipe.triggered.connect(self.open_swipe_windows)
        # self.actionregister.triggered.connect()

    def init_task(self):
        """
        create time task schedule including(every Sunday ,evey Morn,After,Even)
        :return:
        """
        self.log.info_out('开启定时任务')
        self.task_schedule = TaskSchedule()
        self.task_schedule.add_weekday_task(task_name='clean_course',target=self.time_task_callback)
        self.task_schedule.add_everyday_task(task_name='morning_attendance',
                                             target=self.time_task_callback,time=MORINING_TIME)
        self.task_schedule.add_everyday_task(task_name='afternoon_attendance',
                                             target=self.time_task_callback,time=AFTERNOON_TIME)
        self.task_schedule.add_everyday_task(task_name='evening_attendance',
                                             target=self.time_task_callback,time=EVENING_TIME)

    def init_com_obj(self):
        """
        init com obj including creating
        :return:
        """
        self.ser= Serial(target=self.serial_callback,args='')
        com_list=self.ser.search_port()
        if com_list:
            msg=self.ser.port_init(com_list[0][0],bps=9600)
            self.log.info_out('串口初始化:{}'.format(msg))
            self.ser.start()
            return com_list
        else:
            QMessageBox.information(self, "错误!", "未发现读写器，请检查读写器连接!!!", QMessageBox.Yes)

    def serial_callback(self,msg):
        """
        this function is used for recv serial msg
        :param msg:
        :return:
        """
        self.recv_signal.emit(msg)

    def time_task_callback(self,task_name):
        """
        this function is used for recv seri
        :param task_name:
        :return:
        """
        self.log.info_out('定时任务:{}'.format(task_name))
        self.task_signal.emit(task_name)

    def open_register_windows(self):
        """
        open register window
        delete all widgets of gridLayout_widget,and recreate register obj ,add this widget on gridLayout_widget
        :return:
        """
        self.log.info_out('注册：开启注册界面！')
        self.student_register = StudentRegister(self.log)
        if self.serial_connect_slot is not None:
            self.recv_signal.disconnect(self.serial_connect_slot)
        self.serial_connect_slot=self.student_register.read_rfid
        self.recv_signal.connect(self.serial_connect_slot)
        #移除所有添加的控件，同时对象会被回收!!!!!!!
        for i in range(self.gridLayout_widget.count()):
            self.gridLayout_widget.itemAt(i).widget().deleteLater()
        self.student_register.load_team_info(CHARGE_PERSONS)
        self.gridLayout_widget.addWidget(self.student_register)

    def open_swipe_windows(self):
        """
        open register window
        delete all widgets of gridLayout_widget,and recreate register obj ,add this widget on gridLayout_widget
        :return:
        """
        self.log.info_out('打卡：开启打卡界面！')
        self.student_swipe = StudentSwipe(self.log, target=None, args='')
        if self.serial_connect_slot is not None:
            self.recv_signal.disconnect(self.serial_connect_slot)
        self.serial_connect_slot=self.student_swipe.read_rfid
        self.recv_signal.connect(self.serial_connect_slot)
        for i in range(self.gridLayout_widget.count()):
            self.gridLayout_widget.itemAt(i).widget().deleteLater()
        self.student_swipe.load_team_info(CHARGE_PERSONS)
        self.gridLayout_widget.addWidget(self.student_swipe)
        # self.call_func=self.student_swipe.read_rfid


    def open_com_windows(self):
        """
        put com list info into combox of com_win
        :return:
        """
        self.com_win = ComWindows(target=self.change_com, args='')
        com_list=self.ser.search_port()
        if com_list:
            self.com_win.put_com_list(com_list)
            self.com_win.show()
        else:
            QMessageBox.information(self, "错误!", "未发现读写器，请检查读写器连接!!!", QMessageBox.Yes)



    def change_com(self,com_name):
        """
        close com and restart com
        :param com_name:
        :return:
        """
        self.com_win.close()
        self.ser.close()
        time.sleep(0.2)
        msg=self.ser.port_init(com_name,bps=9600)
        self.log.info_out('串口切换:{}'.format(msg))







if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Windows()
    ex.show()
    sys.exit(app.exec_())

