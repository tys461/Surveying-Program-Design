import math
import statistics
import copy

class MatriX:
    def __init__(self,lis_data:list):
        self.__data=lis_data

    def mirror(self,idx, size):
        '''镜像填充'''
        if idx < 0:
            return -idx - 1
        elif idx >= size:
            return 2 * size - idx - 1
        return idx

    '''取邻域值'''
    def __round_core(self,row,col,lis):
        result=[]
        for round_row in range(-1,2,1):
            for round_col in range(-1,2,1):
                if round_row == 0 and round_col == 0 :
                    continue
                if  row+round_row>=0 and row+round_row<15 and col+round_col>=0 and col+round_col<15 :
                    result.append(lis[row+round_row][col+round_col])
        return [float(i) for i in  result]


    def weighted_formula(self, row, col, lis_data):
        '''高斯加权替换'''
        total_weight = 0.0
        total_value = 0.0
        sigma = 1.0  # 可根据需要调整
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue  # 排除中心点
                nr = self.mirror(row + dr, 15)
                nc = self.mirror(col + dc, 15)
                weight = math.exp(-(dr * dr + dc * dc) / (2 * sigma * sigma))
                total_value += weight * float(lis_data[nr][nc])
                total_weight += weight
        return total_value / total_weight if total_weight != 0 else float(lis_data[row][col])


    def fix_missing_values(self):
        '''修复缺失值 检测并修复异常值'''
        lis_data=copy.deepcopy(self.__data)
        for row in range(len(lis_data)):
            for col in range(len(lis_data[0])):

                _round=self.__round_core(row, col, lis_data)
                p=float(lis_data[row][col])
                '''邻域均值'''
                mean=sum(_round)/len(_round)
                '''邻域样本标准差'''
                standard=sum(map(lambda x:(x-mean)**2,_round))/(len(_round)-1)
                standard=math.sqrt(standard)

                '''检测修复缺失值'''
                if lis_data[row][col]=='nan' :
                    if len(_round)>=3:
                        _round.sort()
                        lis_data[row][col]=f'{statistics.median(_round):.1f}'
                '''检测并修复异常值'''
                if len(_round) >= 5:
                    if abs(p-mean)>3*standard:
                        lis_data[row][col] =f'{self.weighted_formula(row,col,lis_data):.1f}'
        return lis_data


    def filtering_five(self,row,col,lis):
        d=2.0
        r=15.0
        total_weight=0
        weighted_sum=0
        center=float(lis[row][col])
        for row_idx in range(-2,3,1):
            for col_idx in range(-2, 3, 1):
                if row_idx == 0 and col_idx == 0:
                    continue  # 排除中心点
                nr = self.mirror(row + row_idx, 15)
                nc = self.mirror(col + col_idx, 15)
                neig=float(lis[nr][nc])
                e1=math.exp(-(row_idx**2+col_idx**2)/(2*(d**2)))
                e2=math.exp(-(float(lis[nr][nc])-center)**2/(2*(r**2)))
                weight=e1*e2
                total_weight += weight
                weighted_sum += weight * neig
        return weighted_sum / total_weight

    def bilateral_filtering(self):
        lis_data=self.fix_missing_values()
        lis_data_copy=copy.deepcopy(lis_data)
        center_x, center_y = 7, 7
        radius_circle = 5
        for row in range(len(lis_data)):
            for col in range(len(lis_data[0])):
                if (row-center_x)**2 + (col-center_y)**2<=radius_circle**2:
                    filtered=self.filtering_five(row, col, lis_data)
                    lis_data_copy[row][col]=f'{filtered:.1f}'
        return lis_data_copy
