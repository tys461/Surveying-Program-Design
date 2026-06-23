from ellipsoidal_parameters import*
import math


class Ell_count:
    def __init__(self,B):
        self.B=B
        self.cunt()

    def __auxiliary_calculations(self,e_2,oe_2,B) -> None :
        '''辅助计算公式'''
        self.W=math.sqrt(1-e_2*math.pow(math.sin(B), 2))
        self.nu_2=oe_2*math.pow(math.cos(B),2)
        self.t=math.tan(B)

    # def __parameters1(self) -> None:
    #     '''参数计算公式1'''
    #     self.fai=(self.a-self.b)/self.a
    #     self.e_2=(math.pow(self.a,2)-math.pow(self.b,2))/math.pow(self.a,2)
    #     self.oe_2=self.e_2/(1-self.e_2)

    def __parameters2(self) -> None:
        '''参数计算公式2'''
        self.N=self.a/self.W
        self.M=self.a*(1-self.e_2)/math.pow(self.W,3)
        self.M0=self.a*(1-self.e_2)

    def cunt(self) -> None:
        # self.__parameters1()
        self.__auxiliary_calculations(self.e_2,self.e_2_1,self.B)
        self.__parameters2()

class GpositiveArithmetic(kelasuofu,IUGG1975,CGCS2000,Ell_count) :
    def __init__(self,B_rad,L,L0,n,ell):
        # 1. 先初始化 kelasuofu（它会设置 self.a, self.e_2, self.e_2_1）
        self.check_ell(ell)
        # 2. 再初始化 Ell_count，只传入纬度 B
        Ell_count.__init__(self,B_rad)
        # 此时 self 中已有 a, e2，Ell_count 的方法可以直接使用
        self.L=L
        self.L0=L0
        self.n=n

    def check_ell(self,ell):
        if ell=='kelasuofu':
            kelasuofu.__init__(self)
        if ell=='IUGG1975':
            IUGG1975.__init__(self)
        if ell=='CGCS2000':
            CGCS2000.__init__(self)

    def __ArclengthCalculation(self):
        e2 = self.e_2
        A_coef = (1 + (3 / 4) * e2 + (45 / 64) * math.pow(e2, 2) + (175 / 256) * math.pow(e2, 3) +
                  (11025 / 16384) * math.pow(e2, 4) + (43659 / 65536) * math.pow(e2, 5))
        B_coef = ((3 / 4) * e2 + (15 / 16) * math.pow(e2, 2) + (525 / 512) * math.pow(e2, 3) +
                  (2205 / 2048) * math.pow(e2, 4) + (72765 / 65536) * math.pow(e2, 5))
        C_coef = ((15 / 64) * math.pow(e2, 2) + (105 / 256) * math.pow(e2, 3) +
                  (2205 / 4096) * math.pow(e2, 4) + (10395 / 16384) * math.pow(e2, 5))
        D_coef = ((35 / 512) * math.pow(e2, 3) + (315 / 2048) * math.pow(e2, 4) +
                  (31185 / 131072) * math.pow(e2, 5))
        E_coef = (315 / 16384) * math.pow(e2, 4) + (3465 / 65536) * math.pow(e2, 5)
        F_coef = (693 / 131072) * math.pow(e2, 5)

        self.alpha = A_coef * self.M0
        self.beta = -0.5 * (B_coef * self.M0)
        self.gamma = 0.25 * (C_coef * self.M0)
        self.delta = -1 / 6 * (D_coef * self.M0)
        self.epsilon = 1 / 8 * (E_coef * self.M0)  # 注意符号为正
        self.zeta = -0.1 * (F_coef * self.M0)

        self.X = (self.alpha * self.B +
                  self.beta * math.sin(2 * self.B) +
                  self.gamma * math.sin(4 * self.B) +
                  self.delta * math.sin(6 * self.B) +
                  self.epsilon * math.sin(8 * self.B) +
                  self.zeta * math.sin(10 * self.B))

    def __warppoor(self) -> None:
        '''经差计算'''
        self.l = math.radians(self.L - self.L0)

    def __assisted(self) -> None:
        '''计算辅助量'''
        cosB=math.cos(self.B)
        self.a0=self.X
        self.a1=self.N*cosB
        self.a2=(1/2)*self.N*(cosB**2)*self.t
        self.a3=((1/6)*self.N*(cosB**3)*(1-(self.t**2)+self.nu_2))
        self.a4=(1/24)*self.N*(cosB**4)*(5-(self.t**2)+9*self.nu_2+4*(self.t**4))*self.t
        self.a5=(1/120)*self.N*(cosB**5)*(5-18*(self.t**2)+(self.t**4)+14*self.nu_2-58*self.nu_2*(self.t**2))
        self.a6=(1/720)*self.N*(cosB**6)*(61-58*(self.t**2)+(self.t**4)+270*self.nu_2-330*self.nu_2*(self.t**2))*self.t


    def __naturalcoordinates(self) -> None:
        '''计算自然坐标'''
        self.x=self.a0*(self.l**0)+self.a2*(self.l**2)+self.a4*(self.l**4)+self.a6*(self.l**6)
        self.y=self.a1*(self.l**1)+self.a3*(self.l**3)+self.a5*(self.l**5)

    def generalcoordinates(self):
        '''计算通用坐标'''
        self.__ArclengthCalculation()
        self.__warppoor()
        self.__assisted()
        self.__naturalcoordinates()
        # 注意：北坐标是 self.x（自然北坐标），不要覆盖 self.X
        print(self.n)
        X = self.x
        Y = self.n * 1000000 + self.y + 500000
        return X, Y, self.y


