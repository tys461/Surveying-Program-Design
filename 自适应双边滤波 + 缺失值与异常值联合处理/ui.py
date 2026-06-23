from PyQt6.QtCore import QFile,QIODevice,QTextStream
from prossce import MatriX

def open(path):
    file=QFile(path)
    matrix_lis=[]
    try:
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            print('文件打开失败')
            return
        else:
            try:
                stream=QTextStream(file)
                while not stream.atEnd():
                    part=stream.readLine().split()
                    part=[i  for i in part]
                    matrix_lis.append(part)
                return MatriX(matrix_lis)
            except:
                print('文件格式有误')
    except:
        print('文件打开失败')

if __name__=='__main__':
    matriX=open('deepseek_text_20260610_430fe8.txt')
    for i in matriX.bilateral_filtering():
        print(i)




