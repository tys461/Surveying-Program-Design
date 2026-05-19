from PyQt6.QtWidgets import QApplication,QMainWindow,QWidget
from PyQt6.QtCore import QTextStream,QFile,QIODevice

class Open_dat():
    def __init__(self):
        self.list_data=[]
        self.open_file()
        # self.data_cor()

    def open_file(self):
        file=QFile('0624CH67#连续梁.DAT')
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            print('打开失败',file.errorString)
            return
        stream=QTextStream(file)
        # stream.setCodec('utf-8')
        while not stream.atEnd():
            self.list_data.append(stream.readLine().split('|'))

    # def data_cor(self):
    #     for i in range(len(self.list_data)):
    #         self.list_data[i][1]=self.list_data[i][1].split()
    #         self.list_data[i][2]=self.list_data[i][2].split()
    #         self.list_data[i][3]=self.list_data[i][3].split()
    #         self.list_data[i][4]=self.list_data[i][4].split()
    #         self.list_data[i][5] = self.list_data[i][5].split()
