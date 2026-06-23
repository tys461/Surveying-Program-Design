import math
from PyQt6.QtCore import QFile,QTextStream,QIODevice,Qt,QPointF
from prossce import Point,Pointscllection
from PyQt6.QtWidgets import (QMainWindow,QMessageBox,QLabel,QLineEdit
                    ,QFileDialog,QTableWidgetItem,QGraphicsView)
from PyQt6.QtGui import QPainter,QColor,QPen,QWheelEvent
from PyQt6.QtCharts import QChart,QChartView,QLineSeries,QScatterSeries,QValueAxis
from PyQt6 import QtCharts
from window import Ui_MainWindow
def open(path):
    file=QFile(path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        QMessageBox.information(None,'错误','文件打开失败')
        return
    else:
        stream=QTextStream(file)
        h=float((stream.readLine().split(',')[1]))
        pointscllection=Pointscllection(h)
        while not stream.atEnd():
            line=stream.readLine().split(',')
            if len(line)==4:
                a=Point(line[0],float(line[1]),float(line[2]),float(line[3]))
                pointscllection.lis_points.append(a)
        return pointscllection,h
class CustomChartView(QtCharts.QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def wheelEvent(self, event: QWheelEvent):
        factor = 1.05
        if event.angleDelta().y() > 0:
            self.scale(factor, factor)
        else:
            self.scale(1/factor, 1/factor)
        event.accept()


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialization()



    def initialization(self):

        self.chart = QChart()
        self.chart.setTitle('凸包示意图')
        self.chartview = CustomChartView(self.chart,)
        self.chartview.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.verticalLayout_4.addWidget(self.chartview)


        self.pushButton.clicked.connect(lambda:self.swith(0))
        self.pushButton_2.clicked.connect(lambda:self.swith(1))
        self.pushButton_3.clicked.connect(lambda:self.swith(2))
        self.label1=QLabel('基准高程')
        self.lineEdit1=QLineEdit()
        self.lineEdit1.setMaximumWidth(60)
        self.toolBar.addWidget(self.label1)
        self.toolBar.addWidget(self.lineEdit1)
        self.toolBar.addSeparator()
        self.label2=QLabel('网格间隔')
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setMaximumWidth(60)
        self.toolBar.addWidget(self.label2)
        self.toolBar.addWidget(self.lineEdit2)
        self.stackedWidget.setCurrentIndex(0)
        self.action_open.triggered.connect(self.open_write)
        self.action_count_V.triggered.connect(self.count)
        self.action_count_stact.triggered.connect(self.count)
        self.action_save.triggered.connect(self.save_txt)


    # def set_chart(self,minx, maxx,miny, maxy,l):
    #     self.line_series=QLineSeries()
    #     self.line_series.setName('凸包示意图')
    #     self.point_series=QScatterSeries()
    #     self.point_series.setName('凸包点')
    #
    #     self.chart.addSeries(self.line_series)
    #     self.chart.addSeries(self.point_series)
    #
    #     self.line_series.setColor(QColor(61, 116, 230))
    #     self.point_series.setColor(QColor(179, 11, 0))
    #     self.point_series.setMarkerSize(8)
    #
    #     self.axis_x = QValueAxis()
    #     self.axis_y = QValueAxis()
    #
    #     self.axis_x.setRange(minx, maxx + 1)
    #     self.axis_y.setRange(miny, maxy)
    #     f1 = (math.ceil(maxx - minx) + 1) * (1 / l)
    #     f2 = (math.ceil(maxy - miny) + 1) * (1 / l)
    #     self.axis_x.setTickCount(int(f1))  # 关键
    #     self.axis_y.setTickCount(int(f2))
    #
    #     self.axis_x.setLabelsVisible(False)
    #     self.axis_y.setLabelsVisible(False)
    #     self.axis_x.setLineVisible(False)
    #     self.axis_y.setLineVisible(False)
    #
    #     pen = QPen(QColor(0, 0, 0))
    #     pen.setWidth(1)
    #     self.axis_x.setGridLinePen(pen)
    #     self.axis_y.setGridLinePen(pen)
    #     self.axis_x.setMinorGridLineVisible(False)
    #     self.axis_y.setMinorGridLineVisible(False)
    #
    #     self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
    #     self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
    #
    #     self.line_series.attachAxis(self.axis_x)
    #     self.line_series.attachAxis(self.axis_y)
    #     self.point_series.attachAxis(self.axis_x)
    #     self.point_series.attachAxis(self.axis_y)
    def set_chart(self,minx, maxx,miny, maxy,l):
        self.line_series = QLineSeries()
        self.line_series.setName('凸包示意图')
        self.point_series = QScatterSeries()
        self.point_series.setName('凸包点')

        self.line_series.setColor(QColor(179, 11, 0))
        self.point_series.setMarkerSize(8)
        self.point_series.setColor(QColor(28, 164, 240))

        self.chart.addSeries(self.line_series)
        self.chart.addSeries(self.point_series)

        self.axis_x=QValueAxis()
        self.axis_y=QValueAxis()

        self.axis_x.setRange(minx, maxx)
        self.axis_y.setRange(miny, maxy)
        f1 = (math.ceil(maxx - minx) + 1) * (1 / l)
        f2 = (math.ceil(maxy - miny) + 1) * (1 / l)

        self.axis_x.setTickCount(int(f1))
        self.axis_y.setTickCount(int(f2))

        self.axis_x.setLabelsVisible(False)
        self.axis_y.setLabelsVisible(False)
        self.axis_x.setLineVisible(False)
        self.axis_y.setLineVisible(False)

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        self.axis_x.setGridLinePen(pen)
        self.axis_y.setGridLinePen(pen)
        self.axis_x.setMinorGridLineVisible(False)
        self.axis_y.setMinorGridLineVisible(False)

        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)

        self.line_series.attachAxis(self.axis_x)
        self.line_series.attachAxis(self.axis_y)
        self.point_series.attachAxis(self.axis_x)
        self.point_series.attachAxis(self.axis_y)





    def clear_all(self):
        """
        完全清除图表中的所有系列和坐标轴（适用于自带网格线的场景）
        """
        # 1. 移除所有系列（例如 line_series, point_series 等）
        for series in self.chart.series():
            self.chart.removeSeries(series)
            series.deleteLater()

        # 2. 移除所有坐标轴（X 和 Y 轴）
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)
            axis.deleteLater()

        # 3. 重置成员变量
        self.axis_x = None
        self.axis_y = None
        self.line_series = None
        self.point_series = None

        # 4. 可选：清除图表标题、图例等
        self.chart.setTitle("")
        self.chart.legend().setVisible(True)  # 恢复默认（如果你不需要图例可设为 False）

        # 5. 强制刷新
        self.chart.update()
    def point_draw(self,stact_point):
        self.line_series.clear()
        self.point_series.clear()
        for i in stact_point:
            self.line_series.append(QPointF(float(i.x),float(i.y)))
            self.point_series.append(QPointF(float(i.x),float(i.y)))

    def swith(self,idx):
        self.stackedWidget.setCurrentIndex(idx)

    def open_write(self):
        try:
            file_path,_=QFileDialog.getOpenFileName(self,'选择点文件','.','txt(*.txt)')
            self.pointscllection,h=open(file_path)
            self.lineEdit1.setText(str(h))
            self.lineEdit2.setText('1.0')
            points=self.pointscllection.lis_points
            heards=['点名','X分量（m）','Y分量（m）','Z分量（m）']

            self.H=h

            row=len(points)+1
            colum=len(heards)
            self.tableWidget.setRowCount(row)
            self.tableWidget.setColumnCount(colum)



            for idx,heard in enumerate(heards):
                item=QTableWidgetItem(heard)
                self.tableWidget.setItem(0,idx,item)

            for i in range(len(points)):
                self.tableWidget.setItem(i+1,0, QTableWidgetItem(points[i].n))
                self.tableWidget.setItem(i+1,1, QTableWidgetItem(str(points[i].x)))
                self.tableWidget.setItem(i+1,2, QTableWidgetItem(str(points[i].y)))
                self.tableWidget.setItem(i+1,3, QTableWidgetItem(str(points[i].z)))
        except:
            pass



    def count(self):
        try:
            # self.stackedWidget.setCurrentIndex(1)
            self.chartview.resetTransform()
            self.reuslt,point=self.pointscllection.report(float(self.lineEdit1.text()),float(self.lineEdit2.text()))
            self.textBrowser.append(self.reuslt)
            minx = point[0]
            maxx = point[1]
            miny = point[2]
            maxy = point[3]
            self.clear_all()
            self.set_chart(minx, maxx, miny, maxy, float(self.lineEdit2.text()))
            self.point_draw(self.pointscllection.stact)
            QMessageBox.information(self,'提醒','计算成功')
        except :
            QMessageBox.information(self,'错误','文件还未读取')

    def save_txt(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, '选择文件', '.', 'txt(*.txt)')
            file = QFile(file_path)
            file.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text)
            file.write(self.reuslt.encode('utf-8'))
            QMessageBox.information(self,'提醒','文件保存成功')

        except :
            QMessageBox.information(self,'错误','文件还未读取或进行计算')