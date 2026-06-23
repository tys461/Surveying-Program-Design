import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QPointF,QFile,QTextStream,QIODevice,QMargins
from PyQt6.QtGui import QPainter
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from mywindow import Ui_Form





class mainwindow(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()

        self.ui=self.setupUi(self)
        self.open()
        self.chart_vi()


    def open(self):
        self.lis_point=[]
        file=QFile('测试数据.txt')
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            print('错误')
            return
        else:
            stream=QTextStream(file)
            while not stream.atEnd():
                part=stream.readLine().split(',')
                self.lis_point.append([float(part[1]),float(part[2])])

    from PyQt6.QtCore import Qt, QPointF, QFile, QTextStream, QIODevice, QMargins  # 添加 QMargins

    # ... 其他代码保持不变

    def chart_vi(self):
        lis_point = self.lis_point[0::]
        series = QLineSeries()
        xs = []  # 用于存储所有X值
        ys = []  # 用于存储所有Y值
        for i in lis_point:
            x = float(i[0])
            y = float(i[1])
            xs.append(x)
            ys.append(y)
            series.append(QPointF(x, y))
        series.setName('point——data')

        # 计算数据的范围
        x_min = min(xs)
        x_max = max(xs)
        y_min = min(ys)
        y_max = max(ys)

        # 扩展范围，留出边距（例如扩展 5%）
        x_margin = (x_max - x_min) * 0.05
        y_margin = (y_max - y_min) * 0.05
        # 特殊情况：如果所有数据点相同，避免零扩展
        if x_margin == 0:
            x_margin = 1.0
        if y_margin == 0:
            y_margin = 1.0

        new_x_min = x_min - x_margin
        new_x_max = x_max + x_margin
        new_y_min = y_min - y_margin
        new_y_max = y_max + y_margin

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Simple Line Chart')
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        axis_x = QValueAxis()
        axis_y = QValueAxis()
        axis_x.setRange(new_x_min, new_x_max)
        axis_y.setRange(new_y_min, new_y_max)

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = self.horizontalLayout
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            layout.addWidget(chart_view)

if __name__=='__main__':
    app = QApplication(sys.argv)
    mywindow = mainwindow()
    w = mywindow.show()
    sys.exit(app.exec())