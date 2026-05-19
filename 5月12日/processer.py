from data import SightInfo,StationInfo,PartInfo,LineInfo
from open import Open_dat

class ReadData(Open_dat,SightInfo,StationInfo,PartInfo,LineInfo):
    def __init__(self):
        super().__init__()
        for i in self.list_data:
            if self.list_data[i][2][1] == 'Start-Line':
                LineInfo()




