import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtCharts import QChart, QChartView, QValueAxis
from PyQt6.QtGui import QPainter, QPen, QColor
from window import Ui_Form

class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.chart = QChart()
        self.chart.setTitle("50x50 格网 (边长2)")

        axis_x = QValueAxis()
        axis_y = QValueAxis()
        axis_x.setRange(0, 100)
        axis_y.setRange(0, 100)
        axis_x.setTickCount(51)   # 0,2,4,...,100
        axis_y.setTickCount(51)

        # 可选：隐藏刻度标签和轴线
        axis_x.setLabelsVisible(False)
        axis_y.setLabelsVisible(False)
        axis_x.setLineVisible(False)
        axis_y.setLineVisible(False)

        # 网格线样式
        pen = QPen(QColor(180, 180, 180))
        pen.setWidth(1)
        axis_x.setGridLinePen(pen)
        axis_y.setGridLinePen(pen)
        axis_x.setMinorGridLineVisible(False)
        axis_y.setMinorGridLineVisible(False)

        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        self.chartview = QChartView(self.chart)
        self.chartview.setFixedSize(600, 600)
        self.chartview.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.horizontalLayout.addWidget(self.chartview)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())