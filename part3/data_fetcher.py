import os

class readOpen():
    def __init__(self,path):
        self.path=path
        self.data=[]
    def open(self):
        if not os.path.exists(self.path):
            print("文件不存在 ")
            return None
        with open(self.path,'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                parts=line.split(',')
                name=int(parts[0])
                x=float(parts[1])
                y=float(parts[2])
                self.data.append([name,x,y])

