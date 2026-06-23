import sys
from PyQt6.QtWidgets import QDialog, QWidget, QApplication, QPushButton
from PyQt6.QtCore import pyqtSignal,pyqtSignal
from mymainwindow import Ui_Dialog   # 主窗口 UI
from mysunwindow import Ui_Form      # 子窗口 UI

# 子窗口类（独立窗口）
class SubWindow(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)            # 加载子窗口 UI
        self.setWindowTitle("子窗口")


# 主窗口类
class MainWindow(QDialog, Ui_Dialog):
    '''定义一个str类型的信号'''
    nametext = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        ok_button = self.buttonBox.button(self.buttonBox.StandardButton.Ok)
        # 将确定按钮的点击信号连接到自定义槽函数
        ok_button.clicked.connect(self.open_sub_window)

        self.sub_win = SubWindow()
        self.sub_win.show()
        '''建立信号连接（只需一次）'''
        self.nametext.connect(self.lineEdit.setText)



    def open_sub_window(self):
        # 创建子窗口实例（非模态，独立显示）
        text= self.sub_win.lineEdit.text()
        self.nametext.emit(text)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())