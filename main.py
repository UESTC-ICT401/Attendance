from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QMainWindow, QGridLayout)
import sys
from UI.ui_mainWin import Ui_MainWindow
from UI.student_register import student_register
from UI.ui_com import Ui_Com_Form
from log_output import Mylog
from serial_read import Serial
from mysql_operation import *

class Com_Windows(QWidget,Ui_Com_Form):
    def __init__(self,target,args=None):
        super(Com_Windows,self).__init__()
        self.target=target
        self.args=args
        self.setupUi(self)
        self.signal_slot_connect()

    def put_com_list(self,com_list):
        """
        input the list of com name
        :param com_list:
        :return:
        """
        for port in com_list:
            self.comboBox_com.addItem(port[0])


    def signal_slot_connect(self):
        """
        connect signals and slots of Qt
        :return: chioced combox name
        """
        self.pushButton_ok.clicked.connect(self.call_fun)

    def call_fun(self):
        self.args = str(self.comboBox_com.currentText())
        self.target(self.args)



class Windows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Windows, self).__init__()
        self.setupUi(self)
        self.signal_slot_connect()
        self.log=Mylog("log/student_register.txt")
        #Warnning: the next 3 commands can't be exchanged
        self.student_register = student_register(self.log,self.register_stu_sql)
        # create serial obj and open COM1(first com of com_list)
        self.init_com_obj()
        self.com_win = Com_Windows(target=self.change_com,args='')
        #create mysql connect obj
        self.sql=SqlOperate()
        msg,self.db=self.sql.connect_sql()
        if self.db :
            self.log.info_out(msg)
        else:
            QMessageBox.information(self, "错误!", "数据库连接失败!!!", QMessageBox.Yes)
            self.log.debug_out(msg)

        # self.student_register.load_course_info(["adsfa","asdfasdf","asdf","asdfaf","asdfasdf"])
        self.student_register.load_team_info(["刘鑫","李行宇","林仕文"])

        self.gridLayout_widget.addWidget(self.student_register)
        #create com obj


    def signal_slot_connect(self):
        """
        connect signals and slots of Qt
        :return:
        """
        self.actionCOM.triggered.connect(self.open_com_windows)
        # self.actionregister.triggered.connect()

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
        self.ser= Serial(target=self.student_register.read_rfid,args='')
        com_list=self.ser.search_port()
        if com_list:
            msg,info=self.ser.port_init(com_list[0][0],bps=9600)
            self.log.debug_out(msg)
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
            pass

    def register_stu_sql(self,stu):
        print(stu)
        self.stu_info_operate = StuInfoOperate(stu=stu,db=self.db)
        msg=self.stu_info_operate.insert_stu()
        self.log.info_out(msg)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Windows()
    ex.show()
    sys.exit(app.exec_())

