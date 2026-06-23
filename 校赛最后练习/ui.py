from PyQt6.QtWidgets import QMainWindow,QWidget,QMessageBox,QFileDialog,QTableWidgetItem,QHeaderView,QTableWidget,QLabel,QStyle
from PyQt6.QtGui import QActionGroup,QAction
from PyQt6.QtCore import QFile,QIODevice,QTextStream,pyqtSignal,Qt
from PyQt6.QtGui import QIcon
from mainwin import Ui_MainWindow
from baogao import Ui_Form_bao
from zhuanhuan import Ui_Form_zhuan
from prossce import tranform,lindaihuansuan

class BaogaoWin(QWidget,Ui_Form_bao):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class ZhuanWin(QWidget,Ui_Form_zhuan,):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__zhuanduda=3
        self.zhua_ell='kelasuofu'
        self.trigg()

    def trigg(self):
        self.radioButton.clicked.connect(self.Z_zhuan1)
        self.radioButton_2.clicked.connect(self.Z_zhuan2)
        self.pushButton.clicked.connect(self.count)



    def Z_zhuan1(self):
        if self.radioButton.isChecked():
            self.__zhuanduda = 3
            # print(3)

    def Z_zhuan2(self):
        if self.radioButton_2.isChecked():
            self.__zhuanduda = 6
            # print(6)


    def count(self):
        x=self.lineEdit_X.text()
        y=self.lineEdit_Y.text()
        try:
            x=float(x)
            y=float(y)
        except:
            QMessageBox.information(self,'提醒','数据有误，请输入正确的数据')
        else:
            result_lis=lindaihuansuan(x,y,self.__zhuanduda,self.zhua_ell)
            print(result_lis)
            lelf=result_lis[0]
            right=result_lis[1]
            print(str(lelf[0]))
            self.lineEdit_lx.setText(str(lelf[0]))
            self.lineEdit_ly.setText(str(lelf[1]))
            self.lineEdit_rx.setText(str(right[0]))
            self.lineEdit_ry.setText(str(right[1]))


