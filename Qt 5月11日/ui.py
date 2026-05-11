from PyQt6.QtCore import QFile,QIODevice,QTextStream

class Open ():
    def __init__(self):
        self.data_list=[]

    def open_data_(self):
        file = QFile('bhl1.txt')
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            print("打开文件失败:", file.errorString())
            # return
        print('文件打开成功，内容如下：')
        a=[]
        while not file.atEnd():
            line = file.readLine()
            a.append(float(line.data().decode('utf-8').strip()))

        self.data_list=[a[i:i+9] for i in range(0,len(a),9)]
        print(self.data_list)
        return self.data_list
a=Open()
a.open_data_()