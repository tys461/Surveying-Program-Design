# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton,QPlainTextEdit,QMessageBox


# def handlecale():
#     info=textEdit.toPlainText()
#     print('666')
#     QMessageBox.about(my_window,'统计结果',f"{info}")
#
#
# app=QApplication()
# my_window=QMainWindow()
#
# my_window.resize(500,400)
# my_window.move(30,200)
# my_window.setWindowTitle('This is my window')
#
# textEdit=QPlainTextEdit(my_window)
# textEdit.setPlaceholderText('请输入东西')
# textEdit.resize(300,300)
# textEdit.move(10,25)
#
# button=QPushButton('点击',my_window)
# button.move(380,80)
# button.clicked.connect(handlecale)
#
#
# my_window.show()
#
# app.exec()
# from PySide6.QtWidgets import QApplication, QMessageBox
# from PySide6.QtUiTools import QUiLoader
#
#
# class Stats:
#
#     def __init__(self):
#         # 从文件中加载UI定义
#
#         # 从 UI 定义中动态 创建一个相应的窗口对象
#         # 注意：里面的控件对象也成为窗口对象的属性了
#         # 比如 self.ui.button , self.ui.textEdit
#         self.ui = QUiLoader().load('untitled.ui')
#
#         self.ui.button.clicked.connect(self.handleCalc)
#
#     def handleCalc(self):
#         info = self.ui.textEdit.toPlainText()
#
#         salary_above_20k = ''
#         salary_below_20k = ''
#         for line in info.splitlines():
#             if not line.strip():
#                 continue
#             parts = line.split(' ')
#
#             parts = [p for p in parts if p]
#             name, salary, age = parts
#             if int(salary) >= 20000:
#                 salary_above_20k += name + '\n'
#             else:
#                 salary_below_20k += name + '\n'
#
#         QMessageBox.about(self.ui,
#                           '统计结果',
#                           f'''薪资20000 以上的有：\n{salary_above_20k}
#                     \n薪资20000 以下的有：\n{salary_below_20k}'''
#                           )
#
#
# app = QApplication()
# stats = Stats()
# stats.ui.show()
# app.exec()

from PySide6.QtWidgets import QApplication, QMainWindow,QWidget
from ui_main import Ui_Form
from ome import Tex_dat


# 注意 这里选择的父类 要和你UI文件窗体一样的类型
# 主窗口是 QMainWindow， 表单是 QWidget， 对话框是 QDialog
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_Form()

        # 初始化界面
        self.ui.setupUi(self)
        self.ui.button.clicked.connect(self.hh)
        # 使用界面定义的控件，也是从ui里面访问
        # self.ui.webview.load('http://www.baidu.com')
    def hh(self):
        print('hh')
        for i in range(len(dat.dat)-1):
            self.ui.textBrowser.append(f'{','.join(dat.dat[i])}')

