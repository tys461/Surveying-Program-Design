import sys
from PyQt6.QtWidgets import QMainWindow,QApplication,QFileDialog,QMessageBox
from PyQt6.QtCore import QFile,QTextStream,QIODevice
from process import Point,Points

from window import Ui_MainWindow

def open(path):
    file=QFile(path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('读取失败')
        return
    lis_points=[]
    stream=QTextStream(file)
    while not stream.atEnd():
        part=stream.readLine().split(',')
        lis_points.append(Point(part[0],float(part[1]),float(part[2]),float(part[3])))

    return Points(lis_points)





class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.action_open.triggered.connect(self.open_write)

    def open_write(self):
        file_path,_=QFileDialog.getOpenFileName(self,'选择点文件','.','txt(*.txt)')
        self.points=open(file_path)





if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec())


