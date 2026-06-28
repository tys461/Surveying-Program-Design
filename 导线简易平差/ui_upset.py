from PyQt6.QtCore import QFile,QTextStream,QIODevice
from process_upset import Point,Points,KeyPoints

def open(path):
    file=QFile(path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件打开失败')
        return
    # try:
    else:
        H0 = 0
        stream=QTextStream(file)
        line=1
        key_points=[]
        azimuth_p=[]
        lis_points=[]
        while not stream.atEnd():
            if line==1:
              part=stream.readLine().split(',')
              H0=float(part[1])
            if line==2:
                part = stream.readLine().split(',')
                key_points=part
            if line==3 or line==4:
                part = stream.readLine().split(',')
                azimuth_p.append([part[0],float(part[1]),float(part[2])])
            if line>=5:
                part = stream.readLine().split(',')
                if len(part)==4:
                    if part[0] in key_points:
                        key_points[key_points.index(part[0])]=KeyPoints(part[0],float(part[1]),float(part[2]),float(part[3]))
                    lis_points.append(Point(part[0],float(part[1]),float(part[2]),float(part[3])))
            line+=1
        file.close()
        return Points(lis_points,H0,key_points,azimuth_p)

    # except:
    #     print('文件格式有误')
    #     file.close()


if __name__=='__main__':
    r=open('data/data.txt')
    # print(r.calculation_inter_point())
    # print(r.calculation_cross_sectional_area())
    # print(r.key_points)
    for i in r.calculation_inter_point():
        print(i)
