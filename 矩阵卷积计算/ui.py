import sys
from PyQt6.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt6.QtCore import QFile,QTextStream,QIODevice
from window import Ui_MainWindow
from prossce import func1





def open(path):
    file=QFile(path)
    list_input=[]
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('错误')
        return
    else:
        stream=QTextStream(file)
        while not stream.atEnd():
            line=stream.readLine()
            part=line.split()
            part=[float(i) for i in part]
            list_input.append(part)
    return list_input

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.action_open_M.triggered.connect(self.open_M)
        self.action_open_N.triggered.connect(self.open_N)
        self.action_count.triggered.connect(self.count)






    def open_M(self):
        file_path,_=QFileDialog.getOpenFileName(self,'选择文件','.','txt(*.txt)')
        self.lisM=open(file_path)
        self.textBrowser.clear()
        r=''
        for i in self.lisM:
            for k in i:
                r=r+f'{k} '
            r=r+'\n'
        self.textBrowser.setText(r)

    def open_N(self):
        file_path,_=QFileDialog.getOpenFileName(self,'选择文件','.','txt(*.txt)')
        self.lisN=open(file_path)
        self.textBrowser.clear()
        r=''
        for i in self.lisM:
            for k in i:
                r=r+f'{k} '
            r=r+'\n'
        self.textBrowser.setText(r)


    def count(self):
        r=func1(self.lisN,self.lisM)
        self.textBrowser.clear()
        self.textBrowser.setText(r)

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
