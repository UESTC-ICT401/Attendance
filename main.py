from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QGridLayout)
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QPixmap,QPalette,QBrush,QPainter
import sys
import time
from UI.ui_mainWin import Ui_MainWindow
from UI.student_register import StudentRegister
from UI.com import ComWindows
from UI.student_swipe import StudentSwipe
from UI.course_add import CourseAdd
from log_output import Mylog
from serial_read import Serial
from task_schedule import TaskSchedule
from global_value import *
from course import  Course



class Windows(QMainWindow, Ui_MainWindow):
    #this signal is very important for communication between serial thread and UI thread
    recv_signal = pyqtSignal(str)
    check_task_signal =pyqtSignal(str)
    attendance_task_signal = pyqtSignal(str)

    def __init__(self):
        super(Windows, self).__init__()
        self.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./UI/picture/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.log=Mylog("log/student_register.txt")
        self.log.info_out('初始化：开始运行')
        self.signal_slot_connect()
        #init com window
        self.init_com_obj()
        #default wiget is the swipe wiget
        self.open_swipe_windows()
        self.init_task()

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.log.info_out('退出：QT线程退出')
            self.ser.stop()
            self.log.info_out('退出：串口线程设置退出')
            self.task_schedule.stop()
            self.log.info_out('退出：定时任务线程设置退出')
            event.accept()
        else:
            event.ignore()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        size=self.size()
        # painter.setPen(self.NoPen)
        painter.drawPixmap(0, 0, size.width(),size.height(), QPixmap("./UI/picture/ground.jpeg"))
        painter.end()

    def signal_slot_connect(self):
        """
        connect signals and slots of Qt
        :return:
        """
        #record the connecting slot
        # self.serial_connect_slot=None
        self.actionRegister.triggered.connect(self.open_register_windows)
        self.actionCOM.triggered.connect(self.open_com_windows)
        self.actionSwipe.triggered.connect(self.open_swipe_windows)
        self.actionCourseRegister.triggered.connect(self.open_course_register_windows)
        # self.actionregister.triggered.connect()

    def init_task(self):
        """
        create time task schedule including(every Sunday ,evey Morn,After,Even)
        :return:
        """
        self.log.info_out('开启定时任务')
        self.task_schedule = TaskSchedule()
        self.task_schedule.add_weekday_task(task_name='check_courses',target=self.time_task_callback)
        self.task_schedule.add_everyday_task(task_name='set_late',
                                             target=self.time_task_callback,time=MORINING_ATTENDANCE_TIME)
        self.task_schedule.add_everyday_task(task_name='set_late',
                                             target=self.time_task_callback,time=AFTERNOON_ATTENDANCE_TIME)
        self.task_schedule.add_everyday_task(task_name='set_late',
                                             target=self.time_task_callback,time=EVENING_ATTENDANCE_TIME)
        self.task_schedule.start()

    def init_com_obj(self):
        """
        init com obj including creating
        :return:
        """
        self.ser= Serial(target=self.serial_callback,args='')
        com_list=self.ser.search_port()
        if com_list:
            try:
                msg=self.ser.port_init(com_list[0][0],bps=9600)
                self.log.info_out('串口初始化:{}'.format(msg))
                self.ser.start()
                return
            except Exception as e:
                self.log.info_out('串口初始化:{}'.format(e))

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
        if task_name == 'check_courses':
            self.check_task_signal.emit(task_name)
            return
        if task_name == 'set_late':
            self.attendance_task_signal.emit(task_name)
            return


    def open_register_windows(self):
        """
        open register window
        delete all widgets of gridLayout_widget,and recreate register obj ,add this widget on gridLayout_widget
        :return:
        """
        self.log.info_out('注册：开启注册界面！')
        self.student_register = StudentRegister(self.log)
        # if self.serial_connect_slot is not None:
        #     self.recv_signal.disconnect(self.serial_connect_slot)
        # self.recv_signal.disconnect(self.student_register.read_rfid)
        self.recv_signal.connect(self.student_register.read_rfid)
        #移除所有添加的控件，同时对象会被回收!!!!!!!
        for i in range(self.gridLayout_widget.count()):
            self.gridLayout_widget.itemAt(i).widget().deleteLater()
        self.student_register.load_team_info(CHARGE_PERSONS)
        self.student_register.load_course_info()
        self.gridLayout_widget.addWidget(self.student_register)

    def open_swipe_windows(self):
        """
        open register window
        delete all widgets of gridLayout_widget,and recreate register obj ,add this widget on gridLayout_widget
        :return:
        """
        self.log.info_out('打卡：开启打卡界面！')
        self.student_swipe = StudentSwipe(self.log, target=None, args='')
        # if self.serial_connect_slot is not None:
        #     self.recv_signal.disconnect(self.serial_connect_slot)
        # self.serial_connect_slot=self.student_swipe.read_rfid
        self.recv_signal.connect(self.student_swipe.read_rfid)
        for i in range(self.gridLayout_widget.count()):
            self.gridLayout_widget.itemAt(i).widget().deleteLater()
        self.student_swipe.load_team_info(CHARGE_PERSONS)
        self.gridLayout_widget.addWidget(self.student_swipe)
        #connect slot
        self.attendance_task_signal.connect(self.student_swipe.check_late)
        self.check_task_signal.connect(self.student_swipe.check_courses)

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

    def open_course_register_windows(self):
        """
        open register window
        delete all widgets of gridLayout_widget,and recreate register obj ,add this widget on gridLayout_widget
        :return:
        """
        self.log.info_out('课程注册：开启注册界面！')
        self.course_add = CourseAdd(self.log)
        for i in range(self.gridLayout_widget.count()):
            self.gridLayout_widget.itemAt(i).widget().deleteLater()
        self.gridLayout_widget.addWidget(self.course_add)

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

