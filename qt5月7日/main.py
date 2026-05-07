from PyQt6.QtWidgets import (QApplication,QMainWindow,QWidget,QTextEdit,QStyle,
QVBoxLayout,QPushButton,QPlainTextEdit,QMenu,QFileDialog,QMessageBox,QInputDialog)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QDir
# from amenubat import Ui_MainWindow
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu=self.menuBar()##获取窗口自带的菜单栏

        self.filemenu=QMenu('文件') #定义一个menu
        self.openFile=QAction('打开文件')#定义一个Action


        self.closeFile = QAction('关闭文件')

        self.inputD=QInputDialog.getInt(self,'标题','内容',1,0,100,1)


        self.openFile.triggered.connect(self.open)



        self.filemenu.addAction(self.openFile)
        self.filemenu.addAction(self.closeFile)

        self.moreMenu=QMenu('更多')
        self.s1=QAction('00')
        self.s2=QAction('01')
        self.s1.triggered.connect(self.message)

        self.moreMenu.addAction(self.s1)
        self.moreMenu.addAction(self.s2)
        self.filemenu.addMenu(self.moreMenu)


        self.menu.addMenu(self.filemenu)

    def message(self):#使用一个messagebox
        QMessageBox.information(self,'你好','世界！')

    def open(self):#打开文件
        curPath=QDir.currentPath()#获取系统当前目录
        filt="文本文件(*.txt)"
        returnpath=QFileDialog.getOpenFileName(self,'选择文件夹这是标题','.',filt)
        print(returnpath)



        # self.setupUi(self)
        self.openFile.triggered.connect(lambda:print('文件打开'))  #openFile
        self.closeFile.triggered.connect(QMainWindow.close)
        # self.actionsave.triggered.connect(lambda:print('文件保存'))


        # textEdit=QPlainTextEdit()
        # textEdit.appendPlainText('sdgf')  ##追加文本
        # bu=QPushButton('追加文本 ')
        # bu.clicked.connect(lambda:textEdit.appendPlainText('sdgf'))
        #
        self.mainLayout=QVBoxLayout()

        # self.mainLayout.addWidget(textEdit)
        # self.mainLayout.addWidget(bu)

        self.setLayout(self.mainLayout)


if __name__ =='__main__':
    app=QApplication([])
    window=MyWindow()
    window.show()
    app.exec()