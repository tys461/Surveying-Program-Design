from PyQt6.QtWidgets import QFileDialog,QMainWindow
from PyQt6.QtCore import QFile,QIODevice,QTextStream
from prossce import*



def open(path):
    file=QFile(path)
    lis_point=[]
    if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print('文件打开失败')
        return
    else:
        try:
            stream=QTextStream(file)
            while not stream.atEnd():
                line=stream.readLine()
                part=line.split(',')
                p=Point(int(part[0]),float(part[1]),float(part[2]),float(part[3]))
                lis_point.append(p)
            return lis_point
        except:
            print('文件格式不对')

if __name__=='__main__':
    if __name__ == '__main__':
        lis = open('散点数据.txt')
        points = Points(lis)
        triangles = points.generate_initial_triangulation_network()
        print(f"最终三角形个数: {len(triangles)}")

        # 创建追踪器
        tracer = ContourTracer(lis, triangles)

        # 遍历高程范围：从 9 到 17，步长 1
        all_contours = []
        for h in range(9, 18):  # 9,10,11,...,17
            result = tracer.trace_contour(h)
            all_contours.extend(result)
            print(f"高程 {h}: 追踪到 {len(result)} 条等高线")

        print(f"总计追踪到 {len(all_contours)} 条等高线段")

        # 打印第一条结果看看
        if all_contours:
            print(f"第一条等高线点数: {len(all_contours[0])}")

