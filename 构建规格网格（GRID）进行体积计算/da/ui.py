from PyQt6.QtCore import QFile,QIODevice,QTextStream,Qt, QRectF, QPointF
from PyQt6.QtWidgets import (QMainWindow,QWidgetAction,QFileDialog,QLabel,QTableWidgetItem,QLineEdit
,QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsTextItem)
from PyQt6.QtGui import QPen, QBrush, QColor, QPolygonF,QPainter
from window import Ui_MainWindow
from prossce import*
import math

def open(path):
    file=QFile(path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件读取失败')
        return
    else:
        stream=QTextStream(file)
        h=float(stream.readLine().split(',')[1])
        pointscllection = Pointscllection(h)
        while not stream.atEnd():
            line=stream.readLine().split(',')
            if len(line)==4:
                a=Point(line[0],float(line[1]),float(line[2]),float(line[3]))
                pointscllection.lis_points.append(a)
        return pointscllection,h

def save(path,r):
    file = QFile(path)
    if not file.open(QIODevice.OpenModeFlag.WriteOnly):
        print('文件保存失败')
    else:
        file.write(r.encode('utf-8'))


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui=self.setupUi(self)
        self.addaction()

        self.action_open.triggered.connect(self.open_data)
        self.action_open.triggered.connect(lambda:self.swicht_page(0))
        self.action_countV.triggered.connect(self.count)
        self.action_countV.triggered.connect(lambda:self.swicht_page(1))
        self.action_save.triggered.connect(self.save_txt)

        self.left_label = QLabel("数据表格 凸包图形 报告")
        self.center_label = QLabel("目前状态")
        self.statusbar.addWidget(self.left_label, 1)  # stretch=1 让它尽量靠左
        self.statusbar.addWidget(self.center_label, 1)  # stretch=1 让它尽量居中

    def addaction(self):
        self.tool_label_ji=QLabel("基准高程(m):")
        self.tool_label_ji.setToolTip('基准高程(m):')
        self.toolBar.addWidget(self.tool_label_ji)
        self.tool_line_ji=QLineEdit()
        self.tool_line_ji.setMaximumWidth(60)
        self.toolBar.addWidget(self.tool_line_ji)
        self.toolBar.addSeparator()
        self.tool_label_wang=QLabel("网格间隔(m):")
        self.tool_label_wang.setToolTip('网格间隔(m):')
        self.toolBar.addWidget(self.tool_label_wang)
        self.tool_line_wang=QLineEdit()
        self.tool_line_wang.setMaximumWidth(60)
        self.tool_line_wang.setText('1')
        self.toolBar.addWidget(self.tool_line_wang)

    def swicht_page(self,idx):
        self.stackedWidget.setCurrentIndex(idx)

    def open_data(self):
        file_path,_=QFileDialog.getOpenFileName(self,'选择文件','.','txt(*.txt)')
        self.pointscllection,h=open(file_path)
        lis_points=self.pointscllection.lis_points
        heards=['点名','x分量','y分量','h分量']



        row=len(lis_points)
        colum=len(heards)

        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(colum)

        for idx,heard in enumerate(heards):
            item=QTableWidgetItem(heard)
            self.tableWidget.setItem(0,idx,item)

        for i in range(len(lis_points)):
            self.tableWidget.setItem(i+1, 0, QTableWidgetItem(lis_points[i].n))
            self.tableWidget.setItem(i+1, 1, QTableWidgetItem(str(lis_points[i].x)))
            self.tableWidget.setItem(i+1, 2, QTableWidgetItem(str(lis_points[i].y)))
            self.tableWidget.setItem(i+1, 3, QTableWidgetItem(str(lis_points[i].z)))
        self.tool_line_ji.setText(f'{h}')
        self.center_label.setText('目前状态:导入数据')

    def count(self):
        self.re,point=self.pointscllection.report(float(self.tool_line_ji.text()),float(self.tool_line_wang.text()))
        self.textBrowser.setText(self.re)


    def save_txt(self):
        file_path, _ = QFileDialog.getSaveFileName(self, '选择文件', '.', 'txt(*.txt)')
        save(file_path,self.re)











