from PyQt6.QtWidgets import QApplication , QWidget,QMainWindow,QFileDialog
from PyQt6.QtCore import QFile,QTextStream,QIODevice
from mainui import Ui_MainWindow
from report import Ui_Form
from prossce import cuont





def wirte(data):
    file = QFile('C012唐思远.txt')
    if not file.open(QIODevice.OpenModeFlag.WriteOnly ):
        print("读取失败")

    else:
        num=1
        print(len(data))
        for i in data:
            file.write((f'------------（{num}）------------\n').encode('utf-8'))
            if type(i) == list:
                for a in i :
                    file.write(a.encode('utf-8')+'\n'.encode('utf-8'))
            else:
                file.write(i.encode('utf-8') + '\n'.encode('utf-8'))
            num+=1


class ReportUi(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.ui=self.setupUi(self)



class MymainWindow(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=self.setupUi(self)

        self.actionopen.triggered.connect(self.open_data)
        self.actioncount.triggered.connect(self.coun)
        # self.actionreport.triggered.connect(self.report)

    def open_data(self):
        file_path,_=QFileDialog.getOpenFileName(self,'open','.','(*.txt)')
        self.lis_data = []
        file = QFile(file_path)

        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            print("读取失败")
        else:
            self.textBrowser.append('--------点号--------经度--------纬度--------')
            stream = QTextStream(file)
            while not stream.atEnd():
                line = stream.readLine()
                self.textBrowser.append(line)
                part = line.split(',')
                # print(part)
                self.lis_data.append([int(part[0]), float(part[1]), float(part[2])])


    def coun(self):
        # print(self.lis_data)
        result=cuont(self.lis_data)
        self.textBrowser.clear()
        # print(result)
        self.textBrowser.append('-------计算结果----------')
        for i in result:
            if type(i) == list:
                for a in i:
                    self.textBrowser.append(a)
            else:
                self.textBrowser.append(i)











