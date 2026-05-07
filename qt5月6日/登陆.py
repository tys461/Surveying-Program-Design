from PyQt6.QtWidgets import QApplication,QWidget,QComboBox,QVBoxLayout,QCheckBox,QPushButton
# from uiJisuan import Ui_Form

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        bo=QCheckBox("请勾选我")
        # bo.addItems(['梨花','张三','小民'])
        # bo.currentIndexChanged.connect(lambda:print(bo.currentText()))
        bt=QPushButton('查看选择')
        bt.clicked.connect(lambda:print(bo.isChecked()))


        mainlayout=QVBoxLayout()
        mainlayout.addWidget(bo)
        mainlayout.addWidget(bt)
        self.setLayout(mainlayout)

    #     self.reuslt=''
    #     self.bind()
    # def bind(self):
    #     self.pushButton0.clicked.connect(lambda:self.addNum('0'))
    #     self.pushButton_1.clicked.connect(lambda:self.addNum('1'))
    #     self.pushButton_2.clicked.connect(lambda:self.addNum('2'))
    #     self.pushButton_3.clicked.connect(lambda:self.addNum('3'))
    #     self.pushButton_4.clicked.connect(lambda:self.addNum('4'))
    #     self.pushButton_5.clicked.connect(lambda:self.addNum('5'))
    #     self.pushButton_6.clicked.connect(lambda:self.addNum('6'))
    #     self.pushButton_7.clicked.connect(lambda:self.addNum('7'))
    #     self.pushButton_8.clicked.connect(lambda:self.addNum('8'))
    #     self.pushButton_9.clicked.connect(lambda:self.addNum('9'))
    #     self.pushButton_jia.clicked.connect(lambda:self.addNum('+'))
    #     self.pushButton_jian.clicked.connect(lambda:self.addNum('-'))
    #     self.pushButton_cheng.clicked.connect(lambda:self.addNum('*'))
    #     self.pushButton_chu.clicked.connect(lambda:self.addNum('/'))
    #     self.pushButton_den.clicked.connect(self.equal)
    #
    #
    #
    # def addNum(self,number):
    #     self.textEdit.clear()
    #     self.reuslt+=number
    #     self.textEdit.setText(self.reuslt)
    #
    # def equal(self):
    #     self.numberruslt=eval(self.reuslt)
    #     self.textEdit.setText(str(self.numberruslt))




    #     self.pushButton.clicked.connect(self.loginfuc)
    # def loginfuc(self):
    #     #获取账号
    #     account=self.lineEdit.text()
    #     #获取密码
    #     password=self.lineEdit_2.text()
    #
    #     if account=='123' and password=='123':
    #         print("登陆成功")
    #     else:
    #         print("登陆失败")

if __name__ == "__main__":
    app=QApplication([])
    window=MyWindow()
    window.show()
    app.exec()
