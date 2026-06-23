from PyQt6.QtCore import QFile,QIODevice,QTextStream,Qt,QPointF
from PyQt6.QtWidgets import QMainWindow,QWidgetAction,QFileDialog,QLabel,QTableWidgetItem,QLineEdit, QGraphicsPolygonItem
from PyQt6.QtGui import QPen, QColor,QPainter,QPolygonF,QBrush
from PyQt6.QtCharts import QChart,QChartView,QValueAxis,QLineSeries,QScatterSeries
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
        self.statubar_set()
        self.funt_connect()
        self.swicht_page(2)


        self.chart=QChart()
        self.chart.setTitle('66')
        self.chartview=QChartView(self.chart)
        self.chartview.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.horizontalLayout.addWidget(self.chartview)




    def set_chart(self,minx, maxx,miny, maxy,l):

        self.line_series=QLineSeries()
        self.line_series.setName('6666')
        self.point_series=QScatterSeries()


        self.chart.addSeries(self.line_series)
        self.chart.addSeries(self.point_series)




        self.line_series.setColor(QColor(61, 116, 230))
        self.point_series.setColor(QColor(179,11,0))
        self.point_series.setMarkerSize(8)

        self.axis_x=QValueAxis()
        self.axis_y=QValueAxis()

        self.axis_x.setRange(minx, maxx+1)
        self.axis_y.setRange(miny, maxy)
        f1=(math.ceil(maxx-minx)+1)*(1/l)
        f2=(math.ceil(maxy-miny)+1)*(1/l)
        print(f1,f2)
        self.axis_x.setTickCount(int(f1))   # 关键
        self.axis_y.setTickCount(int(f2))

        self.axis_x.setLabelsVisible(False)
        self.axis_y.setLabelsVisible(False)
        self.axis_x.setLineVisible(False)
        self.axis_y.setLineVisible(False)

        pen=QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        self.axis_x.setGridLinePen(pen)
        self.axis_y.setGridLinePen(pen)
        self.axis_x.setMinorGridLineVisible(False)
        self.axis_y.setMinorGridLineVisible(False)

        self.chart.addAxis(self.axis_x,Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)

        self.line_series.attachAxis(self.axis_x)
        self.line_series.attachAxis(self.axis_y)
        self.point_series.attachAxis(self.axis_x)
        self.point_series.attachAxis(self.axis_y)



        w = self.page_painter.width()
        h = self.page_painter.height()


    def funt_connect(self):
        self.action_open.triggered.connect(self.open_data)
        self.action_open.triggered.connect(lambda: self.swicht_page(0))
        self.action_countV.triggered.connect(self.count)
        self.action_countV.triggered.connect(lambda: self.swicht_page(1))
        self.action_save.triggered.connect(self.save_txt)
        self.actionpoint.triggered.connect(lambda: self.swicht_page(2))
        self.actionpoint.triggered.connect(self.count)


    def statubar_set(self):
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
        minx=point[0];maxx=point[1]
        miny=point[2]; maxy=point[3]
        self.clear_all()
        self.set_chart(minx, maxx,miny, maxy,float(self.tool_line_wang.text()))
        self.point_draw(self.pointscllection.stact)


    def save_txt(self):
        file_path, _ = QFileDialog.getSaveFileName(self, '选择文件', '.', 'txt(*.txt)')
        save(file_path,self.re)


    def point_draw(self,stact_point):
        self.line_series.clear()
        for i in stact_point:
            print(float(i.x),float(i.y))
            self.line_series.append(QPointF(float(i.x),float(i.y)))
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












