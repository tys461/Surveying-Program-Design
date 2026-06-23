import math
import copy
class Point:
    def __init__(self,n,x,y):
        self.n=n
        self.x=x
        self.y=y

class Points:
    def __init__(self):
        self.points_lis:list[Point]=[]

    def closed(self):
        closed_points=copy.deepcopy(self.points_lis)
        closed_points.insert(0,closed_points[-1])
        closed_points.insert(0,closed_points[-2])
        closed_points.append(self.points_lis[0])
        closed_points.append(self.points_lis[1])
        closed_points.append(self.points_lis[2])

        return closed_points

    def unclosed(self):
        unclosed_points=copy.deepcopy(self.points_lis)
        p0=unclosed_points[0]
        p1=unclosed_points[1]
        p2=unclosed_points[2]
        pax=p2.x-3*p1.x+3*p0.x
        pay=p2.y-3*p1.y+3*p0.y
        unclosed_points.insert(0,Point('addA',pax,pay))
        pa=unclosed_points[0]
        pbx=p1.x-3*p0.x+3*pa.x
        pby=p1.y-3*p0.y+3*pa.y
        unclosed_points.insert(0,Point('addB',pbx,pby))

        p0=unclosed_points[-1]
        p1=unclosed_points[-2]
        p2=unclosed_points[-3]

        pcx = p2.x - 3 * p1.x + 3 * p0.x
        pcy = p2.y - 3 * p1.y + 3 * p0.y
        unclosed_points.append(Point('addC',pcx,pcy))
        pc=unclosed_points[-1]
        pdx = p1.x - 3 * p0.x + 3 * pc.x
        pdy = p1.y - 3 * p0.y + 3 * pc.y
        unclosed_points.append(Point('addD',pdx,pdy))



        return unclosed_points



    """pi_1:i-1  pi__2:i+2"""

    def count_a0b0(self,pi,pi_1,pi_2,pi__1,pi__2):
        a1=pi_1.x-pi_2.x
        a2=pi.x-pi_1.x
        a3=pi__1.x-pi.x
        a4=pi__2.x-pi__1.x

        b1=pi_1.y-pi_2.y
        b2=pi.y-pi_1.y
        b3=pi__1.y-pi.y
        b4=pi__2.y-pi__1.y

        w2=abs(a3*b4-a4*b3)
        w3=abs(a1*b2-a2*b1)
        # w2=a3*b4-a4*b3
        # w3=a1*b2-a2*b1

        a0=w2*a2+w3*a3
        b0=w2*b2+w3*b3

        return a0,b0


    def count_degree(self,pi,pi_1,pi_2,pi__1,pi__2):
        a0,b0=self.count_a0b0(pi,pi_1,pi_2,pi__1,pi__2)
        cosi=a0/(math.sqrt(a0**2+b0**2))
        sini=b0/(math.sqrt(a0**2+b0**2))

        return cosi,sini


    def count_EF(self,pi,pi_1,pi_2,pi__1,pi__2,pi__3):

        cosi,sini=self.count_degree(pi,pi_1,pi_2,pi__1,pi__2)
        cosi__1,sini__1=self.count_degree(pi__1,pi,pi_1,pi__2,pi__3)

        r=math.sqrt((pi__1.x-pi.x)**2+(pi__1.y-pi.y)**2)

        E0=pi.x;E2=3*(pi__1.x-pi.x)-r*(cosi__1+2*cosi)
        E1=r*cosi;E3=-2*(pi__1.x-pi.x)+r*(cosi__1+cosi)
        F0=pi.y;F2=3*(pi__1.y-pi.y)-r*(sini__1+2*sini)
        F1=r*sini;F3=-2*(pi__1.y-pi.y)+r*(sini__1+sini)


        return E0,E1,E2,E3,F0,F1,F2,F3


    def count_xy(self,pi,pi_1,pi_2,pi__1,pi__2,pi__3,z):

        E0,E1,E2,E3,F0,F1,F2,F3=self.count_EF(pi,pi_1,pi_2,pi__1,pi__2,pi__3)
        x=E0+E1*z+E2*z**2+E3*z**3
        y=F0+F1*z+F2*z**2+F3*z**3

        return (x,y),(E0,E1,E2,E3,F0,F1,F2,F3)


    def count_all(self):
        add_points=self.closed()
        l=len(self.points_lis)
        report=[]
        ni_point=[]
        for i in range(l):
            ni_point.append([])

            pi = add_points[i + 2]
            pi_1 = add_points[i + 1]
            pi_2 = add_points[i]
            pi__1 = add_points[i + 3]
            pi__2 = add_points[i + 4]
            pi__3 = add_points[i+5]

            w_id = 4  # ID列宽
            w_xy = 10  # 坐标/系数列宽
            w_float = 3  # 小数位数

            z=0.1
            for num in range(int(1/z)):
                ni_point[-1].append([pi.x,pi.y,*(self.count_xy(pi,pi_1,pi_2,pi__1,pi__2,pi__3,z)[0]),*(self.count_xy(pi,pi_1,pi_2,pi__1,pi__2,pi__3,z)[1])])
                z+=0.1
            last = ni_point[-1][-1]
            # 格式化该行
            line = (f"{i:<{w_id}} "
                    f"{last[0]:<{w_xy}.{w_float}f} "
                    f"{last[1]:<{w_xy}.{w_float}f} "
                    f"{i + 1:<{w_id}} "
                    f"{last[2]:<{w_xy}.{w_float}f} "
                    f"{last[3]:<{w_xy}.{w_float}f} "
                    f"{last[4]:<{w_xy}.{w_float}f} "
                    f"{last[5]:<{w_xy}.{w_float}f} "
                    f"{last[6]:<{w_xy}.{w_float}f} "
                    f"{last[7]:<{w_xy}.{w_float}f} "
                    f"{last[8]:<{w_xy}.{w_float}f} "
                    f"{last[9]:<{w_xy}.{w_float}f} "
                    f"{last[10]:<{w_xy}.{w_float}f} "
                    f"{last[11]:<{w_xy}.{w_float}f}")
            report.append(line)
        return ni_point, report

    def uncount_all(self):
        add_points=self.unclosed()
        l=len(self.points_lis)
        report=[]
        ni_point=[]
        for i in range(l-1):
            ni_point.append([])

            pi = add_points[i + 2]
            pi_1 = add_points[i + 1]
            pi_2 = add_points[i]
            pi__1 = add_points[i + 3]
            pi__2 = add_points[i + 4]
            pi__3 = add_points[i+5]

            w_id = 4  # ID列宽
            w_xy = 10  # 坐标/系数列宽
            w_float = 3  # 小数位数

            z=0.1
            for num in range(int(1/z)):
                ni_point[-1].append([pi.x,pi.y,*(self.count_xy(pi,pi_1,pi_2,pi__1,pi__2,pi__3,z)[0]),*(self.count_xy(pi,pi_1,pi_2,pi__1,pi__2,pi__3,z)[1])])
                z+=0.1
            last = ni_point[-1][-1]
            # 格式化该行
            line = (f"{i:<{w_id}} "
                    f"{last[0]:<{w_xy}.{w_float}f} "
                    f"{last[1]:<{w_xy}.{w_float}f} "
                    f"{i + 1:<{w_id}} "
                    f"{last[2]:<{w_xy}.{w_float}f} "
                    f"{last[3]:<{w_xy}.{w_float}f} "
                    f"{last[4]:<{w_xy}.{w_float}f} "
                    f"{last[5]:<{w_xy}.{w_float}f} "
                    f"{last[6]:<{w_xy}.{w_float}f} "
                    f"{last[7]:<{w_xy}.{w_float}f} "
                    f"{last[8]:<{w_xy}.{w_float}f} "
                    f"{last[9]:<{w_xy}.{w_float}f} "
                    f"{last[10]:<{w_xy}.{w_float}f} "
                    f"{last[11]:<{w_xy}.{w_float}f}")
            report.append(line)
        return ni_point,report

    def closereport(self):
        x_min=min(self.points_lis,key=lambda s:s.x)
        x_max=max(self.points_lis,key=lambda s:s.x)
        y_min=min(self.points_lis,key=lambda s:s.y)
        y_max=max(self.points_lis,key=lambda s:s.y)
        w_id = 4
        w_xy = 10
        header = (f"{'起点ID':<{w_id}} {'起点x':<{w_xy}} {'起点y':<{w_xy}} "
                  f"{'终点ID':<{w_id}}  {'终点x':<{w_xy}} {'终点y':<{w_xy}} "
                  f"{'p0':<{w_xy}} {'p1':<{w_xy}} {'p2':<{w_xy}} {'p3':<{w_xy}} "
                  f"{'q0':<{w_xy}} {'q1':<{w_xy}} {'q2':<{w_xy}} {'q3':<{w_xy}}")

        re = ("结果报告\n"
              "------------基本信息------------\n"
              f"总点数:{len(self.points_lis)}\n"
              f"x边界:{x_min.x}至{x_max.x}\n"
              f"y边界:{y_min.y}至{y_max.y}\n"
              f"是否闭合:是\n\n"
              "------------计算结果------------\n"
              "说明:两点之间的曲线方程为:\n"
              "x=p0+p1*z+p2*z*z+p3*z*z*z\n"
              "y=q0+q1*z+q2*z*z+q3*z*z*z\n"
              "其中z为两点之间的弦长变量[0,1]\n"
              f"{header}\n")

        report = self.count_all()[-1]
        for line in report:
            re += line + "\n"
        return re,self.count_all()[0]

    def unclosereport(self):
        x_min = min(self.points_lis, key=lambda s: s.x)
        x_max = max(self.points_lis, key=lambda s: s.x)
        y_min = min(self.points_lis, key=lambda s: s.y)
        y_max = max(self.points_lis, key=lambda s: s.y)

        w_id = 4
        w_xy = 10
        header = (f"{'起点ID':<{w_id}} {'起点x':<{w_xy}} {'起点y':<{w_xy}} "
                  f"{'终点ID':<{w_id}} {'终点x':<{w_xy}} {'终点y':<{w_xy}} "
                  f"{'p0':<{w_xy}} {'p1':<{w_xy}} {'p2':<{w_xy}} {'p3':<{w_xy}} "
                  f"{'q0':<{w_xy}} {'q1':<{w_xy}} {'q2':<{w_xy}} {'q3':<{w_xy}}")

        re = ("结果报告\n"
              "------------基本信息------------\n"
              f"总点数:{len(self.points_lis)}\n"
              f"x边界:{x_min.x}至{x_max.x}\n"
              f"y边界:{y_min.y}至{y_max.y}\n"
              f"是否闭合:否\n\n"
              "------------计算结果------------\n"
              "说明:两点之间的曲线方程为:\n"
              "x=p0+p1*z+p2*z*z+p3*z*z*z\n"
              "y=q0+q1*z+q2*z*z+q3*z*z*z\n"
              "其中z为两点之间的弦长变量[0,1]\n"
              f"{header}\n")

        report = self.uncount_all()[-1]
        for line in report:
            re += line + "\n"
        return re,self.uncount_all()[0]


def addpoint(p1,p2,p3):
    x=(p3.x-p2.x)-(p2.x-p1.x)
    y=(p3.y-p2.y)-(p2.y-p1.y)

    return Point('add',x,y)