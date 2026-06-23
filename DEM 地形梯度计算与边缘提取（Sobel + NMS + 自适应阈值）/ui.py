import os
from PyQt6.QtCore import QFile, QIODevice, QTextStream
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt6.QtGui import QFont
from window import Ui_MainWindow
from prossce import MyMatrix


def open(path):
    file = QFile(path)
    lis_data = []
    try:
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            print('文件打开失败')
            return
        else:
            try:
                stream = QTextStream(file)
                while not stream.atEnd():
                    part = stream.readLine().split()
                    lis_data.append(part)
                return lis_data
            except:
                print('文件格式有误')
    except:
        print('文件打开失败')


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        font = QFont("黑体", 9)  # 或 "Courier New", "Liberation Mono"
        # font.setBold(True)
        self.textBrowser_report.setFont(font)
        self.textBrowser_data.setFont(font)
        self.statusbar.showMessage('就绪', 0)
        self.conncet_action()

    def conncet_action(self):
        self.action_open.triggered.connect(self.open_file)
        self.action_about.triggered.connect(self.about_func)
        self.action_help.triggered.connect(self.help_func)
        self.action_count.triggered.connect(self.count)
        self.action_save.triggered.connect(self.save_report)
        self.tabWidget.currentChanged.connect(self.on_tab_changed)
        self.action_close.triggered.connect(self.close)

    def on_tab_changed(self, index):
        # 假设 tab_data 索引为 0，tab_report 索引为 1（根据实际 UI 文件中的顺序）
        if index == 0:  # 数据标签页
            if hasattr(self, 'matrix') and self.matrix is not None:
                self.statusbar.showMessage('当前状态: 原始文件数据', 0)
            else:
                self.statusbar.showMessage('当前状态: 未加载矩阵数据', 0)
        elif index == 1:  # 报告标签页
            if self.textBrowser_report.toPlainText().strip():
                self.statusbar.showMessage('当前状态: 计算结果', 0)
            else:
                self.statusbar.showMessage('当前状态: 尚未计算', 0)
        else:
            # 如果有其他标签页，可扩展
            self.statusbar.showMessage('就绪', 0)

    def set_open(self, tip, tile):
        QMessageBox.information(self, '提示', f'{tip}')
        file_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '.', 'txt(*.txt)')
        data = open(file_path)
        try:
            output = "\n".join(" ".join(f'{cell:>6}' for cell in row) for row in data)
            self.textBrowser_data.append(f'________________{tile}________________\n')
            self.textBrowser_data.append(output)
            return data
        except Exception as e:
            QMessageBox.information(self, '错误', f'文件打开失败\n{e}')

    def open_file(self):
        self.textBrowser_data.clear()
        self.tabWidget.setCurrentWidget(self.tab_data)

        matrix_data = self.set_open('请选择矩阵文件', '待处理矩阵')
        if matrix_data == None:
            return

        core_x = self.set_open('请选择核矩阵文件（X）', '核矩阵（X）')
        if core_x == None:
            return

        core_y = self.set_open('请选择核矩阵文件（Y）', '核矩阵（Y）')
        if core_x == None:
            return

        try:
            self.matrix = MyMatrix(core_x, core_y, matrix_data)
        except Exception as e:
            ...

        self.statusbar.showMessage('当前状态:   原始文件数据', 0)

    def set_report(self, tile, data):
        self.textBrowser_report.append(f'________________{tile}________________\n')
        output = "\n".join(" ".join(f'{cell:>6}' for cell in row) for row in data)
        self.textBrowser_report.append(output)

    def count(self):
        self.textBrowser_report.clear()
        try:
            value_repair = self.matrix.missing_value_repair()
            self.set_report('修复后矩阵', value_repair)

            gradient_count, gradient_degree = self.matrix.calculate_gradient_amplitude(value_repair)
            self.set_report('梯度幅值M', gradient_count)
            self.set_report('梯度方向θ', gradient_degree)

            suppression_gradient_degree = self.matrix.non_maximum_suppression(gradient_degree)
            self.set_report('非极大值抑制', suppression_gradient_degree)

            threshold_segmentation = self.matrix.adaptive_threshold_segmentation(suppression_gradient_degree)
            self.set_report('自适应阈值分割', threshold_segmentation)

            self.tabWidget.setCurrentWidget(self.tab_report)
            QMessageBox.information(self, '提醒', f'计算成功')
            self.statusbar.showMessage('当前状态:    计算结果', 0)

        except Exception as e:
            QMessageBox.information(self, '错误', f'计算失败,你还未加载矩阵\n{e}')

    def save_report(self):
        if self.textBrowser_report.toPlainText() == '':
            QMessageBox.information(self, '错误', '你还未进行计算')
        else:
            save_path, _ = QFileDialog.getSaveFileName(self, '选择保存路径', r'.\reuslt', 'txt(*.txt)')
            file = QFile(save_path)
            if not file.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
                QMessageBox.information(self, '错误', '文件路径有误保存失败')
                return
            else:
                try:
                    file.write(self.textBrowser_report.toPlainText().encode('utf-8'))
                except Exception as e:
                    QMessageBox.information(self, '错误', f'文件保存失败\n{e}')

    def about_func(self):
        QMessageBox.about(self, "关于我的应用",
                          """
                          <h2>DEM 地形梯度计算与边缘提取（Sobel + NMS + 自适应阈值）</h2>
                          <p>版本 1.0.0</p>
                          <p>一个用 PyQt6 构建的应用</p>
                          <p> 2026 测绘技能大赛</p>
                          """
                          )

    def help_func(self):
        try:
            os.startfile('')
        except:
            ...
