from PyQt6.QtCore import QFile,QTextStream,QIODevice
from process import Point,Points

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
                        for idx in range(len(key_points)):
                            if part[0]==key_points[idx]:
                                key_points[idx]=Point(part[0],float(part[1]),float(part[2]),float(part[3]))
                    lis_points.append(Point(part[0],float(part[1]),float(part[2]),float(part[3])))
            line+=1
        file.close()
        return Points(lis_points,H0,key_points,azimuth_p)

    # except:
    #     print('文件格式有误')
    #     file.close()


if __name__=='__main__':
    r=open('data/data.txt')
    inter_m=r.calculate_plane_coordinates_elevations_cross_section_interpolation()
    for i in inter_m:
        print(i)
