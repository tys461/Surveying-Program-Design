from dataclasses import dataclass
import math

@dataclass(slots=True)
class Point:
    """定义点类"""
    n : str
    x : float
    y : float
    z : float

class Points:
    """定义点集"""
    def __init__(self,lis_points:list[Point]):
        self.lis_points=lis_points
        self.Q1=(4310,3600)

    def weighted_interpolation(self):
        lis_distance=[]
        for  p in self.lis_points:
            dis=math.hypot(self.Q1[0]-p.x,self.Q1[1]-p.y)
            lis_distance.append((dis,p.z))

        lis_distance.sort()
        lis_distance=lis_distance[0:5]

        up=0
        down=0
        for i in lis_distance:
            up+=i[1]*1/i[0]
            down+=1/i[0]

        return up/down



