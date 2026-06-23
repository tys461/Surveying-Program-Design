from PyQt6.QtCore import QFile,QTextStream,QIODevice
from prossce import Point,LisPoints,Grids

def open(path):
    file=QFile(path)
    lisPoints=LisPoints()
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件打开失败')
        return
    else:
        stream=QTextStream(file)
        idx=1
        while not stream.atEnd():
            part=stream.readLine().split()
            if len(part)==3:
                a=Point(idx,float(part[0]),float(part[1]),float(part[2]))
                lisPoints.lis_points.append(a)
                idx+=1
    return lisPoints



if __name__=='__main__':
    lisPoints=open('point.txt')
    grids=Grids(lisPoints)
    print(grids.count_all())



