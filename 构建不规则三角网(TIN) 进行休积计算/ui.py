from PyQt6.QtCore import QFile, QIODevice, QTextStream, Qt, QPointF
from PyQt6.QtGui import QFont, QPainter, QPainterPath, QBrush, QPen, QColor,QIcon
from PyQt6.QtWidgets import (QMainWindow, QLabel, QLineEdit, QFileDialog
                            , QMessageBox, QTableWidgetItem, QGraphicsView, QGraphicsScene)
from window import Ui_MainWindow
from process import *

def open(path):
    file = QFile(path)
    lis_points = []
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件打开失败')
        return
    else:
        stream = QTextStream(file)
        line1 = stream.readLine().split(',')
        h = float(line1[1])
        while not stream.atEnd():
            part = stream.readLine().split(',')
            if len(part) == 4:
                a = Point(part[0], float(part[1]), float(part[2]), float(part[3]))
                lis_points.append(a)
        return Points(h, lis_points)


class GraphicsView(QGraphicsView):
    """自定义视图，内置缩放功能"""

    def __init__(self, scene):
        super().__init__(scene)
        # 开启拖拽平移（手形光标）
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        # 抗锯齿
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 缩放时以鼠标位置为中心
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def wheelEvent(self, event):
        # 滚轮缩放：每次缩放 1.1 倍
        factor = 1.1 if event.angleDelta().y() > 0 else 1 / 1.1
        self.scale(factor, factor)

    def mouseDoubleClickEvent(self, event):
        # 双击重置为最佳适应视图
        self.fitInView(self.scene().itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.textBrowser.setFont(QFont('黑体', 13))
        self.set_paint()
        self.insert_widget()
        self.action_conncet()

    def set_paint(self):
        """设置场景和视图"""
        self.scene = QGraphicsScene()
        self.view = GraphicsView(self.scene)
        self.verticalLayout_3.addWidget(self.view)

    def action_conncet(self):
        """action链接对应的槽函数"""
        self.action_open.triggered.connect(self.open_data)
        self.action_save.triggered.connect(self.save)
        self.action_count.triggered.connect(self.count)
        self.action_big.triggered.connect(self.zoom_in)
        self.action_samll.triggered.connect(self.zoom_out)
        self.tabWidget.currentChanged.connect(self.set_statusbar)
        self.action_data.triggered.connect(lambda: self.tabWidget.setCurrentWidget(self.data))
        self.action_tri.triggered.connect(lambda: self.tabWidget.setCurrentWidget(self.tri))
        self.action_report.triggered.connect(lambda: self.tabWidget.setCurrentWidget(self.report))
        self.action_about.triggered.connect(self.about)
        self.action_close.triggered.connect(self.close)

    def insert_widget(self):
        """在toolBar中插入控件"""
        self.l_base_h = QLabel('基准高程')
        self.base_line = QLineEdit()
        self.base_line.setMaximumWidth(60)
        self.l_equilibrium_h = QLabel('平衡高程')
        self.equilibrium_line = QLineEdit()
        self.equilibrium_line.setMaximumWidth(60)

        self.toolBar.insertWidget(self.action_close, self.l_base_h)
        self.toolBar.insertWidget(self.action_close, self.base_line)
        self.toolBar.addSeparator()
        self.toolBar.insertWidget(self.action_close, self.l_equilibrium_h)
        self.toolBar.insertWidget(self.action_close, self.equilibrium_line)

    def set_statusbar(self, idx):
        """状态栏切换"""
        if idx == 0:
            if hasattr(self, 'point_data'):
                self.statusbar.showMessage('当前状态：点云数据', 0)
            else:
                self.statusbar.showMessage('当前状态：还未读取点云数据', 0)
        if idx == 1:
            self.statusbar.showMessage('当前状态：三角网示意图', 0)

        if idx == 2:
            if self.textBrowser.toPlainText() == '':
                self.statusbar.showMessage('当前状态：还未计算', 0)
            else:
                self.statusbar.showMessage('当前状态:计算报告', 0)

    def open_data(self):
        """读取点云文件"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, '选择点云文件', '.\data', 'txt(*.txt)')
            data = open(file_path)
            points = data.lis_points

            heards = ['点名', 'X分量', 'Y分量', 'Z分量']
            row = len(points) + 1
            col = len(heards)

            self.tableWidget.setRowCount(row)
            self.tableWidget.setColumnCount(col)

            for idx, heard in enumerate(heards):
                item = QTableWidgetItem(heard)
                self.tableWidget.setItem(0, idx, item)

            for idx, point in enumerate(points):
                self.tableWidget.setItem(idx + 1, 0, QTableWidgetItem(point.n))
                self.tableWidget.setItem(idx + 1, 1, QTableWidgetItem(str(point.x)))
                self.tableWidget.setItem(idx + 1, 2, QTableWidgetItem(str(point.y)))
                self.tableWidget.setItem(idx + 1, 3, QTableWidgetItem(str(point.z)))

            self.base_line.setText(f'{data.base_h}m')
            self.point_data = data
            self.tabWidget.setCurrentWidget(self.data)
            self.statusbar.showMessage('当前状态：点云数据', 0)
            QMessageBox.information(self, '提示', '文件读取成功')

            pen_point = QPen(QColor(225, 0, 0), 0.1)
            brush_point = QBrush(QColor(255, 0, 0))
            for p in self.point_data.lis_points:
                self.scene.addEllipse(p.x - 0.5, p.y - 0.5, 1, 1, pen_point, brush_point)
            self.view.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

        except:
            QMessageBox.critical(self, '错误', '文件读取失败')

    def save(self):
        """保存报告文档"""
        result = self.textBrowser.toPlainText()
        print(result)
        if result != '':
            try:
                save_path, _ = QFileDialog.getSaveFileName(self, '保存路径', r'.\result', 'txt(*.txt)')
                file = QFile(save_path)
                file.open(QIODevice.OpenModeFlag.WriteOnly)
                file.write(result.encode('utf-8'))
                QMessageBox.information(self, '提示', '保存成功')
            except:
                QMessageBox.critical(self, '错误', '保存失败')
        else:
            QMessageBox.information(self, '提醒', '你还未计算生成计算报告，请进行计算生成计算报告')

    """
    基准高程9.0m
    三角形个数:73
    平衡高程:10.8180969358142
    总挖方体积:7291.33655767516
    总填方体积:0
    总体积:7291.33655767516
    
    ------------------三角形说明------------------
    序号    三个顶点
    1       P06     P07     P08    
    
    ------------------具体体积说明--------------------
    序号    挖方体积  填方体积         
    1       9.412     0.000 
    """

    def count(self):
        if hasattr(self, 'point_data'):

            base_h = self.point_data.base_h
            tris, aver_h = self.point_data.calculate_equilibrium_elevation()
            V_fill, V_cul, dic_fill_cul = self.point_data.calculation_volume_excavated_fill_area_triangle()
            fill_lis = dic_fill_cul.get('fill')
            cul_lis = dic_fill_cul.get('cul')

            self.equilibrium_line.setText(f'{aver_h:.3f}m')

            self.textBrowser.setText("                   结果报告                   \n"
                                     "-------------------基本信息----------------------\n"
                                     f"基准高程:{base_h}m\n"
                                     f"三角形个数:{len(tris)}\n"
                                     f"平衡高程:{aver_h}\n"
                                     f"总挖方体积:{V_cul}\n"
                                     f"总填方体积:{V_fill}\n"
                                     f"总体积:{V_cul + V_fill}\n")

            self.textBrowser.append("------------------三角形说明------------------\n"
                                    f"{'序号':<4}{'三个顶点':<4}")
            output = '\n'.join(f'{idx + 1:<8}{p.p0.n:<8}{p.p1.n:<8}{p.p2.n:<8}' for idx, p in enumerate(tris))
            self.textBrowser.append(output)

            self.textBrowser.append("------------------具体体积说明------------------\n"
                                    f"{'序号':<6}{'挖方体积':<7}{'填方体积':<7}")
            output = '\n'.join(
                f'{idx + 1:<10}{cul_lis[idx]:<10.3f}{fill_lis[idx]:<10.3f}' for idx in range(len(fill_lis)))
            self.textBrowser.append(output)

            self.tabWidget.setCurrentWidget(self.report)
            self.statusbar.showMessage('当前状态：计算报告', 0)
            QMessageBox.information(self, '提示', '计算成功')

            self.build_scene_tri(tris) #生成三角网

        else:
            QMessageBox.critical(self, '错误', '你还未读取矩阵文件')

    def build_scene_tri(self, tris):
        """绘制三角网"""
        self.scene.clear()
        if not tris:
            return
        """绘制三角网"""
        path = QPainterPath()
        for tri in tris:
            p0 = tri.p0
            p1 = tri.p1
            p2 = tri.p2
            path.moveTo(QPointF(p0.x, p0.y))
            path.lineTo(QPointF(p1.x, p1.y))
            path.lineTo(QPointF(p2.x, p2.y))
            path.closeSubpath()

        fill_brush = QBrush(QColor(237, 243, 254))
        pen_border = QPen(QColor(0, 0, 0), 0.1)
        item = self.scene.addPath(path, pen_border, fill_brush)

        pen_point = QPen(QColor(225, 0, 0), 0.1)
        brush_point = QBrush(QColor(255, 0, 0))
        for p in self.point_data.lis_points:
            self.scene.addEllipse(p.x - 0.5, p.y - 0.5, 1, 1, pen_point, brush_point)
        self.view.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)#确保视图居中

    def zoom_in(self):
        """action控制缩放"""
        factor = 1.1
        self._zoom_at_center(factor)

    def zoom_out(self):
        factor = 1 / 1.1
        self._zoom_at_center(factor)

    def _zoom_at_center(self, factor):
        view = self.view
        # 获取当前视图中心对应的场景坐标
        center = view.mapToScene(view.viewport().rect().center())
        # 缩放
        view.scale(factor, factor)
        # 重新将中心点移动到视图中心
        view.centerOn(center)


    def about(self):
        QMessageBox.about(self,'关于',
                          """
                          <h2>构建不规则三角网(TIN) 进行休积计算</h2>
                          <p>由 python 3.10 和 PyQt6 所编写</p>
                          <p>版本 ：1.0.0 </p>
                          """)
