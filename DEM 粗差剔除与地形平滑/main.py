from PyQt6.QtCore import QFile,QTextStream,QIODevice
from prossce import Matrix

def open(path):
    file=QFile(path)
    lis_data=[]
    try:
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            print('文件件打开失败')
            return
        else:
            try:
                stream=QTextStream(file)
                while not  stream.atEnd():
                    part=stream.readLine().split()
                    lis_data.append(part)
                return Matrix(lis_data)
            except ValueError as e:
                print(f'文件格式有误{e}')
    except:
        print(f'文件打开失败')

if __name__=='__main__':
    r=open('deepseek_text_20260610_456593.txt')
    # r.adaptive_filtering()
    # for i in r.lis_data:
    #     print(i)
    # print('\n')
    for i in r.adaptive_filtering():
        print(i)
