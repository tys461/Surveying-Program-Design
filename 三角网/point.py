import math
from PyQt6.QtCore import QFile,QTextStream,QIODevice


"""定义点类"""
class Point:
    def __init__(self,point_name,point_X,point_Y,point_Z=0.0):
        self.point_name=point_name
        self.point_X=point_X
        self.point_Y=point_Y
        self.point_Z=point_Z



    def __repr__(self):
        return f'({self.point_X:.4f},{self.point_Y},{self.point_Z})'

    def __eq__(self,other):
        return abs(self.point_X - other.x) < 1e-8 and abs(self.point_Y - other.y) < 1e-8

class Line:
    def __init__(self,p1,p2):
        self.p1=p1
        self.p2=p2
        self.dx=p2.point_X - p1.point_X
        self.dy=p2.point_Y - p1.point_Y
        self.length=math.hypot(self.dx,self.dy)

    def azimuth(self):
        ang_rad = math.atan2(self.dx, self.dy)
        ang_deg = math.degrees(ang_rad)
        if ang_deg < 0:
            ang_deg += 360
        return ang_deg

# class Triangle:
#     def __init__(self,a,b,c):
#         self.a=a
#         self.b=b
#         self.c=c
#         self.__update_circumcircle()
#
#     def __update_circumcircle(self):
#         ax,ay=self.a.point_X,self.a.point_Y
#         bx,by=self.b.point_X,self.b.point_Y
#         cx,cy=self.c.point_X,self.c.point_Y
#         d = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
#         if abs(d) < 1e-12:
#             self.cx = self.cy = float('inf')
#             self.r2 = float('inf')
#             return
#         ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
#         uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
#         self.cx = ux
#         self.cy = uy
#         self.r2 = (ax - ux) * (ax - ux) + (ay - uy) * (ay - uy)



# ------------------------------------------------------------
# 凸包算法 (Andrew 单调链)
# ------------------------------------------------------------
def cross(o, a, b):
    return (a.point_X - o.point_X)*(b.point_Y - o.point_Y) - (a.point_Y - o.point_Y)*(b.point_X - o.point_X)

def convex_hull(points):
    pts = sorted(points, key=lambda p: (p.point_X, p.point_X))
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


def opne():
    point_list=[]
    file=QFile('源/deepseek_plaintext_20260522_414bc0.txt')
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件读取错误')
        return

    stream=QTextStream(file)
    while not stream.atEnd():
        line=stream.readLine()
        part=line.split(',')
        point_list.append(Point(part[0],float(part[2]),float(part[3]),float(part[4])))

    return point_list


lsi=opne()
print(convex_hull(lsi))

