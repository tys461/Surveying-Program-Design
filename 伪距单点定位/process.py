import math
from dataclasses import dataclass

@dataclass(slots=True)
class Gps:
    n:str
    X_s:float #Satposition(X)
    Y_s:float #Satposition(Y)
    Z_s:float #Satposition(Z)
    S_C:float #Sat Clock(m)
    E:float   #Elevation(°)
    CL:float  #CL(m)
    T_D:float #Trop Delay(m)

@dataclass(slots=True)
class Satellite:
    satellite_number:int
    Gps_time:float
    lis_Gps:list[Gps]

class Observation:
    def __init__(self,X_0,Y_0,Z_0,lis_satellite:list):
        self.X_0=X_0
        self.Y_0=Y_0
        self.Z_0=Z_0
        self.lis_satellite=lis_satellite





