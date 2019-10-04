from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QGridLayout)
from PyQt5.QtCore import Qt,pyqtSignal
import sys
from UI.ui_mainWin import Ui_MainWindow
from UI.student_register import StudentRegister
from UI.com import ComWindows
from UI.student_swipe import StudentSwipe
from log_output import Mylog
from serial_read import Serial
import time



class Windows(QMainWindow, Ui_MainWindow):
    #this signal is very important for communication between serial thread and UI thread
    recv_signal = pyqtSignal(str)
    def __init__(self):
        super(Windows, self).__init__()
        self.setupUi(self)
        self.signal_slot_connect()
        #record the connecting slot
        self.connect_slot=None
        #call_func is the callfunction of serial listening-threading.
        self.log=Mylog("log/student_register.txt")
        self.log.info_out('初始化：开始运行')
        self.init_com_obj()
        #default wiget is the swipe wiget
        self.open_swipe_windows()

    def signal_slot_connect(self):
        """
        connect signals and slots of Qt
        :return:
        """
        self.actionRegister.triggered.connect(self.open_register_windows)
        self.actionCOM.triggered.connect(self.open_com_windows)
        self.actionSwipe.triggered.connect(self.open_swipe_windows)
        # self.actionregister.triggered.connect()

    def open_register_windows(self):
        """
        open register window
        delete all widgets of gridLayout_widget,and recreate register obj ,add this widget on gridLayout_widget
        :return:
        """
        self.student_register = StudentRegister(self.log)
        if self.connect_slot is not None:
            self.recv_signal.disconnect(self.connect_slot)
        self.connect_slot=self.student_register.read_rfid
        self.recv_signal.connect(self.connect_slot)
        #移除所有添加的控件，同时对象会被回收。
        for i in range(self.gridLayout_widget.count()):
            self.gridLayout_widget.itemAt(i).widget().deleteLater()
        self.student_register.load_team_info(["刘鑫", "李行宇", "林仕文"])
        self.gridLayout_widget.addWidget(self.student_register)

    def callback_func(self,msg):
        self.recv_signal.emit(msg)


    def open_swipe_windows(self):
        """
        open register window
        delete all widgets of gridLayout_widget,and recreate register obj ,add this widget on gridLayout_widget
        :return:
        """
        self.student_swipe = StudentSwipe(self.log, target=None, args='')
        if self.connect_slot is not None:
            self.recv_signal.disconnect(self.connect_slot)
        self.connect_slot=self.student_swipe.read_rfid
        self.recv_signal.connect(self.connect_slot)
        for i in range(self.gridLayout_widget.count()):
            self.gridLayout_widget.itemAt(i).widget().deleteLater()
        self.student_swipe.load_team_info(["刘鑫", "李行宇", "林仕文"])
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

    def init_com_obj(self):
        """
        init com obj including creating
        :return:
        """
        self.ser= Serial(target=self.callback_func,args='')
        com_list=self.ser.search_port()
        if com_list:
            msg=self.ser.port_init(com_list[0][0],bps=9600)
            self.log.info_out('串口初始化:{}'.format(msg))
            self.ser.start()
            return com_list
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

