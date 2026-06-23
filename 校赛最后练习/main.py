import sys
from PyQt6.QtWidgets import QApplication,QMainWindow
from PyQt6.QtGui import QAction,QActionGroup
from mainui import Ui_MainWindow

class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui=self.setupUi(self)


if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MyMainWindow()
    window.show()
    sys.exit(app.exec())
