import copy
from PyQt6.QtWidgets import QMainWindow,QFileDialog,QTableWidgetItem,QPushButton,QMessageBox
from PyQt6.QtCore import QFile,QTextStream,QIODevice,QPointF,Qt
from PyQt6.QtCharts import QChart,QChartView,QLineSeries,QValueAxis,QScatterSeries
from prossce import Points,Point
from PyQt6.QtGui import QPainter,QColor, QPen
from window import Ui_MainWindow


def open(path):
    points=Points()
    file=QFile(path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件打开失败')
        return
    else:
        stream=QTextStream(file)
        while not stream.atEnd():
            line=stream.readLine().split(',')
            a=Point(line[0],float(line[1]),float(line[2]))
            points.points_lis.append(a)
    return points

class MainWindow(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=self.setupUi(self)
        self.set_action_pushbutton()
        self.set_point()


    def set_point(self):
        self.chart = QChart()
        self.chart.setTitle("曲线插值结果")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)


        self.series_original = QScatterSeries()   # 原始点连线
        self.series_interp = QLineSeries()

        self.chart.addSeries(self.series_original)
        self.chart.addSeries(self.series_interp)
        # 创建一个空的 series，稍后复用
        self.series_original.setName("原始点")
        self.series_original.setColor(QColor(255, 0, 0))  # 红色
        self.series_original.setMarkerSize(8)  # 点的大小（像素）
        # self.series_original.setMarkerShape(QScatterSeries.MarkerShape.Circle)

        pen_interp = QPen(QColor(0, 0, 255))  # 蓝色
        pen_interp.setWidth(1)
        self.series_interp.setPen(pen_interp)
        self.series_interp.setName("插值曲线")

        # 创建坐标轴（占位，后续更新范围）
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series_original.attachAxis(self.axis_x)
        self.series_original.attachAxis(self.axis_y)
        self.series_interp.attachAxis(self.axis_x)
        self.series_interp.attachAxis(self.axis_y)



        # 一开始不显示图表（可以隐藏或放入布局）
        # 将 chart_view 添加到 horizontalLayout_2 中（只需要一次）
        layout = self.horizontalLayout_2
        if layout is not None:
            layout.addWidget(self.chart_view)

    def set_action_pushbutton(self):
        self.action_open.triggered.connect(self.open_write)
        self.action_open.triggered.connect(lambda : self.switch(0))

        self.action_report.triggered.connect(lambda : self.switch(2))
        self.action_data.triggered.connect(lambda : self.switch(0))

        self.pushButton_data.clicked.connect(lambda : self.switch(0))
        self.pushButton_report.clicked.connect(lambda : self.switch(2))


        self.action_point.triggered.connect(lambda : self.switch(1))
        self.pushButton_point.clicked.connect(lambda : self.switch(1))
        self.action_unclose.triggered.connect(self.unclose_count)
        self.action_unclose.triggered.connect(self.point)
        self.action_close.triggered.connect(self.close_count)
        self.action_close.triggered.connect(self.point)



    def switch(self,idx):
        self.stackedWidget.setCurrentIndex(idx)


    def open_write(self):
        filepath,_=QFileDialog.getOpenFileName(self,'打开点文件','.','txt(*.txt)')
        try:
            self.points=open(filepath)
            lis_point=copy.deepcopy(self.points.points_lis)
        except:
            QMessageBox.information(self,'错误','文件读取失败')

        else:
            heards=['点名','x分量（m）','y分量（m）']
            row=len(lis_point)+1
            colum=len(heards)
            self.tableWidget.setRowCount(row)
            self.tableWidget.setColumnCount(colum)


            for idx,hear in enumerate(heards):
                item=QTableWidgetItem(hear)
                self.tableWidget.setItem(0,idx,item)


            for i in range(row-1):
                self.tableWidget.setItem(1+i,0,QTableWidgetItem(lis_point[i].n))
                self.tableWidget.setItem(1+i,1,QTableWidgetItem(str(lis_point[i].x)))
                self.tableWidget.setItem(1+i,2,QTableWidgetItem(str(lis_point[i].y)))

            xs = []
            ys = []
            for i in lis_point:
                x = float(i.x)  # 终点 x
                y = float(i.y)  # 终点 y
                xs.append(x)
                ys.append(y)
                self.series_original.append(QPointF(float(i.x), float(i.y)))
            if xs and ys:
                x_min, x_max = min(xs), max(xs)
                y_min, y_max = min(ys), max(ys)

                x_margin = (x_max - x_min) * 0.1 if x_max != x_min else 1.0
                y_margin = (y_max - y_min) * 0.1 if y_max != y_min else 1.0

                self.axis_x.setRange(x_min - x_margin, x_max + x_margin)
                self.axis_y.setRange(y_min - y_margin, y_max + y_margin)





    def unclose_count(self):
        try:
            re, self.point = self.points.unclosereport()
            self._closed = False  # 标记为不闭合
        except:
            QMessageBox.information(self, '错误', '未读取点文件')
        else:
            self.textBrowser.setText(re)
            QMessageBox.information(self, '提示', '计算不闭合曲线成功')

    def close_count(self):
        try:
            re, self.point = self.points.closereport()
            self._closed = True  # 标记为闭合
        except:
            QMessageBox.information(self, '错误', '未读取点文件')
        else:
            self.textBrowser.setText(re)
            QMessageBox.information(self, '提示', '计算闭合曲线成功')


    def point(self):
        try:
            lis_point = self.point  # 从 closereport 或 unclosereport 获得的数据
            if not lis_point:
                raise ValueError("没有可绘制的曲线数据")

            # 清空 series 中的旧数据
            self.series_interp.clear()
            xs = []
            ys = []
            for pl in lis_point:  # pl 是一段曲线上的离散点列表
                n = 0
                for i in pl:  # i 是 [x0,y0, x1,y1, p0,p1,p2,p3, q0,q1,q2,q3]
                    x = float(i[2])  # 终点 x
                    y = float(i[3])  # 终点 y
                    xs.append(x)
                    ys.append(y)
                    # 添加起点（第一段曲线的起点是原始点）
                    if n == 0:
                        self.series_interp.append(QPointF(float(i[0]), float(i[1])))
                        n = 1
                    # 添加终点
                    self.series_interp.append(QPointF(x, y))

                n = 0  # 重置，为下一段曲线准备

            # 根据新数据更新坐标轴范围
            if xs and ys:
                x_min, x_max = min(xs), max(xs)
                y_min, y_max = min(ys), max(ys)

                x_margin = (x_max - x_min) * 0.1 if x_max != x_min else 1.0
                y_margin = (y_max - y_min) * 0.1 if y_max != y_min else 1.0

                self.axis_x.setRange(x_min - x_margin, x_max + x_margin)
                self.axis_y.setRange(y_min - y_margin, y_max + y_margin)

            # 可选：设置 series 名称（根据闭合/不闭合动态改变）
            # 可以从按钮状态或 points 对象获取
            self.series_interp.setName("闭合曲线" if hasattr(self, '_closed') and self._closed else "不闭合曲线")

        except Exception as e:
            QMessageBox.information(self, '错误', f'绘图失败：{str(e)}')





