import math
from dataclasses import dataclass

@dataclass(slots=True)
class CGCS2000:
    a0 = 6378140
    b0 = 6356755.29
    e_2_1 = 0.00673949677548
    e_2 = 0.00669438002290


@dataclass(slots=True)
class kelasuofu:
    a = 6378245
    e_2 = 0.00669342162297
    e_2_1 = 0.0067385241468

@dataclass(slots=True)
class IUGG1975:
    a = 6378140
    e_2 = 0.00669438499959
    e_2_1 = 0.00673950181947



@dataclass(slots=True)
class AdministrativeDistrict:
    """行政区集"""
    d_c: str          # 行政区代码
    lis_S: list[list[float]]  # 高斯平面坐标点集
@dataclass(slots=True)
class Table:
        scale_={'B':1/500000,'C':1/250000,'D':100000,'E':1/50000,'F':1/25000,
                'G':1/10000,'H':1/5000,'I':1/2000,'J':1/1000,'K':1/500}
        Bbl_={1/1000000:[6,4],1/500000:[3,2],1/250000:[1+30/60,1],1/100000:[30/60,20/60],
              1/50000:[15/60,10/60],1/25000:[7/60+30/3600,5/60],1/10000:[3/60+45/3600,1/60+15/3600],
              1/5000:[1/60+52.5/3600,1/60+15/3600],1/2000:[37.5/3600,25/3600],
              1/1000:[18.75/3600,12.5/3600],1/500:[9.375/3600,6.25/3600]}

