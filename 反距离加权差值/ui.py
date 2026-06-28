from PyQt6.QtWidgets import QMainWindow,QFileDialog,QMessageBox,QTableWidgetItem
from PyQt6.QtCore import QFile,QTextStream,QIODevice
from window import Ui_MainWindow
from prossce import Count

class Point:
    def __init__(self,idx,x,y,z):
        self.idx=idx
        self.x=float(x)
        self.y=float(y)
        self.z=float(z)


def open_file(path):
    lis_point=[]
    file=QFile(path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('读取失败')
        return
    else:
        stream=QTextStream(file)
        while not stream.atEnd():
            line=stream.readLine()
            part=line.split(',')
            point=Point(part[0],part[1],part[2],part[3])
            lis_point.append(point)
        return lis_point

def save_result(path,data):
    file = QFile(path)
    if not file.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
        print('读取失败')
        return
    else:
        file.write(data.encode('utf-8'))




class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui=self.setupUi(self)
        self.resutl =''
        self.statusbar.showMessage('就绪',0)


        self.actionopen.triggered.connect(lambda:self.switch_page(0))
        self.actioncount.triggered.connect(lambda:self.switch_page(1))
        self.stackedWidget.setCurrentIndex(0)
        self.actionopen.triggered.connect(self.open)
        self.actioncount.triggered.connect(self.coun)
        self.actionsave.triggered.connect(self.save)
        self.pushButton_data.clicked.connect(lambda:self.switch_page(0))
        self.pushButtoncount.clicked.connect(lambda:self.switch_page(1))




    def write_table(self):
        heards=['点名','x(m)','y(m)','z(m)']
        row=len(self.lis_point)+1
        colum=len(heards)

        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(colum)

        for idx , heard in enumerate(heards):
            item=QTableWidgetItem(heard)
            self.tableWidget.setItem(0,idx,item)

        for idx , point in enumerate(self.lis_point):
            item1=QTableWidgetItem(point.idx)
            item2=QTableWidgetItem(str(point.x))
            item3=QTableWidgetItem(str(point.y))
            item4=QTableWidgetItem(str(point.z))
            self.tableWidget.setItem(idx+1,0,item1)
            self.tableWidget.setItem(idx+1,1,item2)
            self.tableWidget.setItem(idx+1,2,item3)
            self.tableWidget.setItem(idx+1,3,item4)

    def switch_page(self, index):
        # 核心切换逻辑
        self.stackedWidget.setCurrentIndex(index)
    def open(self):
        file_path,_=QFileDialog.getOpenFileName(self,'open','.','txt文件(*.txt)')
        self.lis_point=open_file(file_path)
        self.write_table()
        self.statusbar.showMessage(f'读取文件{file_path}',5000)


    def save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'open', '.', 'txt文件(*.txt)')
        save_result(file_path,self.resutl)

    def coun(self):
        Q1=Count('Q1',4310,3600)
        Q2=Count('Q2',4330,3600)
        Q3=Count('Q3',4310,3620)
        Q4=Count('Q4',4330,3620)
        Q1_r=Q1.count(self.lis_point)
        Q2_r=Q2.count(self.lis_point)
        Q3_r=Q3.count(self.lis_point)
        Q4_r=Q4.count(self.lis_point)
        self.resutl=f'点名 X(m) Y(m) H(m) 参与插值的点列表\n{Q1_r}\n{Q2_r}\n{Q3_r}\n{Q4_r}\n'
        # QMessageBox.information(self,'0',self.resutl)
        self.textBrowser.setText(self.resutl)


