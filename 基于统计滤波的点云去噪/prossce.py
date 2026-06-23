import math

class Point:
   def __init__(self,n,x,y,z):
       self.n=n
       self.x=x
       self.y=y
       self.z=z

   def __repr__(self):
       return f"({self.n}:x={self.x} y={self.y} z={self.z})"



   def __eq__(self,other):
       if not isinstance(other,Point):
            return False
       return other.x==self.x and other.z==self.z and other.y==self.y



class LisPoints:
    def __init__(self):
        self.lis_points:list[Point]=[]


    @property
    def max_point_x(self):
        return max(self.lis_points,key=lambda p : p.x).x

    @property
    def max_point_y(self):
        return max(self.lis_points,key=lambda p : p.y).y
    @property
    def max_point_z(self):
        return max(self.lis_points,key=lambda p : p.z).z

    @property
    def min_point_x(self):
        return min(self.lis_points, key=lambda p: p.x).x

    @property
    def min_point_y(self):
        return min(self.lis_points, key=lambda p: p.y).y

    @property
    def min_point_z(self):
        return min(self.lis_points, key=lambda p: p.z).z



class Grids:
    def __init__(self,lisPoints:LisPoints):
        self.lisPoints = lisPoints
        self.set_grids()


    def set_grids(self):
        self.max_x=self.lisPoints.max_point_x
        self.max_y=self.lisPoints.max_point_y
        self.max_z=self.lisPoints.max_point_z
        self.min_x=self.lisPoints.min_point_x
        self.min_y=self.lisPoints.min_point_y
        self.min_z=self.lisPoints.min_point_z
        self.grids={}
        self.point_to_grid = {}
        self.n_to_point = {}

        seta=3
        xmax1=math.floor(((self.max_x-self.min_x)/seta)+1)*seta+self.min_x
        ymay1=math.floor(((self.max_y-self.min_y)/seta)+1)*seta+self.min_y
        zmaz1=math.floor(((self.max_z-self.min_z)/seta)+1)*seta+self.min_z

        print(f"xmax1{xmax1},ymay1{ymay1},zmaz1{zmaz1}")

        for p in self.lisPoints.lis_points:
            self.n_to_point[p.n] = p
            i=math.floor((p.x-self.min_x)/3)
            j=math.floor((p.y-self.min_y)/3)
            k=math.floor((p.z-self.min_z)/3)

            lis_p = self.grids.get((i, j, k), [])
            lis_p.append(p)
            self.grids[(i,j,k)]=lis_p
            self.point_to_grid[p.n]=(i, j, k)

        return xmax1,ymay1,zmaz1

    def distance(self,p1,p2):
        x1=p1.x
        y1=p1.y
        z1=p1.z
        x2=p2.x
        y2=p2.y
        z2=p2.z

        return p2.n,math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)


    def k_resech(self,grid,point):
        x_c=grid[0]-1
        y_c=grid[1]-1
        z_c=grid[2]-1
        reuslt=[]
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    point_lis=self.grids.get((x_c+x,y_c+y,z_c+z))
                    if  point_lis != None:
                        for i in point_lis:
                            if i != point:
                                dis=self.distance(point,i)
                                reuslt.append(dis)
                    else:
                        continue

        reuslt.sort(key=lambda p:p[1])
        return reuslt


    def count_mu_zata(self,point):
        grid = self.point_to_grid.get(point)
        if grid is None:
            return 0, 0
        p = self.n_to_point[point]  # 也需要一个编号到对象的映射
        dis_lis = self.k_resech(grid, p)
        mu=sum(i[1] for i in dis_lis[0:6])/6
        a=sum((1/6)*(i[1]-mu)**2 for i in dis_lis[0:6])
        zata=math.sqrt(a)
        return mu,zata

    def count_mu_zata_all(self, k, p):
        dis_lis = self.k_resech(k, p)
        n = min(6, len(dis_lis))  # 实际邻居数
        if n == 0:
            return 0.0, 0.0
        mu = sum(d[1] for d in dis_lis[:n]) / n  # 用实际邻居数作分母
        var = sum((d[1] - mu) ** 2 for d in dis_lis[:n]) / n
        zata = math.sqrt(var)
        return mu, zata

    def count_all(self):
        u_list = []  # 只存储每个点的 u，不存储 zata
        for k, v in self.grids.items():
            for p in v:
                u, _ = self.count_mu_zata_all(k, p)  # 只取 u
                u_list.append(u)

        mu_all = sum(u_list) / len(u_list)
        # 计算 u_list 的总体标准差
        variance = sum((x - mu_all) ** 2 for x in u_list) / len(u_list)
        sigma = math.sqrt(variance)  # 这是正确的全局标准差

        threshold = mu_all + 2 * sigma

        print(mu_all,sigma,threshold)

        p1=self.count_mu_zata(1)
        p6=self.count_mu_zata(6)

        li_red=[]
        li_wirte=[]
        for i in self.lisPoints.lis_points:
            # print(i.n)
            p=self.count_mu_zata(i.n)
            if p[0]>threshold:
                li_red.append(i)
            else:
                li_wirte.append(i)



