from  PyQt6.QtWidgets import QMainWindow,QTableWidgetItem,QFileDialog
from PyQt6.QtCore import QFile,QTextStream,QIODevice
from prossce import Point,PointCollection,Time
from window import Ui_MainWindow



def open(path):
    file=QFile(path)
    list_data=[]
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件读取失败')
        return
    else:
        stream=QTextStream(file)
        heard = stream.readLine().split()
        time = Time(float(heard[1]),float(heard[2]),float(heard[3])
                    ,float(heard[4]),float(heard[5]),float(heard[6]))
        list_XYZ = PointCollection(time)
        while not stream.atEnd():
            line=stream.readLine()
            patr=line.split()
            a1=Point(patr[0],float(patr[1]),float(patr[2]),float(patr[3]))
            list_data.append(a1)
            list_XYZ.points.append(a1)
    return list_data,list_XYZ


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui=self.setupUi(self)

        self.actionopen.triggered.connect(self.table_write)
        self.actioncount.triggered.connect(self.count)
        self.actionopen.triggered.connect(lambda:self.swhich_page(0))
        self.actioncount.triggered.connect(lambda:self.swhich_page(1))
        self.stackedWidget.setCurrentIndex(0)


    def swhich_page(self,page):
        self.stackedWidget.setCurrentIndex(page)



    def table_write(self):
        fiel_path,_=QFileDialog.getOpenFileName(self,'选择文件','.','txt文件(*.txt)')
        self.list_data,self.list_XYZ=open(fiel_path)


        heards=['卫星标识','x坐标分量','y坐标分量','z坐标分量']

        row=len(self.list_data)
        colum=len(heards)

        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(colum)

        for idx,heard in enumerate(heards):
            item=QTableWidgetItem(heard)
            self.tableWidget.setItem(0,idx,item)

        for idx,heard in enumerate(self.list_data):
            item1 = QTableWidgetItem(heard.n)
            item2 = QTableWidgetItem(str(heard.x/1000))
            item3 = QTableWidgetItem(str(heard.y/1000))
            item4 = QTableWidgetItem(str(heard.z/1000))
            self.tableWidget.setItem(idx+1, 0, item1)
            self.tableWidget.setItem(idx+1, 1, item2)
            self.tableWidget.setItem(idx+1, 2, item3)
            self.tableWidget.setItem(idx+1, 3, item4)

    def count(self):
        data=self.list_XYZ.count_result()
        for i in data:
            self.textBrowser.append(i)



# if __name__=='__main__':
#     list_data,list_XYZ=open('卫星轨道数据.txt')
#     print(list_XYZ.count_result())