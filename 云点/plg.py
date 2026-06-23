import math
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 基本几何类
# ------------------------------------------------------------
class Point:
    def __init__(self, x, y, h=0.0):
        self.x = x
        self.y = y
        self.h = h

    def __repr__(self):
        return f"({self.x:.4f}, {self.y:.4f}, {self.h:.4f})"

    def __eq__(self, other):
        return abs(self.x - other.x) < 1e-8 and abs(self.y - other.y) < 1e-8


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.dx = p2.x - p1.x
        self.dy = p2.y - p1.y
        self.length = math.hypot(self.dx, self.dy)

    def azimuth(self):
        ang_rad = math.atan2(self.dx, self.dy)
        ang_deg = math.degrees(ang_rad)
        if ang_deg < 0:
            ang_deg += 360
        return ang_deg


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self._update_circumcircle()

    def _update_circumcircle(self):
        ax, ay = self.a.x, self.a.y
        bx, by = self.b.x, self.b.y
        cx, cy = self.c.x, self.c.y
        d = 2.0 * (ax*(by - cy) + bx*(cy - ay) + cx*(ay - by))#计算三角形外心
        if abs(d) < 1e-12:
            self.cx = self.cy = float('inf')
            self.r2 = float('inf')
            return
        ux = ((ax*ax + ay*ay)*(by - cy) + (bx*bx + by*by)*(cy - ay) + (cx*cx + cy*cy)*(ay - by)) / d
        uy = ((ax*ax + ay*ay)*(cx - bx) + (bx*bx + by*by)*(ax - cx) + (cx*cx + cy*cy)*(bx - ax)) / d
        self.cx = ux
        self.cy = uy
        self.r2 = (ax - ux)*(ax - ux) + (ay - uy)*(ay - uy)

    def contains_point_in_circumcircle(self, p):
        dx = p.x - self.cx
        dy = p.y - self.cy
        return dx*dx + dy*dy <= self.r2 + 1e-9

    def vertices(self):
        return [self.a, self.b, self.c]

    def area(self):
        return abs((self.b.x - self.a.x)*(self.c.y - self.a.y) -
                   (self.c.x - self.a.x)*(self.b.y - self.a.y)) / 2.0


# ------------------------------------------------------------
# 凸包算法 (Andrew 单调链)
# ------------------------------------------------------------
def cross(o, a, b):
    return (a.x - o.x)*(b.y - o.y) - (a.y - o.y)*(b.x - o.x)#

def convex_hull(points):
    pts = sorted(points, key=lambda p: (p.x, p.y))
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
    return lower[:-1] + upper[:-1]

def polygon_area(poly):
    if len(poly) < 3:
        return 0.0
    s = 0.0
    n = len(poly)
    for i in range(n):
        p1 = poly[i]
        p2 = poly[(i+1) % n]
        s += p1.x * p2.y - p2.x * p1.y
    return abs(s) / 2.0

# ------------------------------------------------------------
# Bowyer-Watson Delaunay
# ------------------------------------------------------------
def bowyer_watson(points):
    if len(points) < 3:
        return []
    min_x = min(p.x for p in points)
    min_y = min(p.y for p in points)
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)
    dx = max_x - min_x
    dy = max_y - min_y
    dmax = max(dx, dy)
    mid_x = (min_x + max_x) / 2.0
    mid_y = (min_y + max_y) / 2.0
    big_val = dmax * 10
    p1 = Point(mid_x - big_val, mid_y - big_val)
    p2 = Point(mid_x + big_val, mid_y - big_val)
    p3 = Point(mid_x, mid_y + big_val)
    super_tri = Triangle(p1, p2, p3)
    triangles = [super_tri]

    for p in points:
        bad = [tri for tri in triangles if tri.contains_point_in_circumcircle(p)]
        edge_count = {}
        for tri in bad:
            verts = tri.vertices()
            for i in range(3):
                a = verts[i]
                b = verts[(i+1)%3]
                key = (a, b) if id(a) < id(b) else (b, a)
                edge_count[key] = edge_count.get(key, 0) + 1
        boundary = [edge for edge, cnt in edge_count.items() if cnt == 1]
        triangles = [t for t in triangles if t not in bad]
        for a, b in boundary:
            triangles.append(Triangle(a, b, p))

    result = []
    for tri in triangles:
        verts = tri.vertices()
        if any(v is p1 or v is p2 or v is p3 for v in verts):
            continue
        result.append(tri)
    return result

