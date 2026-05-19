import sys
from PyQt6.QtWidgets import QApplication,QMainWindow
from PyQt6.QtCharts import QChart,QChartView,QLineSeries,QValueAxis
from PyQt6.QtCore import QFile,QIODevice,QByteArray,QPointF,Qt
from PyQt6.QtGui import QPainter



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyQt6 Chart')
        self.setGeometry(100,100,800,600)
        self.a=self.point_add()

        #1.创建数据序列
        series=QLineSeries()
        for i in self.point_add():
            series.append(QPointF(i[1],i[2]))
        series.setName('My Data')

        #2.创建图表
        chart=QChart()
        chart.addSeries(series)
        chart.setTitle('Simple Line Chart')
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        #3.创建坐标轴
        axis_x=QValueAxis()
        axis_y=QValueAxis()
        chart.addAxis(axis_x,Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y,Qt.AlignmentFlag.AlignLeft)
        #将序列附加到坐标轴上
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        #4.创建图表视图
        chart_view=QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)#抗锯齿更平滑
        self.setCentralWidget(chart_view)




    def point_add(self):
        data=[]
        file = QFile('压缩计算结果输出.txt')
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            print("打开文件失败:", file.errorString())
            return
        print('文件打开成功，内容如下：')
        while not file.atEnd():
            line = file.readLine()  # 直接返回 QByteArray，无需再包装
            a=line.data().decode('utf-8').strip().split(',')
            n=int(a[0])
            x=float(a[1])
            y=float(a[2])
            data.append([n,x,y])
        return data








if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MainWindow()
    window.point_add()
    window.show()
    #
    sys.exit(app.exec())