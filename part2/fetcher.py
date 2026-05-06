import os

class Opne_data():
    def __init__(self,path):
        self.path=path

    def open(self):
        data=[]
        if not os.path.exists(self.path):
            print(f"错误：文件 {self.path} 不存在")
            return f"错误：文件 {self.path} 不存在"
        with open(self.path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                data.append(parts)
        return data

