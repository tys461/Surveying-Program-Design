import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QMessageBox, QLabel,
    QGraphicsView, QGraphicsScene, QGraphicsPathItem,
    QGraphicsEllipseItem, QGraphicsLineItem
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainterPath, QColor, QPen, QBrush

# 导入你的 process_p 模块
from process_p import Point, Points


class GraphicsView(QGraphicsView):
    """自定义视图，内置滚轮缩放和双击适应"""
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("三角网可视化 (QGraphicsView)")
        self.setGeometry(100, 100, 900, 700)

        # 中央容器
        container = QWidget()
        layout = QVBoxLayout(container)

        # 打开文件按钮
        self.btn_open = QPushButton("打开数据文件")
        self.btn_open.clicked.connect(self.open_file)
        layout.addWidget(self.btn_open, alignment=Qt.AlignmentFlag.AlignLeft)

        # 场景和视图
        self.scene = QGraphicsScene()
        self.view = GraphicsView(self.scene)
        layout.addWidget(self.view)

        self.setCentralWidget(container)

        # 状态栏
        self.status_label = QLabel("请打开 .txt 数据文件")
        self.statusBar().addWidget(self.status_label)

        # 缓存数据（以便重绘）
        self.vertices = []
        self.triangles = []

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择数据文件", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        if not file_path:
            return

        try:
            points = self.read_data(file_path)
            if not points:
                QMessageBox.warning(self, "警告", "文件为空或格式错误")
                return

            # 三角剖分
            triangulator = Points(h=points[0].z, lis_point=points)
            triangles = triangulator.build_triangulation()  # list[Triangle]

            if not triangles:
                QMessageBox.warning(self, "警告", "未能生成有效三角形")
                return

            # 提取绘制数据
            self.vertices = [(p.x, p.y) for p in points]
            self.triangles = [(t.v0, t.v1, t.v2) for t in triangles]

            # 构建场景
            self.build_scene()

            self.status_label.setText(
                f"已加载: {len(points)} 个点, {len(triangles)} 个三角形"
            )

            # 自适应视图
            self.view.fitInView(
                self.scene.itemsBoundingRect(),
                Qt.AspectRatioMode.KeepAspectRatio
            )

        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理数据时出错:\n{str(e)}")
            self.status_label.setText("加载失败")

    def build_scene(self):
        """根据 self.vertices 和 self.triangles 构建场景图元"""
        self.scene.clear()

        if not self.vertices or not self.triangles:
            return

        # ---------- 1. 绘制格网（间隔2，虚线） ----------
        xs = [p[0] for p in self.vertices]
        ys = [p[1] for p in self.vertices]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        spacing = 2.0

        # 网格范围（向外扩展一个间距）
        grid_min_x = math.floor(min_x / spacing) * spacing
        grid_max_x = math.ceil(max_x / spacing) * spacing
        grid_min_y = math.floor(min_y / spacing) * spacing
        grid_max_y = math.ceil(max_y / spacing) * spacing

        pen_grid = QPen(QColor(200, 200, 200), 0.8, Qt.PenStyle.DashLine)
        # 竖线
        x = grid_min_x
        while x <= grid_max_x:
            self.scene.addLine(x, grid_min_y, x, grid_max_y, pen_grid)
            x += spacing
        # 横线
        y = grid_min_y
        while y <= grid_max_y:
            self.scene.addLine(grid_min_x, y, grid_max_x, y, pen_grid)
            y += spacing

        # ---------- 2. 绘制三角网（填充 + 边框） ----------
        path = QPainterPath()
        for (i1, i2, i3) in self.triangles:
            p1 = QPointF(*self.vertices[i1])
            p2 = QPointF(*self.vertices[i2])
            p3 = QPointF(*self.vertices[i3])
            path.moveTo(p1)
            path.lineTo(p2)
            path.lineTo(p3)
            path.closeSubpath()

        # 填充颜色（半透明蓝）+ 黑色边框
        fill_brush = QBrush(QColor(100, 150, 255, 120))
        pen_border = QPen(QColor(0, 0, 0), 1.5)
        item = self.scene.addPath(path, pen_border, fill_brush)
        # 注意：addPath 返回 QGraphicsPathItem，可以后续操作

        # ---------- 3. 绘制顶点（红色圆点） ----------
        pen_vertex = QPen(QColor(0, 0, 0), 1)
        brush_vertex = QBrush(QColor(255, 0, 0))
        for (x, y) in self.vertices:
            # 椭圆中心在 (x,y)，半轴 4
            self.scene.addEllipse(x - 4, y - 4, 8, 8, pen_vertex, brush_vertex)

        # ---------- 4. 绘制示例折线（绿色，连接前10个点） ----------
        if len(self.vertices) >= 10:
            pts = [QPointF(x, y) for (x, y) in self.vertices[:10]]
            poly_path = QPainterPath()
            poly_path.moveTo(pts[0])
            for pt in pts[1:]:
                poly_path.lineTo(pt)
            pen_poly = QPen(QColor(0, 255, 0), 2.0)
            self.scene.addPath(poly_path, pen_poly)

    def read_data(self, file_path):
        """读取数据文件，返回 list[Point]"""
        points = []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        if len(lines) < 2:
            return None

        # 第一行是 "基准高程,数值"，跳过（但 process_p 中 Points 需要 h，这里随便取）
        # 我们只关心点数据
        for line in lines[1:]:
            parts = line.split(',')
            if len(parts) != 4:
                continue
            name = parts[0].strip()
            try:
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                points.append(Point(name, x, y, z))
            except ValueError:
                continue
        return points


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())