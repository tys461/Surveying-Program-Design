import math
from dataclasses import dataclass

@dataclass(slots=True)
class Point:
    """定义点类"""
    n:str
    x:float
    y:float
    z:float
    distan:float=0


    def __repr__(self):
        return f'n:{self.n} x:{self.x} y:{self.y} z:{self.z} distance={self.distan} '


class Points:
    """"定义点集类"""
    def __init__(self,lis_point:list[Point],H0:float,key_points:list[Point],azimuth_p:list[list]):
        self.lis_points=lis_point
        self.H0=H0
        self.key_points=key_points
        self.azimuth_p=azimuth_p
        self.cross_section_distance=self.__cross_section_distance(key_points)


    def __cross_section_distance(self,data):
        """计算纵断面长度 直接开始初始化"""
        distance=0
        for idx in range(len(data)-1):
            distance+=math.hypot(data[idx].x-data[idx+1].x,data[idx].y-data[idx+1].y)
        return distance




    def calculate_azimuth_angles(self):
        """计算AB方位角"""
        A=self.azimuth_p[0]
        B=self.azimuth_p[1]

        bata_x=B[1]-A[1]
        bata_y=B[2]-A[2]

        degree=math.degrees(math.atan2(bata_y,bata_x))
        d=int(degree)
        m=(degree-d)*60
        s=(m-int(m))*60

        return f'{d}⁰{m:.2f}\"{s:.4f}\"'

    def __calculation_interpolation_point(self,inter_p,points):
        """内差点K的高程值计算  题目恶心不单独计算K0了"""
        distance_lis=[]

        for p in points:
            d=math.hypot(inter_p.x-p.x,inter_p.y-p.y)
            if d !=0:
                distance_lis.append((p,d))

        distance_lis.sort(key=lambda p:p[1])
        int_p_lis=distance_lis[0:5]

        sum_up=sum(map(lambda p:(p[0].z/p[1]),int_p_lis))
        sum_down=sum(map(lambda p:(1/p[1]),int_p_lis))

        return sum_up/sum_down


    def calculation_cross_sectional_area(self,data):
        """断面面积计算  老阴了这题目，不单独计算以k0和k1为端的断面面积了
           其实我也可以吧数据结构改为分段的，太麻烦了不想改了
        """
        lis_area=[]
        ran=len(data)
        for idx in range(0,ran-1):
            p1=data[idx]
            p2=data[idx+1]
            print(p1.n)
            bata_l=math.hypot(p1.x-p2.x,p1.y-p2.y)
            s=(p1.z+p2.z-2*self.H0)*bata_l/2
            lis_area.append(s)
        return sum(lis_area),len(lis_area)

    def __inter_fun1(self,intervals,k0,k1,count):
        """第一种算法 当Pi在K0和K1之间时"""
        distance = math.hypot(k0.x - k1.x, k0.y - k1.y)
        angle_rad=math.atan2((k1.y-k0.y),(k1.x-k0.x))
        inter_p_count=int(distance//intervals)
        lis_inter_p:list[Point]=[]

        for idx_p in range(inter_p_count):
            x=k0.x+intervals*(count+1)*math.cos(angle_rad)
            y=k0.y+intervals*(count+1)*math.sin(angle_rad)
            z=self.__calculation_interpolation_point(Point('inter',x,y,0),self.lis_points)
            lis_inter_p.append(Point(f'inter_K{count+1}',x,y,z,intervals*(count+1)))
            count+=1
        return lis_inter_p,count

    def __inter_fun2(self,intervals,k0,k1,count,D):
        """第二种算法 当Pi不是在K0和K1之间时"""
        distance = math.hypot(k0.x - k1.x, k0.y - k1.y)
        angle_rad=math.atan2((k1.y-k0.y),(k1.x-k0.x))
        inter_p_count=int(distance//intervals)
        lis_inter_p:list[Point]=[]

        for idx_p in range(inter_p_count):
            x=k0.x+(intervals*(count+1)-D)*math.cos(angle_rad)
            y=k0.y+(intervals*(count+1)-D)*math.sin(angle_rad)
            z=self.__calculation_interpolation_point(Point('inter',x,y,0),self.lis_points)
            lis_inter_p.append(Point(f'inter_K{count+1}',x,y,z,intervals*(count+1)))
            count+=1
        return lis_inter_p,count

    def calculation_inter_point(self):
        """计算内插点的平面坐标"""
        lis_inter_all_p = []
        ran=len(self.key_points)
        k_i_1=None
        count=0
        for idx in range(ran-1):
            k_i=self.key_points[idx]
            k_i_1=self.key_points[idx+1]
            if k_i.n=='K0':
                k_i.distan=count*10
                r,count=self.__inter_fun1(10,k_i,k_i_1,count)
                lis_inter_all_p.append(k_i)
                lis_inter_all_p.extend(r)

            else:
                D = math.hypot(k_i.x - self.key_points[0].x, k_i.y - self.key_points[0].y)
                k_i.distan =D
                r,count=self.__inter_fun2(10,k_i,k_i_1,count,D)
                lis_inter_all_p.append(k_i)
                lis_inter_all_p.extend(r)
        k_i_1.distan=self.cross_section_distance
        lis_inter_all_p.append(k_i_1)

        return lis_inter_all_p

    def __calculation_center_p(self):
        """计算纵断面的中心点"""
        ran=len(self.key_points)
        result=[]
        for idx in range(ran-1):
            p1=self.key_points[idx]
            p2=self.key_points[idx+1]

            x_m=(p1.x+p2.x)/2
            y_m=(p1.y+p2.y)/2

            result.append((x_m,y_m))

        return result


    def calc_cross_angle(self,x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        A_route = math.atan2(dy, dx)  # rad
        A_route_deg = math.degrees(A_route)
        if A_route_deg < 0:
            A_route_deg += 360
        A_cross = A_route_deg + 90
        if A_cross >= 360:
            A_cross -= 360
        return A_cross

    def calculate_plane_coordinates_elevations_cross_section_interpolation(self):
        """计算横断面插值的平面坐标和高程"""
        calculation_center_p=self.__calculation_center_p()
        lis_inter_m=[]


        m0=((self.key_points[0].x+self.key_points[1].x)/2,(self.key_points[0].y+self.key_points[1].y)/2)
        m1=((self.key_points[1].x+self.key_points[2].x)/2,(self.key_points[1].y+self.key_points[2].y)/2)

        angle_rad=math.atan2(m1[1]-m0[1],m1[0]-m0[0])+math.radians(90)

        for idx in range(-5,6):
            x=m0[0]+idx*math.cos(angle_rad)
            y=m0[1]+idx*math.sin(angle_rad)
            z=self.__calculation_interpolation_point(Point(f'inter_m{6+idx}',x,y,0),self.lis_points)
            lis_inter_m.append(Point(f'inter_m{6+idx}',x,y,z))
        return lis_inter_m














