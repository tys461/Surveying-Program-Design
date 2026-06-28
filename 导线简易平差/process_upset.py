import math
from dataclasses import dataclass
@dataclass(slots=True)
class Point:
    """定义基本点类"""
    n:str
    x:float
    y:float
    z:float

@dataclass(slots=True)
class KeyPoint:
    """定义关键点类"""
    n:str
    x:float
    y:float
    z:float=0
    distance:float=0


class Points:
    """定义点集类"""
    def __init__(self,H0:float,lis_AB:(str,float,float),lis_points:list[Point],lis_key_points:list[KeyPoint]):
        self.H0=H0
        self.lis_AB=lis_AB
        self.lis_points=lis_points
        self.lis_key_points=lis_key_points
        self.cross_distance=self.__cross_section_distance(lis_key_points)


    def __cross_section_distance(self,data):
        """计算纵断面长度 直接开始初始化"""
        distance=0
        for idx in range(len(data)-1):
            distance+=math.hypot(data[idx].x-data[idx+1].x,data[idx].y-data[idx+1].y)
        return float(f'{distance:.3f}')


    def calculate_azimuth_angles(self):
        """计算AB方位角"""
        A=self.lis_AB[0]
        B=self.lis_AB[1]

        bata_x=B[1]-A[1]
        bata_y=B[2]-A[2]

        degree=math.degrees(math.atan2(bata_y,bata_x))
        d=int(degree)
        m=(degree-d)*60
        s=(m-int(m))*60

        return f'{d}⁰{m:.2f}\"{s:.4f}\"'

    def __calculation_interpolation_point(self, inter_p:Point or KeyPoint, points:list[Point]):
        """这里改为计算单个点的高程"""
        distance_lis = []

        for p in points:
            d = math.hypot(inter_p.x - p.x, inter_p.y - p.y)
            if d != 0:
                distance_lis.append((p, d))

        distance_lis.sort(key=lambda p: p[1])
        int_p_lis = distance_lis[0:5]

        sum_up = sum(map(lambda p: (p[0].z / p[1]), int_p_lis))
        sum_down = sum(map(lambda p: (1 / p[1]), int_p_lis))

        return float(f'{sum_up/sum_down:.3f}'),int_p_lis

    def __calculation_cross_sectional_area(self,p1:Point,p2:Point):
        """断面面积计算  这里改为计算单个梯形面积"""
        bata_l=math.hypot(p1.x-p2.x,p1.y-p2.y)
        s=(p1.z+p2.z-2*self.H0)*bata_l/2
        return float(f'{s:.3f}')


    def __inter_fun1(self,intervals,k0,k1,count):
        """第一种算法 当Pi在K0和K1之间时"""
        distance = math.hypot(k0.x - k1.x, k0.y - k1.y)
        angle_rad=math.atan2((k1.y-k0.y),(k1.x-k0.x))
        inter_p_count=int(distance//intervals)
        lis_inter_p:list[(KeyPoint,list)]=[]

        for idx_p in range(inter_p_count):
            x=k0.x+intervals*(count+1)*math.cos(angle_rad)
            y=k0.y+intervals*(count+1)*math.sin(angle_rad)
            inter_point=KeyPoint(f'inter_k{count+1}',float(f'{x:.3f}'),float(f'{y:.3f}'),0,intervals*(count+1))
            z,p=self.__calculation_interpolation_point(inter_point,self.lis_points)
            inter_point.z=z
            lis_inter_p.append((inter_point,p))
            count+=1
        return lis_inter_p,count

    def __inter_fun2(self,intervals,k0,k1,count,D):
        """第二种算法 当Pi不是在K0和K1之间时"""
        distance = math.hypot(k0.x - k1.x, k0.y - k1.y)
        angle_rad=math.atan2((k1.y-k0.y),(k1.x-k0.x))
        inter_p_count=int(distance//intervals)
        lis_inter_p:list[(KeyPoint,list)]=[]

        for idx_p in range(inter_p_count):
            x=k0.x+(intervals*(count+1)-D)*math.cos(angle_rad)
            y=k0.y+(intervals*(count+1)-D)*math.sin(angle_rad)
            inter_point=KeyPoint(f'inter_k{count+1}',float(f'{x:.3f}'),float(f'{y:.3f}'),0,intervals*(count+1))
            z,p=self.__calculation_interpolation_point(inter_point,self.lis_points)
            inter_point.z=z
            lis_inter_p.append((inter_point,p))
            count+=1
        return lis_inter_p,count
    def calculation_inter_point(self):
        """计算内插点的平面坐标"""
        lis_inter_all_p = []
        ran=len(self.lis_key_points)
        k_i_1=None
        count=0
        for idx in range(ran-1):
            k_i=self.lis_key_points[idx]
            k_i_1=self.lis_key_points[idx+1]
            if k_i.n=='K0':
                k_i.distance=count*10
                r,count=self.__inter_fun1(10,k_i,k_i_1,count)
                lis_inter_all_p.append(k_i)
                lis_inter_all_p.extend(r)

            else:
                D = math.hypot(k_i.x - self.lis_key_points[0].x, k_i.y - self.lis_key_points[0].y)
                k_i.distance =float(f'{D:.3f}')
                r,count=self.__inter_fun2(10,k_i,k_i_1,count,D)
                lis_inter_all_p.append(k_i)
                lis_inter_all_p.extend(r)
        k_i_1.distance=self.cross_distance
        lis_inter_all_p.append(k_i_1)

        return lis_inter_all_p


    def __calculation_center_p(self):
        """计算纵断面的中心点"""
        ran=len(self.lis_key_points)
        result=[]
        for idx in range(ran-1):
            p1=self.lis_key_points[idx]
            p2=self.lis_key_points[idx+1]

            x_m=(p1.x+p2.x)/2
            y_m=(p1.y+p2.y)/2

            result.append((f'M{idx}',x_m,y_m))

        return result

    def calculate_plane_coordinates_elevations_cross_section_interpolation(self):
        """计算横断面插值的平面坐标和高程  我靠书上给的算法和参考程序使用的算法根本不一样😒😒😒 这里我按书上的来"""

        center_p=self.__calculation_center_p()

        dic_inter_m:dict={str:[Point]}
        dic_area:dict={str:float}

        ran=len(center_p)
        for idx in range(ran-1):
            m1=center_p[idx]
            m2=center_p[idx+1]

            angle_rad=math.atan2(m1[2]-m2[2],m1[1]-m2[1])+math.radians(90)

            for j in range(-5,6):
                x = m1[1] + j*5 * math.cos(angle_rad)
                y = m1[2] + j*5 * math.sin(angle_rad)
                p=Point(f'inter_m{6 + j}', x, y, 0)
                z,_ = self.__calculation_interpolation_point(p, self.lis_points)
                p.z=z
                lis_inter_m=dic_inter_m.get(m1[0],[])
                lis_inter_m.append(p)
                dic_inter_m[m1[0]]=lis_inter_m


        m1 = center_p[-1]
        m2 = center_p[-2]
        angle_rad = math.atan2(m1[2] - m2[2], m1[1] - m2[1]) + math.radians(90)

        for j in range(-5, 6):
            x = m1[1] + j * 5 * math.cos(angle_rad)
            y = m1[2] + j * 5 * math.sin(angle_rad)
            p = Point(f'inter_m{6 + j}', x, y, 0)
            z, _ = self.__calculation_interpolation_point(p, self.lis_points)
            p.z = z
            lis_inter_m = dic_inter_m.get(m1[0], [])
            lis_inter_m.append(p)
            dic_inter_m[m1[0]] = lis_inter_m


        for k,v in dic_inter_m.items():
            lis_area=[]
            ran=len(v)
            for idx in range(ran-1):
                area=self.__calculation_cross_sectional_area(v[idx],v[idx+1])
                lis_area.append(area)
            _area=sum(lis_area)
            _dic_area=dic_area.get(k,_area)
            dic_area[k]=_dic_area



        return dic_inter_m,dic_area



