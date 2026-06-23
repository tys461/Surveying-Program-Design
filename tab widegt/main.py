import sys
from PyQt6.QtWidgets import QApplication,QMainWindow
from ui import Ui_MainWindow

class Mianwindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ee()

    def ee(self):
        self.tabWidget.setCurrentWidget(self.tab_2)


if __name__=='__main__':
    app=QApplication(sys.argv)
    window=Mianwindow()
    window.show()
    sys.exit(app.exec())

# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton
#
# class Demo(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("标签页跳转示例")
#         self.setGeometry(100, 100, 400, 300)
#
#         layout = QVBoxLayout()
#         self.tab_widget = QTabWidget()
#
#         # 创建两个页面
#         page1 = QWidget()
#         page1_layout = QVBoxLayout()
#         page1_layout.addWidget(QLabel("这是页面 1"))
#         page1.setLayout(page1_layout)
#
#         page2 = QWidget()
#         page2_layout = QVBoxLayout()
#         page2_layout.addWidget(QLabel("这是页面 2"))
#         page2.setLayout(page2_layout)
#
#         self.tab_widget.addTab(page1, "标签 1")
#         self.tab_widget.addTab(page2, "标签 2")
#
#         # 创建跳转按钮
#         btn = QPushButton("跳转到页面 2")
#         btn.clicked.connect(self.jump_to_page2)
#
#         layout.addWidget(self.tab_widget)
#         layout.addWidget(btn)
#         self.setLayout(layout)
#
#     def jump_to_page2(self):
#         # 通过索引跳转（索引 1 表示第二个标签页）
#         self.tab_widget.setCurrentIndex(1)
#         # 或者通过页面对象跳转（需要提前保存页面2的引用）
#         # self.tab_widget.setCurrentWidget(self.page2)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Demo()
#     window.show()
#     sys.exit(app.exec())