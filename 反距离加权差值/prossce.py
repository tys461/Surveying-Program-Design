import math

class Count:
    def __init__(self,Qn,Qx,Qy):
        self.Qn=Qn
        self.Qx=Qx
        self.Qy=Qy

    def Len_Q(self,idx,ix,iy,ih):
       return math.hypot(ix-self.Qx,iy-self.Qy),ih,idx

    def higt_HQ(self,lis_rank):
        up=sum(lis[1]*(1/lis[0]) for lis in lis_rank)
        on=sum((1/lis[0]) for lis in lis_rank)
        return up/on

    def count(self,lis_data):
        lis_rank=[]
        for i in lis_data:
            part=self.Len_Q(i.idx,i.x,i.y,i.z)
            lis_rank.append(part)
        lis_rank.sort(key=lambda x : x[0])
        lis_rank=lis_rank[0:5]
        lis_point=[str(i[2]) for i in lis_rank]
        lis_point_s=' '.join(lis_point)
        return f'{self.Qn} {self.Qx} {self.Qy} {self.higt_HQ(lis_rank):.3f} {lis_point_s}'
