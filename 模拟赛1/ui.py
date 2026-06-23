from PyQt6.QtWidgets import QMainWindow,QFileDialog,QMessageBox
from PyQt6.QtCore import QFile,QTextStream,QIODevice
from prossce import Count
from window import Ui_MainWindow

def open(path):
    lis=[]
    file=QFile(path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件打开失败')
    else:
        stream=QTextStream(file)
        while not stream.atEnd():
            lie=stream.readLine().split(',')
            lie=[float(i) for i in lie]
            lis.append(lie)
    l=''
    for i in lis:
        r='-'.join(map(str,i))
        r+='\n'
        l=l+r
    print(l)

    return lis

class MainWindow(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0)
        self.action_open.triggered.connect(self.open_write)
        self.pushButton_2.clicked.connect(lambda : self.swith(0))
        self.pushButton.clicked.connect(lambda : self.swith(1))
        self.pushButton_2.clicked.connect(lambda:self.statusbar.showMessage('原始数据',0))
        self.pushButton.clicked.connect(lambda:self.statusbar.showMessage('计算结果',0))
        self.action_count.triggered.connect(self.count)
        self.action_count.triggered.connect(lambda : self.swith(1))
        self.action_save.triggered.connect(lambda:self.save(self.reuslt1,'reuslt1'))
        self.action_save_result2.triggered.connect(lambda:self.save(self.reuslt2,'reuslt2'))
        self.statusbar.showMessage('就绪',0)

    def swith(self,idx):
        self.stackedWidget.setCurrentIndex(idx)
    def open_write(self):
        try:
            file_path,_=QFileDialog.getOpenFileName(self,'打开','.','txt(*.txt)')
            self.file=open(file_path)
            self.reuslt = Count(self.file)
            r = '------------原始点数据------------\n'
            for i in self.file:
                for k in i:
                    r=r+str(k)+'   '
                r=r+'\n'
            self.textBrowser.setText(r)
            QMessageBox.information(self, '提示', '文件打开成功')
            self.statusbar.showMessage('原始数据',0)
        except:
            QMessageBox.information(self,'错误','文件打开失败')


    def count(self):
        self.textBrowser_2.clear()
        r1 = f'-----------最大值 最小值 平均值-----------\n {self.reuslt.max_min_aver()}'
        r2 = self.reuslt.mean_filtering()
        r3 = self.reuslt.median_filtering()
        self.reuslt1=r1
        self.reuslt2=('-----------中值滤波-----------\n'+r2+
                      '-----------均值滤波-----------\n'+r3)
        self.textBrowser_2.setText(self.reuslt1+self.reuslt2)

    def save(self,r,filename):
        file_path, _ = QFileDialog.getSaveFileName(self, '打开', f'./{filename}.txt', f'txt(*.txt)')
        file = QFile(file_path)
        if not file.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
            print('文件打开失败')
            return
        result = r.encode('utf-8')
        file.write(result)