class GProjectionInverse(kelasuofu,IUGG1975,CGCS2000,Ell_count):
    def __init__(self,X,Y,duda,ell):
        # 1. 先初始化 kelasuofu（它会设置 self.a, self.e_2, self.e_2_1）
        self.check_ell(ell)
        # 2. 再初始化 Ell_count，只传入纬度 B
        # 此时 self 中已有 a, e2，Ell_count 的方法可以直接使用
        self.X=X
        self.Y=Y
        self.duda=duda

    def check_ell(self,ell):
        if ell=='kelasuofu':
            kelasuofu.__init__(self)
        if ell=='IUGG1975':
            IUGG1975.__init__(self)
        if ell=='CGCS2000':
            CGCS2000.__init__(self)
    def __central_0(self):
        self.n = int(self.Y / 1000000)
        if self.duda == 3:
            self.L0_deg = 3 * self.n  # 保留度数（可选）
            self.L0 = math.radians(3 * self.n)  # 转为弧度用于计算
        if self.duda == 6:
            self.L0_deg = 6 * self.n - 3
            self.L0 = math.radians(6 * self.n - 3)

    def __naturalpoint(self):
        self.inverse_x = self.X
        self.inverse_y = self.Y - self.n * 1000000 - 500000

    def __basepoint(self):
        e2 = self.e_2
        self.M0=self.a*(1-self.e_2)
        e2 = self.e_2
        self.A = (1 + (3 / 4) * e2 + (45 / 64) * math.pow(e2, 2) + (175 / 256) * math.pow(e2, 3) +
                  (11025 / 16384) * math.pow(e2, 4) + (43659 / 65536) * math.pow(e2, 5))
        self.B = ((3 / 4) * e2 + (15 / 16) * math.pow(e2, 2) + (525 / 512) * math.pow(e2, 3) +
                  (2205 / 2048) * math.pow(e2, 4) + (72765 / 65536) * math.pow(e2, 5))
        self.C = ((15 / 64) * math.pow(e2, 2) + (105 / 256) * math.pow(e2, 3) +
                  (2205 / 4096) * math.pow(e2, 4) + (10395 / 16384) * math.pow(e2, 5))
        self.D = ((35 / 512) * math.pow(e2, 3) + (315 / 2048) * math.pow(e2, 4) +
                  (31185 / 131072) * math.pow(e2, 5))
        self.E = (315 / 16384) * math.pow(e2, 4) + (3465 / 65536) * math.pow(e2, 5)
        self.F = (693 / 131072) * math.pow(e2, 5)
        self.alpha = self.A * self.M0
        self.beta = (-1 / 2) * (self.B * self.M0)
        self.gamma = (1 / 4) * (self.C * self.M0)
        self.delta = (-1 / 6) * (self.D * self.M0)
        self.epsilon = (1 / 8) * (self.E * self.M0)
        self.zeta = (-1 / 10) * (self.F * self.M0)


        X = self.X
        B0=self.X/self.alpha

        self.bata=self.beta*math.sin(2*B0)+self.gamma*math.sin(4*B0)+self.delta*math.sin(6*B0)+self.epsilon*math.sin(8*B0)+self.zeta*math.sin(10*B0)
        self.Bf=(X-self.bata)/self.alpha
        # print(self.Bf - B0)
        while abs(self.Bf - B0) > 1e-10:
           B0=self.Bf
           self.bata = self.beta * math.sin(2 * B0) + self.gamma * math.sin(4 * B0) + self.delta * math.sin(
               6 * B0) + self.epsilon * math.sin(8 * B0) + self.zeta * math.sin(10 * B0)
           self.Bf = (X - self.bata) / self.alpha
        # print(self.Bf)


    def dushu(self,input_d):
        B_j=math.degrees(input_d)
        zhen_b=int(B_j)
        fen=(B_j-zhen_b)*60
        miao=(fen-int(fen))*60
        otput=zhen_b+fen+miao
        print(otput)

        return otput





    def __assisted_inverse(self):
            Ell_count.__init__(self,self.Bf)
            Bf=self.Bf
            Nf=self.N
            Nuf_2=self.nu_2
            Mf=self.M
            tf=self.t


            self.b0=self.Bf
            self.b1=1/(Nf*math.cos(Bf))
            self.b2=-tf/(2*Mf*Nf)
            self.b3=-(1+2*(tf**2)+Nuf_2)*self.b1/(6*(Nf**2))
            self.b4=-(5+3*(tf**2)+Nuf_2-9*Nuf_2*(tf**2))*self.b2/(12*(Nf**2))
            self.b5=-(5+28*(tf**2)+24*(tf**4)+6*(Nuf_2)+8*Nuf_2*(tf**2))*self.b1/(120*(Nf**4))
            self.b6=(61+90*(tf**2)+45*(tf**4))*self.b2/(360*(Nf**4))

    def conutBL(self):
        self.__central_0()
        self.__naturalpoint()
        self.__basepoint()
        self.__assisted_inverse()
        y = self.inverse_y
        self.conutBL_B = self.b0 + self.b2 * y ** 2 + self.b4 * y ** 4 + self.b6 * y ** 6
        self.conutBL_L = self.b1 * y + self.b3 * y ** 3 + self.b5 * y ** 5 + self.L0  # self.L0 是弧度
        # 返回：B弧度, L弧度, L0_度数, n
        return self.conutBL_B, self.conutBL_L, self.L0_deg, self.n



