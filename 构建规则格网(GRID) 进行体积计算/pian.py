import sys
import ezdxf
from ezdxf.math import Vec2
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsPathItem
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF

class DxfDisplayScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_spacing = 30                     # 网格间距（像素）
        self.grid_pen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.DashLine)   # 黑色虚线
        self.grid_item = None                      # 显式网格项
        self.dxf_doc = None                        # 存储 DXF 文档

    def set_dxf_document(self, doc):
        """设置 DXF 文档并刷新显示"""
        self.dxf_doc = doc
        self.refresh_display()

    def refresh_display(self):
        """清空并重绘：网格 + DXF 内容"""
        # 1. 重建网格（根据当前场景矩形）
        self.update_grid()

        # 2. 移除除网格以外的所有图形项
        for item in self.items():
            if item is not self.grid_item:
                self.removeItem(item)

        # 3. 如果没有 DXF 文档，直接返回
        if not self.dxf_doc:
            return

        # 4. 解析 DXF 并添加图形项
        msp = self.dxf_doc.modelspace()
        for entity in msp:
            if entity.dxftype() == 'CIRCLE':
                center = entity.dxf.center
                radius = entity.dxf.radius
                item = QGraphicsEllipseItem(center.x - radius, center.y - radius,
                                            radius * 2, radius * 2)
                item.setBrush(QBrush(QColor(255, 0, 0, 200)))   # 红色填充
                item.setPen(QPen(Qt.GlobalColor.black, 1))
                item.setZValue(1)      # 点在线的上方
                self.addItem(item)

            elif entity.dxftype() in ('LWPOLYLINE', 'POLYLINE'):
                vertices = list(entity.vertices())
                if len(vertices) < 2:
                    continue
                path = QPainterPath()
                first = True
                for v in vertices:
                    # 兼容 Vec2/Vec3 或元组
                    if hasattr(v, 'x'):
                        x, y = v.x, v.y
                    else:
                        x, y = v[0], v[1]
                    if first:
                        path.moveTo(x, y)
                        first = False
                    else:
                        path.lineTo(x, y)
                path_item = QGraphicsPathItem(path)
                path_item.setPen(QPen(Qt.GlobalColor.blue, 2))
                path_item.setZValue(0)   # 线在点之下、网格之上
                self.addItem(path_item)

    def update_grid(self):
        """根据当前场景矩形显式创建网格（作为图形项）"""
        # 移除旧网格
        if self.grid_item is not None:
            self.removeItem(self.grid_item)

        rect = self.sceneRect()
        if rect.isEmpty():
            return

        left = rect.left()
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()

        path = QPainterPath()
        # 竖直线
        x = left + (self.grid_spacing - (left % self.grid_spacing)) % self.grid_spacing
        while x < right:
            path.moveTo(x, top)
            path.lineTo(x, bottom)
            x += self.grid_spacing
        # 水平线
        y = top + (self.grid_spacing - (top % self.grid_spacing)) % self.grid_spacing
        while y < bottom:
            path.moveTo(left, y)
            path.lineTo(right, y)
            y += self.grid_spacing

        self.grid_item = QGraphicsPathItem(path)
        self.grid_item.setPen(self.grid_pen)
        self.grid_item.setZValue(-100)    # 最底层
        self.addItem(self.grid_item)

    # 重写 setSceneRect，以便在场景矩形改变时自动重建网格
    def setSceneRect(self, rect):
        super().setSceneRect(rect)
        self.update_grid()                # 矩形改变后重新生成网格

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("生成 DXF + 显示网格/点/线")
        self.resize(900, 700)

        # 1. 准备散点数据
        self.points = [
            (100, 200), (250, 150), (400, 300), (550, 450), (700, 200),
            (150, 400), (350, 500), (500, 100), (650, 350), (750, 550)
        ]

        # 2. 生成 DXF 文档（内存中）并保存到文件
        self.dxf_doc = self.create_dxf_from_points(self.points)
        self.dxf_doc.saveas("output.dxf")
        print("DXF 文件已保存: output.dxf")

        # 3. 创建场景并设置合适的矩形范围（基于数据点，留边距）
        margin = 50
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        scene_rect = QRectF(x_min - margin, y_min - margin,
                            x_max - x_min + 2*margin, y_max - y_min + 2*margin)

        self.scene = DxfDisplayScene()
        self.scene.setSceneRect(scene_rect)       # 会自动调用 update_grid 生成网格

        # 4. 将 DXF 文档内容绘制到场景中
        self.scene.set_dxf_document(self.dxf_doc)

        # 5. 创建视图并显示
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setBackgroundBrush(QBrush(QColor(255, 255, 255)))   # 白色背景
        self.view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.view.fitInView(scene_rect, Qt.AspectRatioMode.KeepAspectRatio)
        self.setCentralWidget(self.view)

    def create_dxf_from_points(self, points):
        """根据散点数据生成 DXF 文档：圆点 + 折线（按 X 排序）"""
        # 按 X 坐标排序的副本用于折线
        sorted_points = sorted(points, key=lambda p: p[0])

        doc = ezdxf.new('R2010')
        msp = doc.modelspace()

        # 添加圆点（半径 5）
        for (x, y) in points:
            msp.add_circle((x, y), radius=5)

        # 添加多段线（折线）
        if len(sorted_points) >= 2:
            vertices = [Vec2(x, y) for (x, y) in sorted_points]
            msp.add_lwpolyline(vertices)

        return doc

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()