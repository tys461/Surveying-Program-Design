import sys
from PyQt6.QtWidgets import QApplication
import ui
from data_fetcher import readOpen
from processor import dadt_processor


if __name__=='__main__':
    data=readOpen('D:\测绘技能大赛\测绘技能大赛程序设计学习\part3\原始数据.txt')
    data.open()
    d=dadt_processor(data.data,50)
    app=QApplication(sys.argv)
    window=ui.MyWindow()
    window.show()
    sys.exit(app.exec())
