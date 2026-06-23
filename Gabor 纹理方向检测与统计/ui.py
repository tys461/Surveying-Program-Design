import os
from PyQt6.QtCore import QFile, QTextStream, QIODevice
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt6.QtGui import  QFont
from window import Ui_MainWindow
from prossce import MyMatrix

def open(path):
    """矩阵读取函数"""
    file = QFile(path)
    lis_matrix = []
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        return
    else:
        try:
            stream = QTextStream(file)
            while not stream.atEnd():
                part = stream.readLine().split()

                lis_matrix.append([float(i) for i in part])
            return lis_matrix
        except:
            return


class MyMianWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_font()
        self.action_conncet()
        self.statusbar.showMessage('就绪！',0)
        self.m=''

    """将初始化内容封装成函数 美观def __init__(self):下的内容"""

    def action_conncet(self):
        """初始化：按键连接函数"""
        self.action_open.triggered.connect(self.open_write)
        self.action_Gabor.triggered.connect(lambda: self.calculate_the_Gabor_filter_response('Gabor 滤波器响应'))
        self.action_NMS.triggered.connect(lambda: self.nms_extracts_peak_responses_ui('非极大值抑制（NMS）'))
        self.action_Direction.triggered.connect(lambda: self.directional_response_statistics_ui('方向响应统计'))
        self.action_count.triggered.connect(self.count_all)
        self.action_save.triggered.connect(self.save_write)
        self.tabWidget.currentChanged.connect(self.tab_changed)
        self.action_about.triggered.connect(self.about)
        self.action.triggered.connect(self.close)
        self.action_help.triggered.connect(self.help)

    def set_font(self):
        """初始化：textBrowser的字体"""
        font = QFont("黑体", 4)
        self.textBrowser_report.setFont(font)
        self.textBrowser_data.setFont(font)

    def tab_changed(self,index):
        """初始化：设置状态栏"""
        if index==0:
            if hasattr(self, 'my_matrix') and self.my_matrix is not None:
                self.statusbar.showMessage('当前状态：矩阵文件', 0)
            else:
                self.statusbar.showMessage('当前状态：尚未读取矩阵文件', 0)

        else:
            if self.textBrowser_report.toPlainText().split():
                self.statusbar.showMessage(self.m, 0)
            else:
                self.statusbar.showMessage('当前状态：尚未计算', 0)

    def open_write(self):
        """矩阵读取函数"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, '选择矩阵文件', '.\data', 'txt(*.txt)')
            lis_matrix = open(file_path)

            self.tabWidget.setCurrentWidget(self.tab)
            self.textBrowser_data.clear()
            output = '\n'.join(' '.join(f'{i:>8.1f}' for i in row) for row in lis_matrix)
            self.textBrowser_data.append('----------------矩阵数据----------------')
            self.textBrowser_data.append(output)
            self.my_matrix = MyMatrix(lis_matrix)
            QMessageBox.information(self, '提示', f'文件打开成功')
            self.statusbar.showMessage('当前状态：矩阵文件',0)
        except ValueError as e:
            QMessageBox.critical(self, '错误', f'文件读取失败\n\n{e}')
        except TypeError as e:
            QMessageBox.critical(self, '错误', f'文件读取失败\n\n{e}')

    def save_write(self):
        """保存计算文件"""
        if self.textBrowser_report.toPlainText() :
            QMessageBox.information(self, '提示', f'保存结果为当前计算结果')
            try:
                file_path, _ = QFileDialog.getSaveFileName(self, '选择矩阵文件', r'.\result', 'txt(*.txt)')
                if file_path=='':
                    QMessageBox.critical(self, '错误', '文件保存失败')
                    return
                file=QFile(file_path)
                file.open(QIODevice.OpenModeFlag.WriteOnly)
                file.write(self.textBrowser_report.toPlainText().encode('utf-8'))
                QMessageBox.information(self, '提示', f'文件保存成功')

            except:
                QMessageBox.critical(self,'错误','文件保存失败')
        else:
            QMessageBox.warning(self, '错误', '你还未进行计算')

    def calculate_the_Gabor_filter_response(self, tile):
        """计算并输出结果"""
        if hasattr(self, 'my_matrix'):
            try:
                self.textBrowser_report.setFont(QFont('黑体', 5))
                gabor_core_real_0 = self.my_matrix.set_fabor_15x15_real(0)
                gabor_core_false_0 = self.my_matrix.set_fabor_15x15_false(0)
                reuslt = self.my_matrix.convolutional_calculation_all(gabor_core_real_0, gabor_core_false_0)
                self.textBrowser_report.clear()
                output = '\n'.join(' '.join(f'{i:>8.1f}' for i in row) for row in reuslt)
                self.textBrowser_report.append(f'----------------{tile}----------------')
                self.textBrowser_report.append(output)
                self.tabWidget.setCurrentWidget(self.tab_2)
                QMessageBox.information(self, '提示', f'{tile}计算成功')
                self.statusbar.showMessage(f'当前状态：{tile}计算报告',0)
                self.m=self.statusbar.currentMessage()

            except ValueError as e:
                QMessageBox.critical(self, '错误', f'计算失败\n\n{e}')
        else:
            QMessageBox.warning(self, '错误', '你还没有读取文件')

    def nms_extracts_peak_responses_ui(self, tile):
        """计算非极大值抑制（NMS）提取响应峰值并输出结果"""
        if hasattr(self, 'my_matrix'):
            try:
                self.textBrowser_report.setFont(QFont('黑体', 5))
                reuslt = self.my_matrix.nms_extracts_peak_responses()
                self.textBrowser_report.clear()
                output = '\n'.join(' '.join(f'{i:>8.1f}' for i in row) for row in reuslt)
                self.textBrowser_report.append(f'----------------{tile}----------------')
                self.textBrowser_report.append(output)
                self.tabWidget.setCurrentWidget(self.tab_2)
                QMessageBox.information(self, '提示', f'{tile}计算成功')
                self.statusbar.showMessage(f'当前状态：{tile}计算报告',0)
                self.m=self.statusbar.currentMessage()

            except ValueError as e:
                QMessageBox.critical(self, '错误', f'计算失败\n\n{e}')
        else:
            QMessageBox.warning(self, '错误', '你还没有读取文件')

    def directional_response_statistics_ui(self, tile):
        """计算方向响应统计（多方向滤波器组）输出结果"""
        if hasattr(self, 'my_matrix'):
            try:
                self.textBrowser_report.setFont(QFont('黑体', 9))
                reuslt = self.my_matrix.directional_response_statistics()
                self.textBrowser_report.clear()
                output = '\n'.join(':'.join(f'{i:>}' for i in item) for item in reuslt.items())
                self.textBrowser_report.append(f'----------------{tile}----------------')
                self.textBrowser_report.append(output)
                self.tabWidget.setCurrentWidget(self.tab_2)
                QMessageBox.information(self, '提示', f'{tile}计算成功')
                self.statusbar.showMessage(f'当前状态：{tile}计算报告',0)
                self.m=self.statusbar.currentMessage()

            except ValueError as e:
                QMessageBox.critical(self, '错误', f'计算失败\n\n{e}')
        else:
            QMessageBox.warning(self, '错误', '你还没有读取文件')

    def count_all(self):
        """计算所有算法"""
        if hasattr(self, 'my_matrix'):
            try:
                self.textBrowser_report.clear()
                self.textBrowser_report.setFont(QFont('黑体', 5))
                gabor_core_real_0 = self.my_matrix.set_fabor_15x15_real(0)
                gabor_core_false_0 = self.my_matrix.set_fabor_15x15_false(0)
                reuslt1 = self.my_matrix.convolutional_calculation_all(gabor_core_real_0, gabor_core_false_0)
                reuslt2 = self.my_matrix.nms_extracts_peak_responses()
                reuslt3 = self.my_matrix.directional_response_statistics()
                output = '\n'.join(' '.join(f'{i:>8.1f}' for i in row) for row in reuslt1)
                self.textBrowser_report.append(f'----------------Gabor 滤波器响应----------------')
                self.textBrowser_report.append(output)

                output = '\n'.join(' '.join(f'{i:>8.1f}' for i in row) for row in reuslt2)
                self.textBrowser_report.append(f'----------------非极大值抑制（NMS）----------------')
                self.textBrowser_report.append(output)

                output = '\n'.join(':'.join(f'{i:>}' for i in item) for item in reuslt3.items())
                self.textBrowser_report.append(f'----------------方向响应统计----------------')
                self.textBrowser_report.append(output)
                self.tabWidget.setCurrentWidget(self.tab_2)
                QMessageBox.information(self, '提示', f'计算成功')
                self.statusbar.showMessage(f'当前状态：计算报告',0)
                self.m=self.statusbar.currentMessage()

            except ValueError as e:
                QMessageBox.critical(self, '错误', f'计算失败\n\n{e}')
        else:
            QMessageBox.warning(self, '错误', '你还没有读取文件')

    def about(self):
        """程序相关信息"""
        QMessageBox.about(self,"关于软件",
                          """
                        <h2> Gabor 纹理方向检测与统计 </h2>
                        <p>版本1.0.0</p>
                        <p>本程序由 python3.10和 PyQt6 构建</p>
                        <p>2026 测绘技能大赛</p>
                          """)

    def help(self):
        try:
            os.startfile('报告文档.pdf')
        except:
            QMessageBox.critical(self, '错误', f'请将报告文档放在正确的文件路径下:.\C2708')



