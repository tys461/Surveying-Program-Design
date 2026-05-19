from PyQt6.QtCore import QTextStream,QFile,QIODevice


def open_Latitude_longitude(input_file):
    file = QFile(input_file)
    lis_point=[]
    longitude_average=0
    latitude_average=0
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件读取失败')
        return
    stream=QTextStream(file)
    while not stream.atEnd():
        line = stream.readLine()
        parts = line.split(',')
        if len(parts) == 3:
            lis_point.append([parts[0], float(parts[1]), float(parts[2])])
    for i in lis_point:
        longitude_average+=i[1]
        latitude_average+=i[2]
    lis_point.append(['Pavg',f'{longitude_average/len(lis_point):.5f}'
                         ,f'{latitude_average/len(lis_point):.5f}'])
    print(lis_point)
    # print(chr(65))

    return lis_point


def open_frame_number(input_file):
    file = QFile(input_file)
    list_frame_number=[]
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件读取失败')
        return
    stream=QTextStream(file)
    while not stream.atEnd():
        line=stream.readLine()
        parts=line.split(',')
        list_frame_number.append(parts)
    return list_frame_number


def write_result(file,data):
    fiel=QFile(file)
    if fiel.open(QIODevice.OpenModeFlag.WriteOnly):
        for i in data:
            for d in i:
                fiel.write(f"{data.index(i) + 1} ".encode('utf-8'))
                fiel.write(f"{d} ".encode('utf-8'))
                for a in i.get(d):
                    fiel.write(f"{a} ".encode('utf-8'))
                fiel.write('\n'.encode('utf-8'))
    fiel.close()


