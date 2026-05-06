import csv

class Tex_dat:
    def __init__(self,path):
        self.path=path
        with open(rf"{self.path}",'r') as tex_dat:
            self.dat=list(csv.reader(tex_dat))

