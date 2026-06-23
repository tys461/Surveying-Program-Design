import sys
from PyQt6.QtWidgets import (QApplication,QWidget,QFileDialog,
                             QMessageBox,QTableWidgetItem,QHeaderView)
from PyQt6.QtCore import QFile,QTextStream,QIODevice,Qt
from window import Ui_Form

class MyMainWindow(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.ui=self.setupUi(self)

        self.file_open()
        self.data_tablewidet( self.data_lis)


    def file_open(self):
        self.data_lis=[]
        file_path,_=QFileDialog.getOpenFileName(self,'选择文件','.','txt(*.txt)')
        file=QFile(file_path)

        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            QMessageBox.information(self,'错误提示','文件打开失败')
            return

        stream=QTextStream(file)
        while not stream.atEnd():
            line=stream.readLine()
            part=line.split(',,')
            self.data_lis.append(part)
        return self.data_lis

    def data_tablewidet(self,data_lis):
        headers=['点号','X坐标','Y坐标','Y通用坐标']

        total_rows=len(data_lis)+2
        total_cols=len(headers)

        self.tableWidget.setRowCount(total_rows)
        self.tableWidget.setColumnCount(total_cols)

        self.tableWidget.setSpan(0,0,1,total_cols)
        title_item=QTableWidgetItem('坐标数据')
        title_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        font=title_item.font()
        font.setPixelSize(15)
        font.setBold(True)
        title_item.setFont(font)
        self.tableWidget.setItem(0,0,title_item)


        for col,header in enumerate(headers):
            item=QTableWidgetItem(header)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableWidget.setItem(1,col,item)


        for row,row_data in enumerate(data_lis):
            for col,vale in enumerate(row_data):
                item = QTableWidgetItem(str(vale))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(row+2,col,item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)



    def addact(self):
        '''在菜单栏添加action'''
        before_action = self.menu_3.menuAction() # 关键：获取菜单的代表动作
        self.action_huan=QAction('邻带换算',self)
        self.action_report=QAction('报告',self)
        self.action_jie=QAction('解算',self)
        self.menubar.insertAction(before_action,self.action_jie)
        self.menubar.addAction(self.action_huan)
        self.menubar.addAction(self.action_report)


if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MyMainWindow()
    window.show()
    sys.exit(app.exec())
