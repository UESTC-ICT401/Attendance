from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QGridLayout)
import sys
from UI.ui_mainWin import Ui_MainWindow
from UI.student_register import StudentRegister
from UI.com import ComWindows
from UI.student_swipe import StudentSwipe
from log_output import Mylog
from serial_read import Serial




class Windows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Windows, self).__init__()
        self.setupUi(self)
        self.signal_slot_connect()
        #call_func is the callfunction of serial listening-threading.
        self.log=Mylog("log/student_register.txt")
        #Warnning: the next 5 commands can't be exchanged.
        # create serial obj and open COM1(first com of com_list).
        self.init_com_obj()
        self.com_win = ComWindows(target=self.change_com,args='')
        #create mysql connect obj.
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
        for i in range(self.gridLayout_widget.count()):
            self.gridLayout_widget.itemAt(i).widget().deleteLater()
        self.student_register = StudentRegister(self.log)
        self.ser.target=self.student_register.read_rfid
        self.student_register.load_team_info(["刘鑫", "李行宇", "林仕文"])
        self.gridLayout_widget.addWidget(self.student_register)

    def open_swipe_windows(self):
        """
        open register window
        delete all widgets of gridLayout_widget,and recreate register obj ,add this widget on gridLayout_widget
        :return:
        """
        for i in range(self.gridLayout_widget.count()):
            self.gridLayout_widget.itemAt(i).widget().deleteLater()
        self.student_swipe = StudentSwipe(self.log,target=None,args='')
        self.student_swipe.load_team_info(["刘鑫", "李行宇", "林仕文"])
        self.gridLayout_widget.addWidget(self.student_swipe)
        self.ser.target=self.student_swipe.read_rfid


    def open_com_windows(self):
        """
        put com list info into combox of com_win
        :return:
        """
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
        self.ser= Serial()
        com_list=self.ser.search_port()
        if com_list:
            print(com_list[0][0])
            msg,info=self.ser.port_init(com_list[0][0],bps=9600)
            self.log.info_out(msg)
            self.log.debug_out(info)
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
        try:
            self.com_win.close()
            self.ser.close()
            self.ser.port_init(com_name,bps=9600)
            self.ser.start()
        except Exception as e:
            self.log.debug_out(e)







if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Windows()
    ex.show()
    sys.exit(app.exec_())