class MyMainwin(QMainWindow,Ui_MainWindow):
    reporttext = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.duda=3
        self.otduda=6
        self.ell='kelasuofu'
        self.report_text=''
        self.data_lis = []

        self.status()
        self.actiongroup()
        self.addact()
        self.act_trigg()
        self.clear()
        self.syl()

    '''初始化'''
    def actiongroup(self):
        '''设置椭球单选互斥'''
        self.ellipsoid_group = QActionGroup(self)
        self.ellipsoid_group.addAction(self.actionkelasuofu)
        self.ellipsoid_group.addAction(self.actionIUGG1975)
        self.ellipsoid_group.addAction(self.actionCGCS2000)
        '''设置功能互斥'''
        self.function_group = QActionGroup(self)
        self.function_group.addAction(self.actiontrans3_6)
        self.function_group.addAction(self.actiontrans6_3)


    def addact(self):
        '''在菜单栏添加action'''
        before_action = self.menu_3.menuAction() # 关键：获取菜单的代表动作
        self.action_huan=QAction('邻带换算',self)
        self.action_report=QAction('报告',self)
        self.action_jie=QAction('解算',self)
        self.menubar.insertAction(before_action,self.action_jie)
        self.menubar.addAction(self.action_huan)
        self.menubar.addAction(self.action_report)

    def act_trigg(self):
        '''连接函数'''
        self.action_huan.triggered.connect(self.zhuan)
        self.action_report.triggered.connect(self.bogao)
        self.action_jie.triggered.connect(self.jiesuan)
        self.actionopen.triggered.connect(self.aopen)
        self.actionclean.triggered.connect(self.clear)
        self.actiontrans3_6.triggered.connect(self.on_toggled3)
        self.actiontrans6_3.triggered.connect(self.on_toggled6)
        self.actionkelasuofu.triggered.connect(self.ell_check_kelasuofu)
        self.actionIUGG1975.triggered.connect(self.ell_check_IUGG1975)
        self.actionCGCS2000.triggered.connect(self.ell_check_CGCS2000)
        self.action.triggered.connect(self.jiesuan)
        self.actionsave.triggered.connect(self.save)


    def status(self):
        # 1. 创建三个永久标签
        self.left_label = QLabel("就绪")
        self.center_label = QLabel(f"{self.duda}度带转{self.otduda}度带")
        self.right_label = QLabel(f"椭球参数：{self.ell}")

        # 2. 添加到状态栏，并使用 stretch 分配空间
        #    - 第一个 stretch=1 将左侧标签推到左边
        #    - 第二个 stretch=1 将中间标签推到中间
        #    - 第三个 stretch=1 将右侧标签推到右边（实际上 addPermanentWidget 也可，但这里统一用 addWidget）
        self.statusbar.addWidget(self.left_label, 1)  # stretch=1
        self.statusbar.addWidget(self.center_label, 1)  # stretch=1
        self.statusbar.addWidget(self.right_label, 1)  # stretch=1

        # 可选：设置标签的最小宽度，避免被压缩
        self.left_label.setMinimumWidth(120)
        self.center_label.setMinimumWidth(120)
        self.right_label.setMinimumWidth(120)

    def syl(self):
        self.action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))


    '''定义子窗口'''
    def bogao(self):
        self.report=BaogaoWin()
        self.report.textBrowser.setText(self.report_text)
        self.report.show()

    def zhuan(self):
        self.zhuanhuan=ZhuanWin()
        self.zhuanhuan.zhua_ell=self.ell
        self.zhuanhuan.show()




    """方法"""
    def open_data(self):
        self.data_lis = []

        '''读取文件数据'''
        get_file=QFileDialog.getOpenFileName(self,"选择点文件",'.','txt文件(*txt)')
        print(get_file)
        file=QFile(get_file[0])
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            QMessageBox.information(self,'错误','文件读取失败')
            return
        stream=QTextStream(file)
        while not stream.atEnd():
            line = stream.readLine()
            parts = line.split()
            print(parts)
            if len(parts)==4:
                self.data_lis.append(parts)

    def save(self):
        if len(self.report_text)==0:
            QMessageBox.information(self, '提醒', '你还没有解算数据')
            return
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存文件",
                "savedata",
                "txt文件(*.txt)",
            )
            file=QFile(file_path)
            if not file.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
                QMessageBox.information(self, '提醒', '数据写入失败')
                return
            file.write(self.report_text.encode('utf-8'))
            file.close()



    def data_tablewidget(self,duda,data,table):
        '''创建表格'''
        # 禁止编辑
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        headers = ["点号", "x坐标 (m)", "y坐标 (m)", "y通用坐标 (m)"]
        self.title_text = f"{duda}度带坐标"

        # 总行数 = 1(大标题) + 1(列标题) + 数据行数
        total_rows = len(data) + 2
        total_cols = len(headers)
        # 设置表格行列数
        table.setRowCount(total_rows)
        table.setColumnCount(total_cols)

        # 1. 合并第一行作为大标题
        table.setSpan(0, 0, 1, total_cols)  #0 0开始竖向跨度 横向跨度
        title_item = QTableWidgetItem(self.title_text)
        title_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title_item.font()
        font.setPointSize(14)
        font.setBold(True)
        title_item.setFont(font)
        table.setItem(0, 0, title_item)

        # 2. 第二行设置列标题
        for col, header in enumerate(headers):
            item = QTableWidgetItem(header)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # 可选：设置表头背景色
            # item.setBackground(Qt.GlobalColor.lightGray)
            table.setItem(1, col, item)

        # 3. 填充数据行（从第三行开始，索引2）
        for row, row_data in enumerate(data):
            # row_data 是从文件读取的四个字符串列表，例如 ["1", "4538610.951", "98666.625", "33598666.625"]
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                print(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                table.setItem(row + 2, col, item)

        # 4. 美化：调整列宽
        table.resizeColumnsToContents()
        # 可选：让列宽等分剩余空间
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # 5. 隐藏默认的行号（垂直表头）
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)


    '''判断勾选部分'''
    def on_toggled3(self):
        if self.actiontrans3_6.isChecked():  # 仅在勾选时执行
            self.duda = 3
            self.otuda=6
            self.clear()
            self.center_label.setText(f"{self.duda}度带转{self.otduda}度带")
        print(f'3{self.duda}')

    def on_toggled6(self):
        if self.actiontrans6_3.isChecked():  # 仅在勾选时执行
            self.duda = 6
            self.otduda=3
            self.clear()
            self.center_label.setText(f"{self.duda}度带转{self.otduda}度带")
        print(f'6{self.duda}')

    def ell_check_kelasuofu(self):
        if self.actionkelasuofu.isChecked():
            self.ell = 'kelasuofu'
            self.right_label.setText(f"椭球参数：{self.ell}")
        print(self.ell)
    def ell_check_IUGG1975(self):
        if self.actionIUGG1975.isChecked():
            self.ell = 'IUGG1975'
            self.right_label.setText(f"椭球参数：{self.ell}")
        print(self.ell)
    def ell_check_CGCS2000(self):
        if self.actionCGCS2000.isChecked():
            self.ell = 'CGCS2000'
            self.right_label.setText(f"椭球参数：{self.ell}")
        print(self.ell)



    def jiesuan(self):
        '''解算和输出报告'''
        # print(self.data_lis)
        if not self.data_lis:
            QMessageBox.information(self, '提醒', '原始数据未读取')
            return
        else:
            self.result_lis=[]
            a=1
            for i in self.data_lis:
                result=tranform(float(i[1]),float(i[3]),self.duda,self.ell)
                print()
                result.insert(0,a)
                self.result_lis.append(result)
                a+=1
            print(self.result_lis)
            if self.duda==3:
                print(self.otduda)
                self.data_tablewidget(self.otduda,self.result_lis,self.tableWidget_2)
            if self.duda==6:
                self.data_tablewidget(self.otduda,self.result_lis,self.tableWidget_2)
                print(self.otduda)
            self.report_text=('           计算报告            \n'
                              '------------------------------\n'
                              f'{self.duda}度带转{self.otduda}\n'
                              f'{self.ell}球\n'
                              )

            self.report_text = self.report_text + f'{self.duda}度带\n'
            self.report_text = self.report_text + '---------------------\n'
            self.report_text = self.report_text + f'点号 通用X（m）  Y（m）  通用Y（m）\n'
            for i in self.data_lis:
                for f in i:
                    self.report_text=self.report_text+f'{f}  '
                self.report_text=self.report_text+'\n'

            self.report_text = self.report_text + f'{self.otduda}度带\n'
            self.report_text = self.report_text + '---------------------\n'
            self.report_text = self.report_text + f'点号 通用X（m）  Y（m）  通用Y（m）\n'
            for i in self.result_lis:
                for f in i:
                    self.report_text = self.report_text + f'{f}  '
                self.report_text=self.report_text+'\n'











    '''初始化或清除数据'''
    def clear(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget_2.setRowCount(0)

        self.l = ['', '', '', ''] * 10
        self.data_tablewidget(self.duda , self.l, self.tableWidget)
        self.data_tablewidget(self.otduda, self.l, self.tableWidget_2)


    '''打开写入文件'''
    def aopen(self):
        self.open_data()
        if not self.data_lis:
            return
        else:
            self.data_tablewidget(self.duda,self.data_lis,self.tableWidget)

