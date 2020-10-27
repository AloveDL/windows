import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainWindow import *
from login.logistic import *



class MainWindow(QMainWindow):
    def __init__(self,):
        super(MainWindow, self).__init__()
        self.myMainWindow = MyMainWindow()
        # styleFile = 'QSS/login.qss'
        # style = CommonHelper.readQss(styleFile)
        self.myMainWindow.setStyleSheet("#MainWindow{border-image:url(images/login.png);}")
        self.myMainWindow.show()







if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MainWindow()
    sys.exit(app.exec_())