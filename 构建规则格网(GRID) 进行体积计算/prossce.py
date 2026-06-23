import math
import copy
class Point:
    def __init__(self,n,x,y,z):
        self.n=n
        self.x=x
        self.y=y
        self.z=z

class Pointscllection:
    def __init__(self,H):
        self.lis_points:list[Point]=[]
        self.H=H

    def stact_count(self):
        points = sorted(self.lis_points, key=lambda p: (p.x, p.y))
        if len(points) < 3:
            return points

        # 下凸包（从左到右）
        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        # 上凸包（从右到左）
        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)

        # 合并，去掉重复的端点（下凸包最后一个点与上凸包第一个点重复，反之亦然）
        result =  upper[::-1]+lower[:-1][::-1]

        self.stact=result

        return result


    def grid_count(self,L_input):
        self.L=L_input
        stact_point = self.stact_count()

        x_min=min(stact_point,key=lambda s:s.x)
        x_max=max(stact_point,key=lambda s:s.x)
        y_min=min(stact_point,key=lambda s:s.y)
        y_max=max(stact_point,key=lambda s:s.y)

        h=y_max.y-y_min.y
        w=x_max.x-x_min.x
        P=(x_min.x,y_min.y)

        row=math.ceil(h/self.L)
        colum=math.ceil(w/self.L)

        self.lis_grid=Grids(stact_point,self.lis_points,self.L,h,w,self.H)

        ind=1
        for r in range(row):
            for c in range(colum):
                a=Grid(f'P{ind}',(P[0]+self.L*(c+1)-(self.L/2),P[1]+self.L*(r+1)-(self.L/2)))
                ind+=1
                self.lis_grid.lis_grids.append(a)

        in_stact=len(self.lis_grid.check_in_stact())
        V=sum(self.lis_grid.v_count())


        report=(f"-------------------------基本信息---------------------\n"
                f"基准高程：   {float(self.H)}\n"
                f"网格间隔：   {int(self.L)}\n"
                f"网格横格：   {row}\n"
                f"网格纵格：   {colum}\n"
                f"总网格数：   {row*colum}\n"
                f"凸包内的网格数：   {in_stact}\n"
                f"体积：  {V:.3f}\n"
                f"-----------点位信息---------\n"
                f"外包矩形的顶点坐标：   \n"
                f"X坐标       Y坐标      \n"
                f"{x_min.x:.3f}  {x_min.y:.3f}  \n"
                f"{x_max.x:.3f}  {x_max.y:.3f}  \n"
                f"{y_min.x:.3f}  {y_min.y:.3f}  \n"
                f"{y_max.x:.3f}  {y_max.y:.3f}  \n")


        return report,(x_min.x,x_max.x,y_min.y,y_max.y)

    def report(self,h,l):
        self.H=h
        r1,_=self.grid_count(1)
        r2,_=self.grid_count(5)
        r3,_=self.grid_count(10)
        self.H=h
        r5,_=self.grid_count(l)

        r_stact=("报告基点是:\n"
                 "点号           X坐标            Y坐标             H高程\n"
                 f"{self.stact[0].n}           {self.stact[0].x:.3f}      {self.stact[0].y:.3f}      {self.stact[0].z:.3f}\n"
                 "--------------------------凸包点----------------------\n"
                 "点号          X坐标           Y坐标           H高程\n")
        for i in  self.stact:
            r_stact=r_stact+f"{i.n}          {i.x:.3f}     {i.y:.3f}     {i.z:.3f}\n"


        return r1+r2+r3+r5+r_stact,self.grid_count(1)[1]


"""
4-----------3
-           -
-           -
-           -
-           -
1-----------2
"""

class Grid:
    def __init__(self,n,p3):
        self.n=n
        self.pc=(p3[0],p3[1])


class Grids:
    def __init__(self,lis_stact,lis_point,L,h,w,H):
        self.lis_grids:list[Grid]=[]
        self.lis_stact:list[Point]=lis_stact
        self.lis_point:list[Point]=lis_point
        self.L=L
        self.h=h
        self.w=w
        self.H=H


    def check_in_stact(self):
        lis_stact=self.lis_stact
        lis_grids=self.lis_grids
        self.lis_instact_p=[]

        len_s=len(lis_stact)
        for ga in lis_grids:
            num=0
            for i in range(len_s-1):
                p1=lis_stact[i]
                p2=lis_stact[i+1]
                max_y=max([p1.y,p2.y])
                min_y=min([p1.y,p2.y])
                if min_y<ga.pc[1]<max_y:
                    if count_x(p1.x,p1.y,p2.x,p2.y,ga.pc[1])>ga.pc[0]:
                        num+=1

            if num%2 !=0:
                self.lis_instact_p.append(ga)
        return self.lis_instact_p

    def v_count(self):
        lis_instact_p=self.check_in_stact()
        lis_point=self.lis_point

        re=[]
        for i in lis_instact_p:
            re.append(h_count(i,lis_point,self.H,self.L,self.h,self.w))

        v_lis=[]
        for i in re:
            print(i)
            v=((sum(i)/4-self.H)*(self.L**2))
            v_lis.append(v)

        return v_lis



def count_x(x1,y1,x2,y2,y):
    return ((x2-x1)/(y2-y1))*(y-y1)+x1


def cross(o: Point, a: Point, b: Point):
    """向量 OA × OB，正值表示 OA 到 OB 逆时针（左转）"""
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)



"""
4-----------3
-           -
-           -
-           -
-           -
1-----------2
"""
def h_count(point,ran_point,H,L,h,w):
    point1234=((point.pc[0]-(L/2),point.pc[1]-(L/2)),(point.pc[0]+(L/2),point.pc[1]-(L/2)),
               (point.pc[0]+(L/2),point.pc[1]+(L/2)),(point.pc[0]-(L/2),point.pc[1]+(L/2)))

    lis_distance=[]
    Q_lis=[]
    for i in point1234:
        lis_distance.append([])
        Q_lis.append([])
        for p in ran_point:
            d = math.hypot(i[0] - p.x, i[1] - p.y)
            if d < (h+w)*0.4:
                lis_distance[-1].append(d)
                Q_lis[-1].append(p)

    h_lis=[]
    for p in range(len(point1234)):
        up = 0
        down = 0
        for d1,z1 in zip(lis_distance[p],Q_lis[p]):
            up=(z1.z/d1)+up
            down=(1/d1)+down
        h_lis.append(up/down)


    return h_lis











