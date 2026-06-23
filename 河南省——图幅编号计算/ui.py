from PyQt6.QtCore import QFile,QTextStream,QIODevice

def open(path):
    file=QFile(path)
    lo_la_sa=[]
    map={}
    if  not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件打开失败')
        return
    else:
        stream=QTextStream(file)
        while not stream.atEnd():
            part1=stream.readLine().split(',')
            part2=stream.readLine().split(',')
            if len(part1)==3 and len(part2)==3:
                lo_la_sa.append([float(part2[0]),float(part2[1]),part2[2]])
            if len(part1)==2 and len(part2)==2:
                m=map.get(part1[0],[])
                m.append([part2[0],part2[1]])
                map[part1[0]]=m

    return lo_la_sa,map

if __name__=='__main__':
    print(open('data/data.txt'))
