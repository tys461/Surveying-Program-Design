import sys
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QBrush

# --------------------------- 点类与凸包算法（已修正）----------------------------
class Point:
    def __init__(self, point_name, point_X, point_Y, point_Z=0.0):
        self.point_name = point_name
        self.point_X = point_X
        self.point_Y = point_Y
        self.point_Z = point_Z

    def __repr__(self):
        return f'({self.point_X:.4f},{self.point_Y:.4f},{self.point_Z})'

def cross(o, a, b):
    """二维叉积 (oa × ob) >0 表示左转"""
    return (a.point_X - o.point_X) * (b.point_Y - o.point_Y) - (a.point_Y - o.point_Y) * (b.point_X - o.point_X)

def convex_hull(points):
    """Andrew 单调链凸包，返回凸包顶点列表（按逆时针顺序）"""
    pts = sorted(points, key=lambda p: (p.point_X, p.point_Y))
    if len(pts) <= 1:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    # 合并，去掉重复的端点
    return lower[:-1] + upper[:-1]

# --------------------------- 数据读取 ----------------------------
def read_points_from_file(filepath):
    points = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                # 格式: 序号, , X, Y, Z
                name = parts[0]
                x = float(parts[2])
                y = float(parts[3])
                z = float(parts[4]) if len(parts) > 4 else 0.0
                points.append(Point(name, x, y, z))
    except Exception as e:
        print(f"读取文件出错: {e}")
    return points

# --------------------------- 绘图窗口 ----------------------------
class PlotWidget(QWidget):
    def __init__(self, all_points, hull_points):
        super().__init__()
        self.all_points = all_points      # 所有点
        self.hull_points = hull_points    # 凸包顶点（顺序）
        # 计算数据的边界，用于坐标映射
        if all_points:
            xs = [p.point_X for p in all_points]
            ys = [p.point_Y for p in all_points]
            self.x_min, self.x_max = min(xs), max(xs)
            self.y_min, self.y_max = min(ys), max(ys)
            # 留出边距
            margin_x = (self.x_max - self.x_min) * 0.1
            margin_y = (self.y_max - self.y_min) * 0.1
            self.x_min -= margin_x
            self.x_max += margin_x
            self.y_min -= margin_y
            self.y_max += margin_y
        else:
            self.x_min = self.x_max = self.y_min = self.y_max = 0

        self.setWindowTitle("点集与凸包可视化")
        self.setMinimumSize(800, 600)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 获取绘图区域大小
        rect = self.rect()
        width = rect.width()
        height = rect.height()

        # 定义映射函数：将数据坐标转为窗口坐标
        def to_screen(x, y):
            sx = (x - self.x_min) / (self.x_max - self.x_min) * width
            sy = height - (y - self.y_min) / (self.y_max - self.y_min) * height
            return int(sx), int(sy)

        # 1. 绘制所有点（灰色小圆）
        pen_point = QPen(Qt.GlobalColor.red, 1)
        painter.setPen(pen_point)
        painter.setBrush(QBrush(Qt.GlobalColor.lightGray))
        radius = 4
        for p in self.all_points:
            sx, sy = to_screen(p.point_X, p.point_Y)
            painter.drawEllipse(sx - radius//2, sy - radius//2, radius, radius)
            # 可选：显示点序号
            painter.drawText(sx + 5, sy - 3, p.point_name)

        # 2. 绘制凸包多边形（红色闭合线）
        if len(self.hull_points) >= 3:
            pen_hull = QPen(QColor(255, 0, 0), 3)
            painter.setPen(pen_hull)
            painter.setBrush(Qt.BrushStyle.NoBrush)   # 不填充
            # 构造闭合折线的坐标点列表
            poly_points = []
            for p in self.hull_points:
                sx, sy = to_screen(p.point_X, p.point_Y)
                poly_points.append((sx, sy))
            # 首尾相连
            if len(poly_points) > 1:
                for i in range(len(poly_points) - 1):
                    painter.drawLine(poly_points[i][0], poly_points[i][1],
                                     poly_points[i+1][0], poly_points[i+1][1])
                painter.drawLine(poly_points[-1][0], poly_points[-1][1],
                                 poly_points[0][0], poly_points[0][1])
        elif len(self.hull_points) == 2:
            # 只有两个点，画一条线
            p1, p2 = self.hull_points
            sx1, sy1 = to_screen(p1.point_X, p1.point_Y)
            sx2, sy2 = to_screen(p2.point_X, p2.point_Y)
            painter.drawLine(sx1, sy1, sx2, sy2)

        # 3. 额外标记凸包顶点（大红圆）
        pen_vertex = QPen(Qt.GlobalColor.red, 2)
        painter.setPen(pen_vertex)
        painter.setBrush(QBrush(QColor(255, 100, 100)))
        for p in self.hull_points:
            sx, sy = to_screen(p.point_X, p.point_Y)
            painter.drawEllipse(sx - radius, sy - radius, radius*2, radius*2)

# --------------------------- 主窗口 ----------------------------
class MainWindow(QMainWindow):
    def __init__(self, all_points, hull_points):
        super().__init__()
        self.setWindowTitle("凸包可视化")
        central_widget = PlotWidget(all_points, hull_points)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    # 读取文件（请根据实际路径修改，或放置于当前目录）
    file_path = "源/deepseek_plaintext_20260522_414bc0.txt"
    points = read_points_from_file(file_path)
    if not points:
        print("没有读取到任何点，退出")
        sys.exit(1)

    hull = convex_hull(points)          # 计算凸包
    print("凸包顶点：")
    for p in hull:
        print(p)

    app = QApplication(sys.argv)
    window = MainWindow(points, hull)
    window.show()
    sys.exit(app.exec())