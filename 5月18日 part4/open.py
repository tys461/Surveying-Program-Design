from PyQt6.QtCore import QFile,QIODevice,QTextStream

def open_data(fiel_path):
    lis_point=[]
    file=QFile(fiel_path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件读取失败')
        return
    stream = QTextStream(file)
    while  not stream.atEnd():
        line = stream.readLine()
        line.encode('utf-8')
        parts=line.split()
        if len(parts) == 4:
            lis_point.append([parts[0], float(parts[1]), float(parts[2]),float(parts[3])])
    return lis_point
