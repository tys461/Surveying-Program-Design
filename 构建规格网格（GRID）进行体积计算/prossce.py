import math

class Point:
    def __init__(self,n,x:float,y:float,z:float):
        self.n=n
        self.x=x
        self.y=y
        self.z=z

    def __repr__(self):
        return f'Grid(n={self.n}),x=({self.x}),y=({self.y}),z=({self.z})'
class Grid:
    def __init__(self,n:str,px:float,py:float):
        self.n=n
        self.p_c=(px,py,)


    @property
    def center(self):
        return Point(self.n,self.p_c[0],self.p_c[1],0)

    def __hash__(self):
        return hash(self.p_c)

    def __repr__(self):
        return f'Grid(n={self.n}),p_c=({self.p_c})'

    def __eq__(self,other):
        if not isinstance(other,Grid):
            return False
        return self.p_c==other.p_c
class ConverxHull:
    def __init__(self,vertices:list[Point]):
        self.vertices=vertices

    def __repr__(self):
        return f'{self.vertices}'

    def __contains__(self,point:Point):
        x,y=point.x,point.y
        cnt=0
        n=len(self.vertices)
        for i in range(n):
            x1,y1=self.vertices[i].x,self.vertices[i].y
            x2,y2=self.vertices[(i+1)%n].x,self.vertices[(i+1)%n].y

            if (y1>y) != (y2>y):
                x_intersect=(x2 - x1) * (y - y1) / (y2 - y1) + x1
                if x_intersect > x:
                    cnt += 1

        return cnt % 2 == 1


class Grids:
    def __init__(self,convex_hull:ConverxHull,lis_point,L,h,w,H):
        self.convex_hull=convex_hull
        self.lis_grids: list[Grid] = []
        self.lis_point: list[Point] = lis_point
        self.L = L
        self.h = h #行
        self.w = w #列
        self.H = H

    def __getitem__(self,key):
        x,y=key
        if not ( 0<= x < self.w and 0<= y <self.h):
            raise IndexError("Grid index out of range")
        idx=y*self.w+x
        return self.lis_grids[idx]

    def __setitem__(self,key,value):
        x,y=key
        if not (0<=x<self.w and 0<=y<self.h):
            raise("Grid index out of range")
        self.lis_grids[y*self.w+x]=value


    def compute_vertex_elevations_for_grids_inside_hull(self):
        self.inside_grids = [g for g in self.lis_grids if g.center in self.convex_hull]
        results={}
        half=self.L/2.0
        for grid in self.inside_grids:
            cx, cy = grid.center.x, grid.center.y
            vertices = [
                (cx - half, cy - half),  # 左下
                (cx + half, cy - half),  # 右下
                (cx - half, cy + half),  # 左上
                (cx + half, cy + half)  # 右上
            ]
            elevs = []
            for vx, vy in vertices:
                z = idw_interpolate(vx, vy, self.lis_point,self.w+self.h)
                elevs.append(z)
            results[grid] = elevs
        return results

def idw_interpolate(x, y, known_points,r):
    """
    known_points: list of Point3D 对象
    返回插值高程
    """
    total_weight = 0.0
    total_weighted_z = 0.0
    for p in known_points:
        dx = x - p.x
        dy = y - p.y
        dist = math.hypot(dx, dy)   # 欧氏距离
        if dist<0.4*(r):
            if dist == 0:
                return p.z
            weight = 1.0 / dist
            total_weight += weight
            total_weighted_z += weight * p.z
    if total_weight == 0:
        return 0.0  # 或 raise
    return total_weighted_z / total_weight

def cross(o: Point, a: Point, b: Point):
    """向量 OA × OB，正值表示 OA 到 OB 逆时针（左转）"""
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)


class Pointscllection:
    def __init__(self,H):
        self.lis_points:list[Point]=[]
        self.H=H

    def stact_count(self):
        rank_points=sorted(self.lis_points,key=lambda p:(p.x,p.y))
        if len(rank_points)<3:
            return rank_points

        upper=[]
        for p in rank_points:
            while len(upper)>=2 and cross(upper[-2],upper[-1],p)>=0:
                upper.pop()
            upper.append(p)

        lower=[]
        for p in reversed(rank_points):
            while len(lower)>=2 and cross(lower[-2],lower[-1],p)>=0:
                lower.pop()
            lower.append(p)

        self.converxHull=ConverxHull(upper[0:]+lower[:-1])
        self.stact=upper[0:]+lower[1:]
        return upper[0:]+lower[1:]

    def grid_count(self,L_input=1):
        self.L=L_input
        stact_point=self.stact_count()
        x_min=min(stact_point,key=lambda s:s.x)
        x_max=max(stact_point,key=lambda s:s.x)
        y_min=min(stact_point,key=lambda s:s.y)
        y_max=max(stact_point,key=lambda s:s.y)

        h=y_max.y-y_min.y
        w=x_max.x-x_min.x
        P=(x_min.x,y_min.y)

        row = math.ceil(h / self.L)
        colum = math.ceil(w / self.L)

        self.lis_grid = Grids(self.converxHull,self.lis_points, self.L, h, w, self.H)

        ind = 1
        for r in range(row):
            for c in range(colum):
                a = Grid(f'P{ind}', P[0] + self.L * (c + 1) - (self.L / 2), P[1] + self.L * (r + 1) - (self.L / 2),)
                ind += 1
                self.lis_grid.lis_grids.append(a)

        grid_h=self.lis_grid.compute_vertex_elevations_for_grids_inside_hull()

        V=0.0
        for i in grid_h:
            V=V+((sum(grid_h[i])/4)-self.H)*self.L**2


        report=(f"-------------------------基本信息---------------------\n"
                f"基准高程：   {float(self.H)}\n"
                f"网格间隔：   {float(self.L)}\n"
                f"网格横格：   {row}\n"
                f"网格纵格：   {colum}\n"
                f"总网格数：   {row*colum}\n"
                f"凸包内的网格数：   {len(stact_point)}\n"
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
        r1, _ = self.grid_count(1)
        r2, _ = self.grid_count(5)
        r3, _ = self.grid_count(10)
        self.H = h
        r5, _ = self.grid_count(l)

        r_stact = ("报告基点是:\n"
                   "点号           X坐标            Y坐标             H高程\n"
                   f"{self.stact[0].n}           {self.stact[0].x:.3f}      {self.stact[0].y:.3f}      {self.stact[0].z:.3f}\n"
                   "--------------------------凸包点----------------------\n"
                   "点号          X坐标           Y坐标           H高程\n")
        for i in self.stact:
            r_stact = r_stact + f"{i.n}          {i.x:.3f}     {i.y:.3f}     {i.z:.3f}\n"

        return r1 + r2 + r3 + r5 + r_stact, self.grid_count(1)[1]