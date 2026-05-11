import math
import ui

def rotataion_elements(phi_edg,omega_deg,kappa_deg):
    """计算旋转矩阵元素"""
    phi=math.radians(phi_edg)
    omega=math.radians(omega_deg)
    kappa=math.radians(kappa_deg)
    # cos_p=math.cos(phi_edg);sin_p=math.sin(phi_edg)
    # cos_o=math.cos(omega_deg);sin_o=math.sin(omega_deg)
    # cos_k=math.cos(kappa_deg);sin_k=math.sin(kappa_deg)
    #

    cos_p=math.cos(phi);sin_p=math.sin(phi)
    cos_o=math.cos(omega);sin_o=math.sin(omega)
    cos_k=math.cos(kappa);sin_k=math.sin(kappa)
    #
    # a1=cos_p*cos_k-cos_p*sin_o*sin_k
    # a2=-cos_p*sin_k-sin_p*sin_o*sin_k
    # a3=-sin_p*cos_p
    #
    # b1=cos_o*sin_k
    # b2=cos_o*cos_k
    # b3=-sin_o
    #
    # c1=sin_p*cos_k+cos_p*sin_o*sin_k
    # c2=-sin_o*cos_k+cos_p*sin_o*sin_k
    # c3=cos_p*cos_o

    a1=cos_p*cos_k-sin_p*sin_o*sin_k
    # a2=-cos_p*sin_k-sin_p*sin_o*sin_k
    a2 = -cos_p * sin_k - sin_p * sin_o * cos_k
    a3=-sin_p*cos_o

    b1=cos_o*sin_k
    b2=cos_o*cos_k
    b3=-sin_o

    c1=sin_p*cos_k+cos_p*sin_o*sin_k
    # c2=-sin_o*sin_k+cos_p*sin_o*cos_k
    c2 = -sin_p * sin_k + cos_p * sin_o * cos_k
    c3=cos_p*cos_o


    return a1,a2,a3,b1,b2,b3,c1,c2,c3

def spatial_auxiliary(x,y,f,phi_edg,omega_deg,kappa_deg):
    """计算空间辅助坐标"""
    a1, a2, a3, b1, b2, b3, c1, c2, c3=rotataion_elements(phi_edg,omega_deg,kappa_deg)

    X=x
    Y=y
    Z=f

    u=a1*X+a2*Y+a3*Z
    v=b1*X+b2*Y+b3*Z
    w=c1*X+c2*Y+c3*Z

    return u,v,w

def projection_coefficient(Xs1,Ys1,Zs1,phi_edg1,omega_deg1,kappa_deg1,x1,y1,z1,Xs2,Ys2,Zs2,
                           phi_edg2,omega_deg2,kappa_deg2,x2,y2,z2):
    u1,v1,w1=spatial_auxiliary(x1,y1,z1,phi_edg1,omega_deg1,kappa_deg1)
    u2,v2,w2=spatial_auxiliary(x2,y2,z2,phi_edg2,omega_deg2,kappa_deg2)

    B_u = Xs2 - Xs1
    B_v=Ys2-Ys1
    B_w=Zs2-Zs1

    N1=(B_u*w2-B_w*u2)/(u1*w2-u2*w1)
    N2=(B_u*w1-B_w*u1)/(u1*w2-u2*w1)


    X=Xs1+N1*u1
    Y=0.5*((Ys1+N1*v1)+(Ys2+N2*v2))
    Z = Zs1 + N1 * w1
    print(f'外方位元素Xs1:{Xs1} 角元素o1:{phi_edg1} 像点坐标x1:{x1}')
    print(f'外方位元素Ys1:{Ys1} 角元素p1:{omega_deg1} 像点坐标y1:{y1}')
    print(f'外方位元素Zs1:{Zs1} 角元素q1:{kappa_deg1} 像点坐标z1:{z1}')
    print('----------------------------------------------')
    print(f'外方位元素Xs1:{Xs2} 角元素o1:{phi_edg2} 像点坐标x1:{x2}')
    print(f'外方位元素Ys1:{Ys2} 角元素p1:{omega_deg2} 像点坐标y1:{y2}')
    print(f'外方位元素Zs1:{Zs2} 角元素q1:{kappa_deg2} 像点坐标z1:{z2}')

    print('\n')
    print(f'象限辅助坐标u1:{u1} 象限辅助坐标v1:{v1} 象限辅助坐标u1:{w1}')
    print(f'象限辅助坐标u1:{u2} 象限辅助坐标v1:{v2} 象限辅助坐标u1:{w2}')
    print('----------------------------------------------')
    print(f'投影系数N1{N1} 投影系数N1：{N2}')
    print('----------------------------------------------')
    print(X,Y,Z)

a=ui.Open()
list_data=a.open_data_()
projection_coefficient(*list_data[0],*list_data[1])

