import re
from PyQt6.QtCore import QFile,QTextStream,QIODevice
from process import Gps,Satellite,Observation

def open(path):
    file=QFile(path)

    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件读取失败')
        return 0

    stream=QTextStream(file)
    part=re.compile(r'[-+]?\d*\.\d+').findall(stream.readLine())
    X0=float(part[0])
    Y0=float(part[1])
    Z0=float(part[2])
    lis_satellite=[]
    while not stream.atEnd():
        line =stream.readLine()
        part=line.split(',')
        if 'Satellite Number' in line:
            n_t = re.compile(r'[-+]?\d*\.?\d+').findall(line)
            lis_satellite.append(Satellite(int(n_t[0]),float(n_t[1]),[]))
        if len(part)==8:
            lis_satellite[-1].lis_Gps.append(Gps(part[0],float(part[1]),float(part[2]),float(part[3])
                            ,float(part[4]),float(part[5]),float(part[6]),float(part[7])))
    return Observation(X0,Y0,Z0,lis_satellite)

if __name__=='__main__':
    obs=open('data/GPS卫星数据.txt')
    for i in obs.lis_satellite:
        print(f'-----------{i.satellite_number}-------------')
        for g in i.lis_Gps:
            print(g)






