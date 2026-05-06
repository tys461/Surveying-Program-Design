from PySide6.QtWidgets import QApplication,QMainWindow,QPushButton,QLabel

class Mywindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # button=QPushButton('按钮',self)#没有布局一定要传入参数self
        # button.setGeometry(0,0,150,20)
        # button.setToolTip('有惊喜')
        # button.setText('我被重新设置')
        la=QLabel('label',self)
        la.


if __name__=='__main__':
    app=QApplication([])
    window=Mywindow()
    window.show()
    app.exec()

