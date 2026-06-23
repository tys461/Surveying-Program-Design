import copy
import statistics
from PyQt6.QtCore import QFile,QTextStream,QIODevice

def open(path):
    file=QFile(path)
    lis_data=[]
    try:
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            print('文件打开失败')
        else:
            try:
                stream=QTextStream(file)
                while not stream.atEnd():
                    for i in range(10):
                        lis_data.append(float(stream.readLine().strip()))
                return Matrix(lis_data)
            except:
                print('文件格式不对')

    except:
        print('文件打开失败')



class Matrix:
    def __init__(self,lis_data):
        self.lis_data=lis_data

    def reflective_filling(self,k,size):
        if k<0:
            return -k-1
        if k>=size:
            return 2*size-k-1
        return k

    def rough_error_detection_replacement(self):
        lis_data = copy.deepcopy(self.lis_data)
        n = len(lis_data)
        half_win = 5
        for i in range(n):
            window = []
            for k in range(-half_win, half_win + 1):
                idx = self.reflective_filling(i + k, n)
                window.append(self.lis_data[idx])
            median_win = statistics.median(window)
            abs_devs = [abs(v - median_win) for v in window]
            mad_win = statistics.median(abs_devs)
            sigma = 1.4826 * mad_win
            if abs(self.lis_data[i] - median_win) > 3.5 * sigma:
                lis_data[i] = median_win
                print(median_win)
        return lis_data





if __name__=='__main__':
    r=open('deepseek_text_20260610_7438da.txt')
    r.rough_error_detection_replacement()
    # for i in r.rough_error_detection_replacement():
    #     print(i)

