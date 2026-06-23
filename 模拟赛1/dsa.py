class Matrix:
    def __init__(self,lis:list[list]):
        self._data=[row[:] for row in lis]
        self.row=len(lis)
        self.cols=len(lis[0]) if lis else 0

