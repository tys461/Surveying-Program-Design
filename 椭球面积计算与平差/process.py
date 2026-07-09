import math
from dataclasses import dataclass

@dataclass(slots=True)
class kelasuofu:
    a=6378245
    e_2=0.00669342162297
    e_2_1=0.0067385241468


@dataclass(slots=True)
class IUGG1975:
    a = 6378140
    e_2 =0.00669438499959
    e_2_1 =0.00673950181947

@dataclass(slots=True)
class CGCS2000:
    a =6378137
    e_2 =0.00669438002290
    e_2_1 =0.00673949677548

@dataclass(slots=True)
class AdministrativeDistrict:
    """行政区集"""
    d_c:str #行政区代码
    lis_S:list[list[float]] #高斯平面坐标点集


class Data:
    """总体数据"""
    def __init__(self,frame_number:str,lis_AD:list[AdministrativeDistrict]):
        self.f_n=frame_number  #图幅编号
        self.lis_AD=lis_AD     #行政区集

    def __auxiliary_calculations(self,ell,B):
        """辅助计算公式"""
        # print(ell.e_2)
        _e_2=ell.e_2/(1-ell.e_2)

        W=math.sqrt(1-ell.e_2*math.sin(B)**2)
        nu_2=_e_2*math.cos(B)**2
        t=math.tan(B)

        return W,nu_2,t

    def gaussian_projection_inverse(self,X:float,Y:float,ell):
        """高斯投影反算求B，L"""
        x=X
        n=int(Y/1000000)
        y=int(Y/1000000)*1000000-500000
        L0=math.radians(6*n-3)


        M0=ell.a*(1-ell.e_2)

        A=(1+3*ell.e_2/4+45*ell.e_2**2/64+175*ell.e_2**3/256
           +11025*ell.e_2**4/16384+43659*ell.e_2**5/65536)
        B=(3*ell.e_2/4+15*ell.e_2**2/16+525*ell.e_2**3/512
           +2205*ell.e_2**4/2048+72765*ell.e_2**5/65536)
        C=(15*ell.e_2**2/64+105*ell.e_2**3/256+2205*ell.e_2**4/4096
           +10395*ell.e_2**5/16384)
        D=35*ell.e_2**3/512+315*ell.e_2**4/2048+31185*ell.e_2**5/131072
        E=315*ell.e_2**4/16384+3465*ell.e_2**5/65536
        F=693*ell.e_2**5/131072

        alpha = A * M0
        beta = (-1 / 2) * (B * M0)
        gamma = (1 / 4) * (C * M0)
        delta = (-1 / 6) * (D * M0)
        epsilon = (1 / 8) * (E * M0)
        zeta = (-1 / 10) * (F * M0)

        B0=X/alpha

        B_beta=(beta*math.sin(2*B0)+gamma*math.sin(4*B0)+
                delta*math.sin(6*B0)+zeta*math.sin(8*B0)+epsilon*math.sin(10*B0))
        B_f=(X-B_beta)/alpha
        while abs(B_f-B0)>1e-8:
            B0=B_f
            B_beta = (beta * math.sin(2 * B0) + gamma * math.sin(4 * B0) +
                      delta * math.sin(6 * B0) + zeta * math.sin(8 * B0) + epsilon * math.sin(10 * B0))
            B_f = (X - B_beta) / alpha

        W, nu_2, t=self.__auxiliary_calculations(ell,B_f)
        N=ell.a/W
        M=ell.a*(1-ell.e_2)/W**3

        b0=B_f
        b1=1/(N*math.cos(B_f))
        b2=-t/(2*M*N)
        b3=-(1+2*t**2+nu_2)*b1/(6*N**2)
        # b4=-(5+3*t**2+nu_2-9*nu_2*t**2)*b2/(12*N**4)
        b4 = (t * (5 + 3 * t ** 2 + nu_2 - 9 * nu_2 * t ** 2) * (1 + nu_2)) / (24 * N ** 3 * M)
        # b5=-(5+28*t**2+24*t**4+6*nu_2+8*nu_2*t**2)*b1/(120*N**4)
        b5=(5+28*t**2+24*t**4+6*nu_2+8*nu_2*t**2)*b1/(120*N**4)

        b6=-(61+90*t**2+45*t**4)*b2/(360*N**4)

        _B=b0*y**0+b2*y**2+b4*y**4+b6*y**6
        _L=b1*y**1+b3*y**3+b5*y**5+L0

        print(math.degrees(_B),math.degrees(_L))
        return (math.degrees(_B),_L)




    def coordinate_conversion(self,lis_points:list[list[float]]):
        for p in lis_points:
            Y=p[0]
            X=p[1]
            self.gaussian_projection_inverse(X,Y,IUGG1975)