class Center:
    def __init__(self,L,duda):
        self.duda=duda
        self.L=L

    def L0_n(self):
        L_deg = math.degrees(self.L) if abs(self.L) < 10 else self.L   # 粗略判断
        if self.duda == 6:
            n = int((L_deg - 1.5) / 3 + 1)
            L0 = 3 * n
        else:
            n = int(L_deg / 6) + 1
            L0 = 6 * n - 3
        return n, L0


def tranform(X,Y,duda,Ell):
    inv=GProjectionInverse(float(X), float(Y),duda,Ell)
    B_rad, L_rad, L0_3, n_3 = inv.conutBL()
    L_deg = math.degrees(L_rad)
    # n_6 = int(L_deg / 6) + 1
    # L0_6 = 6 * n_6 - 3
    cen=Center(L_rad,duda)
    n,L0=cen.L0_n()
    print(n,L0)
    pos = GpositiveArithmetic(B_rad, L_deg, L0, n,Ell)
    X_6, Y_6, y_6 = pos.generalcoordinates()
    print(f"原始3度带坐标: X={X:.3f}, Y={Y:.3f}")
    print(f"大地坐标: B={math.degrees(B_rad):.8f}°, L={L_deg:.8f}°")
    print(f"转换后6度带坐标: X={X_6:.3f}, Y={Y_6:.3f}")
    return [X_6,y_6,Y_6]




def lindaihuansuan(X, Y, duda,ell):
    inv = GProjectionInverse(X, Y, duda,ell)
    B_rad, L_rad, L0_deg, n = inv.conutBL()
    L_deg = math.degrees(L_rad)

    # 左邻带
    n_left = n - 1
    if duda == 3:
        L0_left = 3 * n_left
    else:
        L0_left = 6 * n_left - 3
    # 右邻带
    n_right = n + 1
    if duda == 3:
        L0_right = 3 * n_right
    else:
        L0_right = 6 * n_right - 3

    # 正算到左右邻带
    pos_left = GpositiveArithmetic(B_rad, L_deg, L0_left, n_left,ell)
    pos_right = GpositiveArithmetic(B_rad, L_deg, L0_right, n_right,ell)
    X_left, Y_left, _ = pos_left.generalcoordinates()
    X_right, Y_right, _ = pos_right.generalcoordinates()
    return  [X_left, Y_left],[X_right, Y_right]