# ------------------------------------------------------------
# 图形界面应用
# ------------------------------------------------------------
class App:
    def __init__(self, master):
        self.master = master
        master.title("凸包与Delaunay三角剖分")
        master.geometry("1000x700")

        # 数据存储
        self.points = []      # 所有原始点
        self.hull = []        # 凸包顶点（顺序）
        self.triangles = []   # Delaunay三角形

        # 控制按钮框架
        frame = tk.Frame(master)
        frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        btn_load = tk.Button(frame, text="1. 加载点文件", command=self.load_file)
        btn_load.pack(side=tk.LEFT, padx=5)

        btn_convex = tk.Button(frame, text="2. 计算凸包并绘制", command=self.plot_convex)
        btn_convex.pack(side=tk.LEFT, padx=5)

        btn_delaunay = tk.Button(frame, text="3. 生成Delaunay并保存SJW", command=self.save_delaunay)
        btn_delaunay.pack(side=tk.LEFT, padx=5)

        self.info_label = tk.Label(frame, text="状态: 请加载点文件", fg="blue")
        self.info_label.pack(side=tk.LEFT, padx=20)

        # Matplotlib 图形区域
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 工具栏（缩放、平移等）
        toolbar = NavigationToolbar2Tk(self.canvas, master)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def load_file(self):
        filename = filedialog.askopenfilename(
            title="选择点文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if not filename:
            return
        try:
            points = []
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(',')
                    if len(parts) >= 2:
                        x = float(parts[2])
                        y = float(parts[3])
                        h = float(parts[4]) if len(parts) > 2 else 0.0
                        points.append(Point(x, y, h))

            if len(points) < 3:
                messagebox.showerror("错误", "至少需要3个点")
                return
            self.points = points
            self.hull = []
            self.triangles = []
            self.info_label.config(text=f"已加载 {len(points)} 个点", fg="green")
            # 清空绘图并显示所有原始点
            self.ax.clear()
            self.ax.set_aspect('equal')
            self.ax.grid(True, linestyle='--', alpha=0.6)
            xs = [p.x for p in self.points]
            ys = [p.y for p in self.points]
            self.ax.scatter(xs, ys, c='blue', s=30, zorder=5, label='原始点')
            self.ax.set_title(f"点集 (共{len(points)}点) - 未计算凸包")
            self.ax.legend()
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("错误", f"读取文件失败:\n{str(e)}")

    def plot_convex(self):
        if not self.points:
            messagebox.showwarning("警告", "请先加载点文件")
            return
        # 计算凸包
        self.hull = convex_hull(self.points)
        if len(self.hull) < 3:
            messagebox.showerror("错误", "所有点共线，无法构成凸包")
            return
        area_hull = polygon_area(self.hull)

        # 重新绘图
        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.6)

        # 绘制所有原始点
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        self.ax.scatter(xs, ys, c='blue', s=30, zorder=5, label='原始点')

        # 绘制凸包多边形
        hull_x = [p.x for p in self.hull] + [self.hull[0].x]
        hull_y = [p.y for p in self.hull] + [self.hull[0].y]
        self.ax.plot(hull_x, hull_y, 'r-', linewidth=2, label='凸包边界')

        # 标注每条边的边长和方位角
        n = len(self.hull)
        for i in range(n):
            p1 = self.hull[i]
            p2 = self.hull[(i+1) % n]
            line = Line(p1, p2)
            # 计算边中点
            mx = (p1.x + p2.x) / 2
            my = (p1.y + p2.y) / 2
            # 文本内容
            text = f"L={line.length:.2f}\nAz={line.azimuth():.1f}°"
            self.ax.text(mx, my, text, fontsize=8,
                         ha='center', va='center',
                         bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.2'),
                         color='darkred')

        # 显示面积信息
        self.ax.set_title(f"凸包多边形  面积 = {area_hull:.4f}")
        self.ax.legend()
        self.canvas.draw()

        # 更新状态栏信息
        self.info_label.config(text=f"凸包顶点数: {len(self.hull)}  面积: {area_hull:.4f}", fg="blue")

        # 同时打印边信息到控制台（供参考）
        print("\n=== 凸包边信息 ===")
        for i in range(n):
            p1 = self.hull[i]
            p2 = self.hull[(i+1)%n]
            line = Line(p1, p2)
            print(f"边 {i+1}: 长度={line.length:.4f}, 方位角={line.azimuth():.2f}°")

    def save_delaunay(self):
        if not self.points:
            messagebox.showwarning("警告", "请先加载点文件")
            return
        # 执行 Bowyer-Watson
        self.info_label.config(text="正在执行 Delaunay 三角剖分...", fg="orange")
        self.master.update()
        try:
            self.triangles = bowyer_watson(self.points)
        except Exception as e:
            messagebox.showerror("错误", f"三角剖分失败:\n{str(e)}")
            self.info_label.config(text="三角剖分失败", fg="red")
            return

        if not self.triangles:
            messagebox.showwarning("警告", "未生成任何三角形（点数不足或共线）")
            return

        # 保存为 sjw 文件
        filename = filedialog.asksaveasfilename(
            defaultextension=".sjw",
            filetypes=[("SJW文件", "*.sjw"), ("所有文件", "*.*")]
        )
        if not filename:
            return
        try:
            with open(filename, 'w') as f:
                for tri in self.triangles:
                    for v in tri.vertices():
                        f.write(f"{v.x:.6f} {v.y:.6f} {v.h:.6f}\n")
                    f.write("\n")
        except Exception as e:
            messagebox.showerror("错误", f"保存文件失败:\n{str(e)}")
            return

        # 计算总表面积
        total_area = sum(t.area() for t in self.triangles)
        self.info_label.config(text=f"Delaunay 完成: {len(self.triangles)} 个三角形, 总表面积 {total_area:.4f}", fg="green")
        messagebox.showinfo("成功", f"Delaunay 三角网已保存至:\n{filename}\n三角形数量: {len(self.triangles)}\n总表面积: {total_area:.4f}")

        # 可选：在图形上叠加显示三角网（为清晰，不自动显示，避免覆盖凸包；可增加复选框，此处简单处理）
        # 若需要可取消注释以下代码，会绘制所有三角形边线（灰色）
        # self.ax.clear()
        # self.ax.set_aspect('equal')
        # xs = [p.x for p in self.points]
        # ys = [p.y for p in self.points]
        # self.ax.scatter(xs, ys, c='blue', s=30)
        # for tri in self.triangles:
        #     verts = tri.vertices()
        #     for i in range(3):
        #         p1 = verts[i]
        #         p2 = verts[(i+1)%3]
        #         self.ax.plot([p1.x, p2.x], [p1.y, p2.y], 'g-', linewidth=0.8)
        # self.canvas.draw()


# ------------------------------------------------------------
# 主程序入口
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()