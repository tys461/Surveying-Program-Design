from untitled import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow,QFileDialog,QMessageBox,QComboBox
from PyQt6.QtCore import Qt,QAbstractTableModel,QModelIndex,QFile, QIODevice, QTextStream,QStringConverter,QPointF
from PyQt6.QtCharts import QChart,QChartView,QLineSeries,QValueAxis
from PyQt6.QtGui import QPainter
import processor


class FileDataModel(QAbstractTableModel):
    def __init__(self,filename):
        super().__init__()
        self._data=[]
        self._headers=['序号','x坐标','y坐标']
        self._load_file(filename)


    def _load_file(self,filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(',')
                    if len(parts) == 3:
                        # 保持原始数据为字符串，也可转为数字
                        self._data.append([parts[0], parts[1], parts[2]])
        except FileNotFoundError:
            self._data = [["文件未找到", filename, "请检查路径"]]

    def rowCount(self,parent=QModelIndex()):
        return len(self._data)

    def columnCount(self,parent=QModelIndex()):
        return len(self._headers)

    def data(self,index,role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid:
            return None
        if role==Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        # 垂直表头显示行号（从1开始）
        return str(section + 1)

    def get_data(self):
        """返回原始数据（列表的副本或直接引用）"""
        return self._data

class MyWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui=self.setupUi(self)
        self.data=[]

        self.action_add()
        self.combo = QComboBox()
        items = {"50m": 50, "80m": 80, "100m": 100}
        for text, value in items.items():
            self.combo.addItem(text, value)
        self.toolBar.insertWidget(self.actionData, self.combo)



    def action_add(self):
        self.action.triggered.connect(self.open_file)
        self.action.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.actioninput.triggered.connect(self.save_file)
        self.actioninput.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.actionCOUNT.triggered.connect(self.count)
        self.actionCOUNT.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.actionData.triggered.connect(self.data_show)
        self.actionData.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.actionchart.triggered.connect(self.data_chart)
        self.actionchart.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(4))





    def open_file(self):
        self._opne_file=QFileDialog.getOpenFileName(self,'选择数据文件','.','txt文件(*.txt)')
        self.model = FileDataModel(self._opne_file[0])
        self.label_open.setText(f'{self._opne_file[0]}')
        self.tableView_open.setModel(self.model)


    def save_file(self):
        if self.data:
            print(self.data)
            print('sdf')
        else:
            QMessageBox.warning(self, '错误', '你没有进行计算')
            return None
        file = QFile("output.txt")
        if file.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(file)
            # 推荐：设置编码为UTF-8，解决中文乱码问题
            stream.setEncoding(QStringConverter.Encoding.Utf8)
            stream << "-----------------\n"  # 使用流操作符 << 写入
            for i in self.data:
                stream << f"{i[0]} {i[1]} {i[2]}\n"
            file.close()
            self.textBrowser_save.append('---------写入成功------------')
        else:
            print("打开文件失败")


    def count(self):
        try:
            print(99)
            point=self.model.get_data()
            self.data = processor.dadt_processor(point,self.combo.currentData())
        except:
            QMessageBox.warning(self,'错误','你没有打开原始文件')
        else:
            self.textBrowser_count.clear()
            self.textBrowser_count.append('---------计算成功------------')
            for i in self.data:
                # self.textBrowser_count.append(str(i))
                self.textBrowser_count.append(f'{i[0]} {i[1]} {i[2]}')
                self.textBrowser_count.verticalScrollBar().setValue(0)


    def data_show(self):
        try:
            self.tableView_data.setModel(self.model)
            self.statusBar.showMessage(self._opne_file[0],0)
        except:
            QMessageBox.warning(self, '错误', '你没有打开原始文件')
            self.statusBar.clearMessage()


    def data_chart(self):
        # 1.创建数据序列
        series = QLineSeries()
        for i in self.data:
            series.append(QPointF(float(i[1]), float(i[2])))
        series.setName('My Data')

        # 2.创建图表
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Simple Line Chart')
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # 3.创建坐标轴
        axis_x = QValueAxis()
        axis_y = QValueAxis()
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignBottom)
        # 将序列附加到坐标轴上
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        # 4.创建图表视图
        # 在“actionData”动作前插入组合框
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        layout = self.page_chart.layout()  # 获取水平布局
        if layout is not None:
            # 清除布局内原有的控件（避免重复添加）
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            layout.addWidget(chart_view)



