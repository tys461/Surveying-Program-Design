import sys
from PyQt6 import QtWidgets, QtCore, QtGui, QtCharts

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtChart 缩放示例")
        self.resize(800, 600)

        # 1. 创建图表
        chart = QtCharts.QChart()
        chart.setTitle("可缩放的折线图")

        # 2. 创建数据序列 (正弦波示例)
        series = QtCharts.QLineSeries()
        for x in range(0, 100):
            y = 50 + 30 * (x / 100)
            series.append(x, y)
        chart.addSeries(series)
        chart.createDefaultAxes()

        # 3. 创建自定义的 ChartView
        chart_view = CustomChartView(chart)
        self.setCentralWidget(chart_view)

class CustomChartView(QtCharts.QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        # 启用矩形框选缩放
        self.setRubberBand(QtCharts.QChartView.RubberBand.RectangleRubberBand)
        # 可选：设置抗锯齿，让图表更好看
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        # 自定义滚轮缩放，放大/缩小 5%
        factor = 1.05
        if event.angleDelta().y() > 0:
            self.chart().zoom(factor)
        else:
            self.chart().zoom(1 / factor)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
