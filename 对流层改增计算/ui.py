from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QFileDialog
from PyQt6.QtCore import QFile, QIODevice, QTextStream
from window import Ui_MainWindow
from prossce import *


def open(path):
    file = QFile(path)
    lis_points = PointCllection()
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件读取失败')
        return
    else:
        stream = QTextStream(file)
        heard = stream.readLine().split(',')
        while not stream.atEnd():
            line = stream.readLine().split(',')
            print(int(line[1]))
            a = Point(line[0], line[1], float(line[2]), float(line[3]), float(line[4]), float(line[5]))
            lis_points.lis_point.append(a)
        return lis_points, heard


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0)
        self.statusbar.showMessage('就绪', 5)
        self.actionopen.triggered.connect(self.open_write)
        self.actionopen.triggered.connect(lambda: self.swich_page(0))
        self.actioncount.triggered.connect(self.count_write)
        self.actioncount.triggered.connect(lambda: self.swich_page(1))
        self.pushButton.clicked.connect(lambda: self.swich_page(0))
        self.pushButton_2.clicked.connect(lambda: self.swich_page(1))
        self.actionsave.triggered.connect(self.save)

    def swich_page(self, idx):
        self.stackedWidget.setCurrentIndex(idx)

    def open_write(self):
        path, _ = QFileDialog.getOpenFileName(self, '打开原始数据', '.', 'txt(*.txt)')
        self.points, self.heards = open(path)
        self.lis_points = self.points.lis_point
        row = len(self.lis_points)
        colum = len(self.heards)

        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(colum)

        for idx, heard in enumerate(self.heards):
            item = QTableWidgetItem(heard)
            self.tableWidget.setItem(0, idx, item)

        for idx, point in enumerate(self.lis_points):
            row = idx + 1
            self.tableWidget.setItem(row, 0, QTableWidgetItem(point.n))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(point.t))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(point.x)))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(point.y)))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(point.h)))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(str(point.d)))
        self.statusbar.showMessage('文件读取成功', 5000)

    def save(self):
        path, _ = QFileDialog.getSaveFileName(self, '保存', '.', 'txt(*.txt)')
        file = QFile(path)

        if not file.open(QIODevice.OpenModeFlag.WriteOnly):
            print('保存失败')
            return
        file.write(self.text.encode('utf-8'))

    def count_write(self):
        report = self.points.count()
        header = f"{'测站名':<10} {'高度角':<8} {'ZHD':<12} {'m_d(E)':<12} {'ZWD':<10} {'m_w(E)':<12} {'延迟改正':<14}"
        self.textBrowser.append(header)
        for i in report:
            self.textBrowser.append(i)

        self.text = self.textBrowser.toPlainText()
