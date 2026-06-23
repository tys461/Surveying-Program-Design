import sys
from PyQt6.QtWidgets import QApplication ,QMainWindow
from PyQt6.QtGui import QActionGroup
from win import Ui_MainWindow

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 互斥组
        self.count_group = QActionGroup(self)
        self.count_group.addAction(self.actioncount1)
        self.count_group.addAction(self.actioncount2)
        self.count_group.addAction(self.actioncount3)
        self.count_group.setExclusive(True)   # 确保同一时间只有一个被选中

        # 连接菜单项槽函数
        self.actioncount1.triggered.connect(self.count1)
        self.actioncount2.triggered.connect(self.count2)
        self.actioncount3.triggered.connect(self.count3)

        # 记录当前选中的 action（默认选中 count1）
        self.current_count_action = self.actioncount1
        self.actioncount1.setChecked(True)

        # 当用户在菜单中切换选择时，更新 current_count_action
        self.actioncount1.triggered.connect(lambda: self.set_current_action(self.actioncount1))
        self.actioncount2.triggered.connect(lambda: self.set_current_action(self.actioncount2))
        self.actioncount3.triggered.connect(lambda: self.set_current_action(self.actioncount3))

        # 将工具栏的 actioncount 连接到执行当前选中功能的槽函数
        self.actioncount.triggered.connect(self.execute_current_count)

    def set_current_action(self, action):
        self.current_count_action = action

    def execute_current_count(self):
        # 触发当前选中的 action，从而执行对应的 count1/count2/count3
        self.current_count_action.trigger()

    def count1(self):
        print('1')

    def count2(self):
        print('2')

    def count3(self):
        print('3')


if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MyMainWindow()
    window.show()
    sys.exit(app.exec())