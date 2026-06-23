import math

class Time:
    def __init__(self,y,mm,d,h,m,s):
        self.y=y
        self.mm=mm
        self.d=d
        self.h=h
        self.m=m
        self.s=s



class Point:
    def __init__(self,n,xs,ys,zs):
        self.n=n
        self.x=xs*1000
        self.y=ys*1000
        self.z=zs*1000




class PointCollection:
    def __init__(self,time):
        self.time=time
        self.points:list[Point]=[]
        self.Bp_deg = 30
        self.Lp_deg = 114
        self.Bp = math.radians(30)
        self.Lp = math.radians(114)
        self.A1=5e-9
        self.A3=50400.0
        self.af1 = 0.1397e-7  # α0
        self.af2 = -0.7451e-8  # α1
        self.af3 = -0.5960e-7  # α2
        self.af4 = 0.1192e-6  # α3
        self.bt1 = 0.1270e6  # β0
        self.bt2 = -0.1966e6  # β1
        self.bt3 = 0.6554e5  # β2
        self.bt4 = 0.2621e6  # β3

    def __count_EA(self, point):
        xp, yp, zp = -2225669.7744, 4998936.1598, 3265908.9678
        dx = point.x - xp
        dy = point.y - yp
        dz = point.z - zp
        # 旋转至站心坐标系
        sinB = math.sin(self.Bp)
        cosB = math.cos(self.Bp)
        sinL = math.sin(self.Lp)
        cosL = math.cos(self.Lp)
        X = -dx * sinB * cosL - dy * sinB * sinL + dz * cosB
        Y = -dx * sinL + dy * cosL
        Z = dx * cosB * cosL + dy * cosB * sinL + dz * sinB
        # 方位角（弧度，0~2π）
        A = math.atan2(Y, X)
        if A < 0:
            A += 2 * math.pi
        # 高度角（弧度）
        E = math.atan2(Z, math.sqrt(X * X + Y * Y))
        return A, E

    def __count_f_l(self, A_rad, E_rad):
        E_semi = E_rad / math.pi
        psi_semi = 0.0137 / (E_semi + 0.11) - 0.022
        # 测站纬度、经度转换为半圆
        Bp_semi = self.Bp_deg / 180.0
        Lp_semi = self.Lp_deg / 180.0
        # 穿刺点半圆坐标
        phi_IP_semi = Bp_semi + psi_semi * math.cos(A_rad)
        lambda_IP_semi = Lp_semi + psi_semi * math.sin(A_rad) / math.cos(phi_IP_semi * math.pi)
        # 地磁纬度（半圆）
        phi_m_semi = phi_IP_semi + 0.064 * math.cos((lambda_IP_semi - 1.617) * math.pi)
        # 返回弧度
        return phi_m_semi * math.pi, lambda_IP_semi * math.pi

    def __count_time(self, lambda_IP, phi_m, E_rad, t_sec):
        E_semi = E_rad / math.pi
        F = 1 + 16 * (0.53 - E_semi) ** 3  # E_semi 为半圆单位
        phi_m_semi = phi_m / math.pi
        A2 = self.af1 + self.af2 * phi_m_semi + self.af3 * phi_m_semi ** 2 + self.af4 * phi_m_semi ** 3
        A4 = self.bt1 + self.bt2 * phi_m_semi + self.bt3 * phi_m_semi ** 2 + self.bt4 * phi_m_semi ** 3
        t = 43200 * (lambda_IP / math.pi) + t_sec
        k = 2 * math.pi * (t - self.A3) / A4
        if abs(k) < 1.57:
            T_ion = F * (self.A1 + A2 * math.cos(k))
        else:
            T_ion = F * self.A1
        return T_ion * 299792458

    def count_result(self):
        result = []
        t_sec = self.time.h * 3600 + self.time.m * 60 + self.time.s
        for p in self.points:
            A_rad, E_rad = self.__count_EA(p)
            if E_rad <= 0:
                D_ion = 0.0
            else:
                phi_m, lambda_IP = self.__count_f_l(A_rad, E_rad)
                D_ion = self.__count_time(lambda_IP, phi_m, E_rad, t_sec)
            # 转为度数输出
            A_deg = math.degrees(A_rad)
            E_deg = math.degrees(E_rad)
            result.append(f"{p.n} {E_deg:.3f} {A_deg:.3f} {D_ion:.4f} \n")
        return result
























