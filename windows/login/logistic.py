import sys

import MySQLdb
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from login.login import Ui_MainWindow
from mainWindow import DetectionWindow
from login.dbOperate import *
from tip import *


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('C:\\Users\\27635\\PycharmProjects\windows\windows\images/logo1.png'))
        # self.setWindowIcon(QIcon('../images/logo1.png'))
        self.setWindowTitle('胃癌组织病理辅助诊断系统')
        self.ms = dbConnect()
        #登录槽函数
        self.login_btn.clicked.connect(self.login_trans)

    def login_trans(self,ms):
        username = self.un_edit.text()
        password = self.pwd_edit.text()
        #print(username)
        #print(password)
        if(username == "" or password == ""):
            self.warning()
        else:
            ms = self.ms
            if password == ms.getpassword(username):
                self.close()
                self.detectionWindow = DetectionWindow()
                self.detectionWindow.show()
            else:
                self.error()
                self.pwd_edit.clear()

    def warning(self):

        QMessageBox.warning(self, '警告', '账号或密码不能为空', QMessageBox.Yes, QMessageBox.Yes)

    def error(self):
        QMessageBox.critical(self, "错误", "账号密码错误，请再次检查", QMessageBox.Yes, QMessageBox.Yes)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    # MainWindow = MainWindow()
    myWin.show()
    sys.exit(app.exec_())