class Data:
    """总体数据"""
    def __init__(self, frame_number: str, lis_AD: list[AdministrativeDistrict]):
        self.f_n = frame_number
        self.lis_AD = lis_AD

    def __auxiliary_calculations_1(self, ell, B):
        """辅助计算 W, nu_2, t （已修正 W 缺平方错误）"""
        _e_2 = ell.e_2 / (1 - ell.e_2)
        W = math.sqrt(1 - ell.e_2 * math.sin(B) ** 2)   # 修正：sin(B) 要平方
        nu_2 = _e_2 * math.cos(B) ** 2
        t = math.tan(B)
        return W, nu_2, t

    def __auxiliary_calculations_2(self,ell):
        """辅助计算 e2, A, Bcoef Ccoef..... （已修正 W 缺平方错误）"""
        e2 = ell.e_2
        A = (1 + 3*e2/4 + 45*e2**2/64 + 175*e2**3/256
             + 11025*e2**4/16384 + 43659*e2**5/65536)
        Bcoef = (3*e2/4 + 15*e2**2/16 + 525*e2**3/512
                 + 2205*e2**4/2048 + 72765*e2**5/65536)
        Ccoef = (15*e2**2/64 + 105*e2**3/256 + 2205*e2**4/4096
                 + 10395*e2**5/16384)
        Dcoef = (35*e2**3/512 + 315*e2**4/2048 + 31185*e2**5/131072)
        Ecoef = (315*e2**4/16384 + 3465*e2**5/65536)
        Fcoef = (693*e2**5/131072)

        return e2,A,Bcoef,Ccoef,Dcoef,Ecoef,Fcoef


    def gaussian_projection_inverse(self, X: float, Y: float, ell):
        """
        高斯投影反算（参照 C# BPoint.XYtoBL 算法）
        输入：X, Y（含带号的高斯平面坐标），椭球参数 ell
        返回：(B, L)  单位：弧度
        """
        # ----- 1. 去带号并计算中央经线 -----
        if Y < 1000000:
            raise ValueError("输入坐标无带号，请检查 Y 值！")

        p = int(Y // 1000000)               # 带号
        y = Y - p * 1000000 - 500000        # 去带号并移轴（中央子午线以西为负）

        # 判断带号属于 6°带还是 3°带（参考 C# 逻辑）
        if 13 <= p <= 23:                   # 6°带
            L0_deg = 6 * p - 3
        elif 24 <= p <= 45:                # 3°带
            L0_deg = 3 * p
        else:
            # 若不在常规范围，默认按 6°带处理（或抛出异常）
            L0_deg = 6 * p - 3
        L0 = math.radians(L0_deg)

        # ----- 2. 求底点纬度 B_f（采用迭代法，通用且精度高）-----
        # 子午线弧长系数（与椭球 e_2 相关）
        e2, A, Bcoef, Ccoef, Dcoef, Ecoef, Fcoef=self.__auxiliary_calculations_2(ell)


        M0 = ell.a * (1 - e2)
        alpha = A * M0
        beta = -0.5 * Bcoef * M0
        gamma = 0.25 * Ccoef * M0
        delta = -1/6 * Dcoef * M0
        epsilon = 1/8 * Ecoef * M0
        zeta = -1/10 * Fcoef * M0

        B0 = X / alpha
        while True:
            B_beta = (beta * math.sin(2*B0) + gamma * math.sin(4*B0) +
                      delta * math.sin(6*B0) + zeta * math.sin(8*B0) +
                      epsilon * math.sin(10*B0))
            B_f = (X - B_beta) / alpha
            if abs(B_f - B0) < 1e-12:
                break
            B0 = B_f

        # ----- 3. 计算辅助量 -----
        W, nu_2, t = self.__auxiliary_calculations_1(ell, B_f)
        N = ell.a / W                     # 卯酉圈曲率半径
        M = ell.a * (1 - e2) / W**3       # 子午圈曲率半径

        # ----- 4. 计算纬度 B 和经度 L 的改正系数（参照 C# 公式，修正符号与系数）-----
        # 注意：C# 中采用 (y2/n) 的形式，我们统一用 (y/N)，即单位化坐标
        yN = y / N

        # 纬度改正（B = B_f + 二阶项 + 四阶项 + 六阶项）
        # 二阶项：-0.5*(1+nu_2)*t*yN^2
        b2 = -0.5 * (1 + nu_2) * t * yN**2
        # 四阶项：+ (1/24)*(5+3*t^2+nu_2-9*nu_2*t^2)*(1+nu_2)*t*yN^4
        # 但标准公式中无 (1+nu_2) 因子，C# 中有，为保持一致，此处采用 C# 形式
        # 注意：C# 中分母为 24，且没有除以 N 的额外因子，因为我们直接使用 yN
        b4 = (1/24) * (5 + 3*t**2 + nu_2 - 9*nu_2*t**2) * (1 + nu_2) * t * yN**4
        # 六阶项：- (1/720)*(61+90*t^2+45*t^4)*(1+nu_2)*t*yN^6
        b6 = -(1/720) * (61 + 90*t**2 + 45*t**4) * (1 + nu_2) * t * yN**6

        B = B_f + b2 + b4 + b6

        # 经度改正（L = L0 + 一阶项 + 三阶项 + 五阶项）
        # 一阶项：+ (1/cosBf)*yN
        l1 = (1 / math.cos(B_f)) * yN
        # 三阶项：- (1/6)*(1+2*t^2+nu_2)*(1/cosBf)*yN^3
        l3 = -(1/6) * (1 + 2*t**2 + nu_2) * (1 / math.cos(B_f)) * yN**3
        # 五阶项：+ (1/120)*(5+28*t^2+24*t^4+6*nu_2+8*nu_2*t^2)*(1/cosBf)*yN^5
        l5 = (1/120) * (5 + 28*t**2 + 24*t**4 + 6*nu_2 + 8*nu_2*t**2) * (1 / math.cos(B_f)) * yN**5

        L = L0 + l1 + l3 + l5

        return (B, L)

    def coordinate_conversion(self, lis_points: list[list[float]]):
        """批量转换，使用 IUGG1975 椭球（与 C# 西安80相近）"""
        for p in lis_points:
            Y = p[0]
            X = p[1]
            B, L = self.gaussian_projection_inverse(X, Y, IUGG1975)  # 建议使用 IUGG1975
            print(f"B={math.degrees(B):.9f}°, L={math.degrees(L):.9f}°")





    """
    4--------3
    |        |
    |        |
    1--------2
    """
    # def map_sheet_numbering_calculation(self,scale,beta_L,beta_B,ell):
    #     """分幅计算和图幅理论面积计算"""
    #     table=Table()
    #     row=float(self.f_n[4:7])
    #     col=float(self.f_n[7:10])
    #
    #     B100=(row-1)*4
    #     L100=(col-31)*6
    #
    #     n=table.Bbl_[scale][1]/beta_B
    #
    #     B1=B100+beta_B*(n-row)
    #     L1=L100+beta_L*(col-1)
    #
    #     B2=B1
    #     L2=L1+beta_L
    #
    #     B3=B1+beta_B
    #     L3=L1+beta_L
    #
    #     B4=B1+beta_B
    #     L4=L1
    #
    #     rad_B=math.radians(beta_B)
    #     rad_Bm=math.radians((B1+B2)/2)
    #     rad_L=math.radians(beta_L)
    #     L_f=1+52.5/60
    #
    #     e2, A, B, C, D, E, F=self.__auxiliary_calculations_2(ell)
    #     P=(4*math.pi*ell.b0**2*L_f)/(360*60)*(A*math.sin(rad_B/2)*math.cos(rad_Bm)-
    #                                            B*math.sin(3*rad_B/2)*math.cos(3*rad_Bm)*
    #                                            C*math.sin(5*rad_B/2)*math.cos(5*rad_Bm)-
    #                                            D*math.sin(7*rad_B/2)*math.cos(7*rad_Bm)*
    #                                            E*math.sin(9*rad_B/2)*math.cos(9*rad_Bm))
    #
    #     return P
    def map_sheet_numbering_calculation(self, frame_number: str,table):
        """
        根据图幅编号计算图幅理论面积（平方米）
        完全等效于 C# 的 SheetTheoryArea + CalculateSheetPoints
        输入：frame_number，例如 "B48H109193"
        输出：理论面积（平方米）
        """
        # ---- 1. 解析图幅编号 ----
        alpha = 'ABCDEFGHIJKLMNOPQRSTUV'
        row_char = frame_number[0]  # 行字母
        col_str = frame_number[1:3]  # 列号，两位
        scale_code = frame_number[3]  # 比例尺代码

        # 行号（1~22）
        a = alpha.index(row_char) + 1
        # 列号（31~60等）
        b = int(col_str)

        # 获取比例尺对应的经纬差（度）
        scale = table.scale_[scale_code]  # 假设 self.table 是 Table 实例
        lon_diff, lat_diff = table.Bbl_[scale]  # 经差，纬差（度）

        # 1:100万图幅左下角经纬度（度）
        lat_base = (a - 1) * 4
        lon_base = (b - 31) * 6

        # 默认西南角、东北角（1:100万整幅）
        lat_sw = lat_base
        lon_sw = lon_base
        lat_ne = lat_base + 4
        lon_ne = lon_base + 6

        # 如果图幅编号长度 > 3，说明是子图幅（如 1:50万等）
        if len(frame_number) > 3:
            # 后三位行号（从上往下数），后三位列号（从左往右数）
            c = int(frame_number[4:7])  # 行号
            d = int(frame_number[7:10])  # 列号
            # 计算该子图幅的西南角
            lat_sw = lat_base + (4 / lat_diff - c) * lat_diff
            lon_sw = lon_base + (d - 1) * lon_diff
            lat_ne = lat_sw + lat_diff
            lon_ne = lon_sw + lon_diff

        # 转为弧度
        b1 = math.radians(lat_sw)
        l1 = math.radians(lon_sw)
        b2 = math.radians(lat_ne)
        l2 = math.radians(lon_ne)

        # ---- 2. 计算面积 ----
        # 经差（单位：分）
        dl = abs(l2 - l1) * 180 * 60 / math.pi
        # 平均纬度（弧度）
        bm = (b1 + b2) / 2.0
        # 半纬差（弧度）
        db = abs(b2 - b1) / 2.0

        # 椭球参数（与 C# 一致，使用西安80椭球）
        a0 = 6378140
        b0 = 6356755.29
        e2 = (a0 * a0 - b0 * b0) / (a0 * a0)

        # 系数（注意与变量名区分）
        coefA = (1 + (3.0 / 6.0) * e2 + (30.0 / 80.0) * e2 ** 2 + (35.0 / 112.0) * e2 ** 3
                 + (630.0 / 2304.0) * e2 ** 4)
        coefB = ((1.0 / 6.0) * e2 + (15.0 / 80.0) * e2 ** 2 + (21.0 / 112.0) * e2 ** 3
                 + (420.0 / 2304.0) * e2 ** 4)
        coefC = ((3.0 / 80.0) * e2 ** 2 + (7.0 / 112.0) * e2 ** 3
                 + (180.0 / 2304.0) * e2 ** 4)
        coefD = ((1.0 / 112.0) * e2 ** 3 + (45.0 / 2304.0) * e2 ** 4)
        coefE = ((5.0 / 2304.0) * e2 ** 4)

        # 面积公式（与 C# 完全一致）
        s = (4 * math.pi / (360 * 60)) * b0 * b0 * dl * (
                coefA * math.sin(db) * math.cos(bm)
                - coefB * math.sin(3 * db) * math.cos(3 * bm)
                + coefC * math.sin(5 * db) * math.cos(5 * bm)
                - coefD * math.sin(7 * db) * math.cos(7 * bm)
                + coefE * math.sin(9 * db) * math.cos(9 * bm)
        )

        return s















