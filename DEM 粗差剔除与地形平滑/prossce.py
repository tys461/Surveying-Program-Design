import math
import copy
import statistics


class Matrix:
    def __init__(self,lis_data):
        self.__lis_data=lis_data
        self.check_bad()

    def mirror(self,idx,size):
        '''边缘镜像'''
        if idx<0:
            return -idx-1
        if idx>=size:
            return 2*size -idx-1
        return idx

    # def idw_calculation(self, row, col, lis):
    #     """反距离加权插值，使用3x3邻域内的有效点"""
    #     total_weight = 0.0
    #     weighted_sum = 0.0
    #     for dr in (-1, 0, 1):
    #         for dc in (-1, 0, 1):
    #             if dr == 0 and dc == 0:
    #                 continue
    #             nr, nc = row + dr, col + dc
    #             # 只取矩阵范围内的点，且不能是 NaN
    #             if 0 <= nr < len(lis) and 0 <= nc < len(lis[0]):
    #                 val = float(lis[nr][nc])
    #                 if not math.isnan(val):  # 有效值
    #                     d = math.hypot(dr, dc)  # 欧氏距离 = sqrt(dr^2+dc^2)
    #                     weight = 1.0 / (d * d) if d != 0 else 0
    #                     total_weight += weight
    #                     weighted_sum += weight * val
    #     if total_weight == 0:
    #         # 如果没有有效点，返回全局均值（或保留NaN）
    #         return 'NaN'
    #     return weighted_sum / total_weight
    def global_mean(self, lis):
        """计算整个矩阵的非 NaN 值的均值"""
        total = 0.0
        count = 0
        for row in lis:
            for val in row:
                try:
                    v = float(val)
                    if not math.isnan(v):
                        total += v
                        count += 1
                except (ValueError, TypeError):
                    continue
        return total / count if count > 0 else float('nan')

    def idw_calculation(self, row, col, lis, max_radius=3):
        """
        反距离加权插值，逐步扩大搜索窗口（半径1..max_radius）
        直到找到至少2个有效点，然后计算IDW加权平均值。
        如果最终有效点不足2个，返回全局均值。
        """
        rows = len(lis)
        cols = len(lis[0])
        best_points = []  # 存储 (值, 距离)
        best_radius = None

        # 从半径1开始尝试，半径每增加1，窗口边长增加2
        for radius in range(1, max_radius + 1):
            points = []
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        val = lis[nr][nc]
                        # 转换为浮点数（处理字符串或数字）
                        try:
                            v = float(val)
                        except (ValueError, TypeError):
                            continue
                        if not math.isnan(v):
                            d = math.hypot(dr, dc)  # 欧氏距离
                            points.append((v, d))
            if len(points) >= 2:
                # 找到足够点，使用当前半径的点（不继续扩大）
                best_points = points
                best_radius = radius
                break
            else:
                # 当前半径点不足，继续扩大
                continue

        if best_points:
            total_weight = 0.0
            weighted_sum = 0.0
            for v, d in best_points:
                w = 1.0 / (d * d)
                total_weight += w
                weighted_sum += w * v
            return weighted_sum / total_weight
        else:
            # 所有半径尝试后仍不足2个点，返回全局均值
            return self.global_mean(lis)

    def check_bad(self):
        # 先将所有数据转为 float，'NaN' 转为 float('nan')
        self.lis_data = []
        for row in self.__lis_data:
            new_row = []
            for val in row:
                if val == 'NaN':
                    new_row.append(float('nan'))
                else:
                    new_row.append(float(val))
            self.lis_data.append(new_row)

        # 修复缺失值
        for row in range(len(self.lis_data)):
            for col in range(len(self.lis_data[0])):
                if math.isnan(self.lis_data[row][col]):
                    idw_val = self.idw_calculation(row, col, self.lis_data)
                    self.lis_data[row][col] = idw_val
        return copy.deepcopy(self.lis_data)

    def local_slope_calculation(self,row,col,lis):
        """计算局部坡度"""
        local_slope=[]
        for idx in range(-1,2,2):
            if 0<=row+idx<len(lis):
                count=abs(lis[row][col]-lis[row+idx][col])
                local_slope.append(count)

        for idx in range(-1, 2, 2):
            if 0 <= idx+col < len(lis[0]):
                count=abs(lis[row][col] - lis[row][idx+col])
                local_slope.append(count)
        return max(local_slope)

    def standard_calculation(self, row, col, lis):
        """返回 (局部标准差, 局部均值)，基于3x3邻域（镜像填充，包含所有8个邻域点）"""
        values = []
        median=[]
        rows, cols = len(lis), len(lis[0])

        for dr in range(-1, 2, 1):
            for dc in range(-1, 2, 1):
                if dr == 0 and dc == 0:
                    continue
                nr = self.mirror(row + dr, rows)
                nc = self.mirror(col + dc, cols)
                values.append(lis[nr][nc])
                median.append(lis[nr][nc])
        n = len(values)  # 恒为8
        mean = sum(values) / n
        variance = sum((v - mean) ** 2 for v in values) / (n - 1)
        std = math.sqrt(variance)
        median.sort()
        return std, mean,median

    def  rough_error_detectio(self):
        """粗差检测"""
        T=6.0

        for row in range(len(self.lis_data)):
            for col in range(len(self.lis_data[0])):
                local_slope=self.local_slope_calculation(row,col,self.lis_data)
                standard,mu,median=self.standard_calculation(row,col,self.lis_data)
                if local_slope>T and abs(self.lis_data[row][col]-mu)>2.5*standard:
                    self.lis_data[row][col]=statistics.median(median)
    #
    def gao_filtering(self, row, col, lis):
        r=0
        wight=0
        rows, cols = len(lis), len(lis[0])
        for dr in range(-1, 2, 1):
            for dc in range(-1, 2, 1):
                nr = self.mirror(row + dr, rows)
                nc = self.mirror(col + dc, cols)
                core=math.exp(-(dr**2+dc**2)/2)
                wight+=core
                r+=core*lis[nr][nc]
        return r/wight

    def bilateral_filtering(self,row, col, lis):
        """边缘区 5×5双边滤波"""
        s_d=2.0
        s_r=12.0

        total_weight=0
        weighty_sum=0
        rows, cols = len(lis), len(lis[0])
        for dr in range(-2, 3, 1):
            for dc in range(-2, 3, 1):
                mr=self.mirror(row+dr,rows)
                mc=self.mirror(col+dc,cols)
                weight=(math.exp(-(dr**2+dc**2)/(2*(s_d**2)))*
                        math.exp(-(lis[mr][mc]-lis[row][col])**2/(2*(s_r**2))))
                total_weight+=weight
                weighty_sum+=weight*lis[mr][mc]

        return  weighty_sum/total_weight if total_weight!=0 else 0



    def adaptive_filtering(self):
        """自适应滤波"""
        self.rough_error_detectio()
        lis_result=copy.deepcopy(self.lis_data)
        for row in range(len(self.lis_data)):
            for col in range(len(self.lis_data)):
                standard,mu,median=self.standard_calculation(row,col,self.lis_data)
                CV =standard/mu
                if CV<0.015:
                    r=self.gao_filtering(row,col,self.lis_data)
                    lis_result[row][col]=f'{r:.2f}'
                if 0.015<=CV<=0.05:
                    r = self.bilateral_filtering(row, col, self.lis_data)
                    lis_result[row][col]=f'{r:.2f}'
        return lis_result