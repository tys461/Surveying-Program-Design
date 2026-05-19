class SightInfo:
    """单次观测信息类"""
    def __init__(self, line_id: int = 0, pt_name: str = "", rd: float = 0.0, hd: float = 0.0,
                 adr: int = 0, time_str: str = "", s_type: str = "") -> None:
        self.LineID = line_id      # 所在原始数据行号
        self.ptName = pt_name
        self.RD = rd #读数
        self.HD = hd #视距
        self.Adr = adr
        self.TimeStr = time_str
        self.SType = s_type        # 测量类型：后视B，前视F


class StationInfo:
    """测站信息类"""
    def __init__(self) -> None:
        self.FPtName = ""          # 前视点名
        self.FPtH = 0.0            # 前视点高程
        self.BPtName = ""          # 后视点名
        self.BPtH = 0.0            # 后视点高程
        self.SightList: list[SightInfo] = []   # 测量信息
        self.Rb1 = self.Rb2 = self.Rf1 = self.Rf2 = 0.0  # 后/前视中丝读数
        self.Db1 = self.Db2 = self.Df1 = self.Df2 = 0.0  # 后/前视距
        self.DeltH = 0.0           # 测站高差
        self.DeltD = 0.0           # 测站视距差

    def Reset(self) -> None:
        """重新设置测站信息（后视点高程BPtH需在调用前赋值）"""
        r_num = f_num = 0

        for sight in self.SightList:
            if sight.SType == "B":          # 后视
                r_num += 1
                if r_num == 1:              # 第1次
                    self.Rb1 = sight.RD
                    self.Db1 = sight.HD
                else:                       # 第2次
                    self.Rb2 = sight.RD
                    self.Db2 = sight.HD
                self.BPtName = sight.ptName
            else:                           # 前视
                f_num += 1
                if f_num == 1:
                    self.Rf1 = sight.RD
                    self.Df1 = sight.HD
                else:
                    self.Rf2 = sight.RD
                    self.Df2 = sight.HD
                self.FPtName = sight.ptName

        # 测站高差和视距差（观测次数成对，SightList长度应为偶数）
        self.DeltH = (self.Rb1 - self.Rf1 + self.Rb2 - self.Rf2) / (len(self.SightList) / 2)
        self.DeltD = (self.Db1 - self.Df1 + self.Db2 - self.Df2) / (len(self.SightList) / 2)

        # 计算前视点高程
        self.FPtH = self.DeltH + self.BPtH


class PartInfo:
    """测段信息类"""
    def __init__(self) -> None:
        self.partName = ""                   # 测段名
        self.partNum = 0                     # 测段号
        self.PartCode = ""                   # 测段代码
        self.StartPtName = ""                # 开始点名
        self.EndPtName = ""                  # 结束点名
        self.StationList: list[StationInfo] = []   # 测站信息
        self.StationCount = 0                # 测站数
        self.StartPtH = 0.0                  # 开始点高程
        self.EndPtH = 0.0                    # 结束点高程
        self.sh = 0.0                        # 累计高差
        self.dz = 0.0                        # 线路闭合差
        self.Db = 0.0                        # 累计后视距
        self.Df = 0.0                        # 累计前视距

    def Reset(self) -> None:
        """重新设置测段信息（第一个测站的后视点高程需事先赋值为StartPtH）"""
        self.partName = f"{self.StartPtName}-{self.EndPtName}"
        self.StationCount = len(self.StationList)
        self.sh = self.Db = self.Df = 0.0

        for i, station in enumerate(self.StationList):
            if i > 0:
                station.BPtH = self.StationList[i - 1].FPtH
            station.Reset()
            self.sh += station.DeltH
            # 累计后/前视距：每个测站的后/前视距取平均值（观测次数为2次时，分母=2）
            self.Db += (station.Db1 + station.Db2) / (len(station.SightList) / 2)
            self.Df += (station.Df1 + station.Df2) / (len(station.SightList) / 2)

        self.dz = self.EndPtH - (self.StartPtH + self.sh)


class LineInfo:
    """线路信息类，对应一个观测文件中的所有测段信息"""
    def __init__(self) -> None:
        self.LineName = ""                  # 线路名
        self.PartList: list[PartInfo] = []  # 测段信息

    def GetLength(self) -> float:
        """获得线路长度（后视距+前视距之和）"""
        length = 0.0
        for part in self.PartList:
            length += part.Db + part.Df
        return length

