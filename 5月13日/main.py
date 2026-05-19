from open import Open_dat
from dini03_parser import Dini03Parser

def main():
    # 1. 读取文件，得到按|分割的行列表
    opener = Open_dat()   # 内部 self.list_data 已存储
    raw_data = opener.list_data   # list of list

    # 2. 解析为 LineInfo
    parser = Dini03Parser(raw_data)
    line_info = parser.parse()

    # 3. 为每个测段设置起始点高程（需根据实际已知点补充）
    # 假设从文件某行提取到起点高程为 100.000
    if line_info.PartList:
        # print(line_info.PartList[0].StationList[3].FPtH)
        # part = line_info.PartList[0]  # 第一个测段
        # station = part.StationList[1]  # 第二个测站
        # sight = station.SightList[2]  # 第三次观测
        # print(sight.RD)

        part = line_info.PartList[0]
        part.StartPtH = 0.0   # 替换为实际高程
        # 如果知道终点已知高程，也可设置 part.EndPtH
        part.Reset()   # 执行计算，自动传递高程、计算高差等
        for i in line_info.PartList:
            print('--------------------------------------------------------')
            print(i.partName)
            for k in i.StationList:
                print('------------')
                print(k.FPtName,k.BPtH)
                for n in k.SightList:
                    print(n.ptName,n.RD,n.SType)
        # print(f"测段 {part.partName} 累计高差: {part.sh:.4f} m")
        # print(f"闭合差: {part.dz:.4f} m")
        # print(f"后视距总和: {part.Db:.2f} m, 前视距总和: {part.Df:.2f} m")

if __name__ == "__main__":
    main()