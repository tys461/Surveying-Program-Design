from ellipsoidal_parameters import*
import math


class Ell_count:
    def __init__(self,B,L,L0):
        self.B=B
        self.L=L
        self.L0=L0
        self.cunt()

    def __auxiliary_calculations(self,e_2,oe_2,B) -> None :
        '''辅助计算公式'''
        self.W=math.sqrt(1-e_2*math.pow(math.sin(B), 2))
        self.nu_2=oe_2*math.pow(math.cos(B),2)
        self.t=math.tan(B)

    def __parameters1(self) -> None:
        '''参数计算公式1'''
        self.fai=(self.a-self.b)/self.a
        self.e_2=(math.pow(self.a,2)-math.pow(self.b,2))/math.pow(self.a,2)
        self.oe_2=self.e_2/(1-self.e_2)

    def __parameters2(self) -> None:
        '''参数计算公式1'''
        self.N=self.a/self.W
        self.M=self.a*(1-self.e_2)/math.pow(self.W,3)
        self.M0=self.a*(1-self.e_2)

    def cunt(self) -> None:
        self.__parameters1()
        self.__auxiliary_calculations(self.e_2,self.oe_2,self.B)
        self.__parameters2()

class GpositiveArithmetic(kelasuofu,Ell_count) :
    def __init__(self, B_rad):
        # 1. 先初始化 kelasuofu（它会设置 self.a, self.e_2, self.e_2_1）
        kelasuofu.__init__(self)
        # 2. 再初始化 Ell_count，只传入纬度 B
        Ell_count.__init__(self, B_rad)
        # 此时 self 中已有 a, e2，Ell_count 的方法可以直接使用


    def __ArclengthCalculation(self) -> None:
        '''子午弧长计算公式'''
        e2=self.e_2
        self.A=(1+(3/4)*self.e_2+(45/64)*math.pow(e2,4)+(175/256)*math.pow(e2,6)+
                (11025/16384)*math.pow(e2,8)+(43659/65536)*math.pow(e2,10))
        self.B=((3/4)*self.e_2+(15/16)*math.pow(e2,4)+(525/512)*math.pow(e2,6)+
                (2205/2048)*math.pow(e2,8)+(72765/65536)*math.pow(e2,10))
        self.C=((15/64)*math.pow(e2,4)+(105/256)*math.pow(e2,6)+
                (2205/4096)*math.pow(e2,8)+(10395/16384)*math.pow(e2,10))
        self.D=((35/512)*math.pow(e2,6)+(315/2048)*math.pow(e2,8)+
                (31185/131072)*math.pow(e2,10))
        self.E=(315/16384)*math.pow(e2,8)+(3465/65536)*math.pow(e2,10)
        self.F=(693/131072)*math.pow(e2,10)

        self.alpha=self.A*self.M0
        self.beta=(-1/2)*(self.B*self.M0)
        self.gamma=(1/4)*(self.C*self.M0)
        self.delta=(-1/6)*(self.D*self.M0)
        self.epsilon=(-1/8)*(self.E*self.M0)
        self.zeta=(-1/10)*(self.F*self.M0)


        self.X=(self.alpha*self.B+
                self.beta*math.sin(2*self.B)+
                self.gamma*math.sin(4*self.B)+
                self.delta*math.sin(6*self.B)+
                self.epsilon*math.sin(8*self.B)+
                self.zeta*math.sin(10*self.B))

    def __warppoor(self) -> None:
        self.l=self.L-self.L0

    def __assisted(self):
        cosB=math.cos(self.B)
        self.a0=self.X
        self.a1=self.N*cosB
        self.a2=(1/2)*self.N*(cosB**2)*self.t
        self.a3=((1/24)*self.N*(cosB**3)*(1-(self.t**2)+self.nu_2))
        self.a4=(1/24)*self.N*(cosB**4)*(5-(self.t**2)+9*self.nu_2+4*(self.t**4))*self.t
        self.a5=(1/120)*self.N*(cosB**5)*(5-18*(self.t**2)+(self.t**4)+14*(self.nu_2**2)-58*(self.nu_2**2)*(self.t**2))
        self.a6=(1/720)*self.N*(cosB**6)*(61-58*(self.t**2)+(self.t**4)+270*(self.nu_2**2)-330*(self.nu_2**2)*(self.t**2))*self.t




