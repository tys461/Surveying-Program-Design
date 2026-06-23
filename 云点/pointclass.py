from PyQt6.QtCore import QFile


class Piont:
    def __init__(self,point_name:str='',point_X:float=0,point_Y:float=0,point_Z:float=0
                 ):
        self.point_name=point_name
        self.point_X=point_X
        self.point_Y=point_Y
        self.point_Z=point_Z


