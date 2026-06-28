from PyQt6.QtCore import QFile,QTextStream,QIODevice
from process_upset import Point,KeyPoint,Points

def open(path):
    file=QFile(path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print("文件打开失败")
        return
    row=1
    H0=0
    lis_AB=[]
    lis_points=[]

    lis_key_points_stack:[str]=[]#构建一个关键点的栈

    lis_key_points:[KeyPoint]=[]

    stream=QTextStream(file)
    while not stream.atEnd():
        part=stream.readLine().split(',')
        if row==1:
            H0=float(part[1])

        if row==2:
            part.reverse()
            lis_key_points_stack.extend(part)

        if row==3 or row==4:
            lis_AB.append((part[0],float(part[1]),float(part[2])))

        if row >=5:
            if len(part) != 4:
                continue
            if part[0] in lis_key_points_stack:
                lis_key_points.append(KeyPoint(part[0],float(part[1]),float(part[2]),float(part[3])))
                lis_key_points_stack.pop()
            lis_points.append(Point(part[0],float(part[1]),float(part[2]),float(part[3])))
        row+=1

    return Points(H0,lis_AB,lis_points,lis_key_points)


if __name__=='__main__':
    r=open('data/data.txt')
    print(r.lis_key_points)
    print(r.cross_distance)
    # print(r.calculation_interpolation_point(Point('K1',4534.227,3380.195,19.925 ),r.lis_points))
    # print(r.calculation_cross_sectional_area(Point('K0',4574.012,3358.300,12.922),Point('K1',4534.227,3380.195,19.925 )))
    for p in r.calculation_inter_point():
        print(p)
    m=r.calculate_plane_coordinates_elevations_cross_section_interpolation()
    print(m)
    for k,v in m[0].items():
        print(k)
        print(m[1][k])
        for i in v:
            print(i)



