import re
from PyQt6.QtCore import QFile,QTextStream,QIODevice
from process_ds import *

def open_file(path):
    """读取文件"""
    file=QFile(path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print("读取文件失败")
        return

    stream=QTextStream(file)

    frame_number=stream.readLine().split(',')[0]
    lis_AD=[]
    while not stream.atEnd():
        line=stream.readLine()
        part=line.split(',')
        if re.search('[A-Z]\d+',line):
            administrativeDistrict=AdministrativeDistrict(line,[])
            lis_AD.append(administrativeDistrict)
        if len(part)==2:
            lis_AD[-1].lis_S.append(list(map(lambda x:round(float(x),4),part)))

    file.close()
    return Data(frame_number,lis_AD)

if __name__=='__main__':
    r=open_file('data/data.txt')
    # r.coordinate_conversion(r.lis_AD[0].lis_S)
    P=r.map_sheet_numbering_calculation(r.f_n,Table)
    print(P)