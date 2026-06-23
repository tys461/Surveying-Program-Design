import math
import copy


class MyMatrix:
    def __init__(self, core_x: list, core_y: list, matrix: list):
        self.core_x = core_x
        self.core_y = core_y
        self.matrix_data = matrix
        self.l_r = len(self.matrix_data)
        self.l_c = len(self.matrix_data[0])
        self.all_meam = self.count_all_meam()

    def count_all_meam(self):
        meam = []
        for row in range(self.l_r):
            for col in range(self.l_c):
                p = self.matrix_data[row][col]
                if p != 'NaN' and 0 < float(p) < 200:
                    meam.append(float(p))
        return sum(meam) / len(meam)

    def mirror(self, idx, size):
        """对边界区镜像填充"""
        if idx < 0:
            return -idx - 1
        if idx >= size:
            return 2 * size - idx - 1
        return idx

    def __repair_point(self, row, col, lis, dis):
        """使用其 3×3 邻域内所有有效值的算术平均值填充"""
        mean = []
        for r in range(-int(dis / 2), dis - 1, 1):
            for c in range(--int(dis / 2), dis - 1, 1):
                if r == c == 0:
                    continue
                nr = self.mirror(r + row, self.l_r)
                nc = self.mirror(c + col, self.l_c)
                mean.append(float(lis[nr][nc]))
        if len(mean) < 3:
            if dis > 7:
                return f'{self.all_meam:.1f}'
            else:
                return self.__repair_point(row, col, lis, dis * 2 - 1)
        mean = sum(mean) / len(mean)

        return f'{mean:.1f}'

    def missing_value_repair(self):
        """ 缺失值修复（邻域均值）"""
        matrix_data = copy.deepcopy(self.matrix_data)
        for row in range(self.l_r):
            for col in range(self.l_c):
                # if row==0 or col==0 or row==self.l_r-1  or col==self.l_c-1:
                #     continue
                if self.matrix_data[row][col] == 'NaN':
                    average = self.__repair_point(row, col, self.matrix_data, 3)
                    matrix_data[row][col] = average

        return matrix_data

    def __calculate_gradient_x_or_y(self, row, col, lis, core):
        count = 0
        debug = (row == 1 and col == 0) or (row == 2 and col == 0)
        for r in (-1, 0, 1):
            for c in (-1, 0, 1):
                nr = self.mirror(r + row, self.l_r)
                nc = self.mirror(c + col, self.l_c)
                count += float(core[1 + r][1 + c]) * float(lis[nr][nc])
        return f'{count:.1f}'

    def calculate_gradient_amplitude(self, repaired_matrix):
        '''使用 Sobel 算子 分别计算 x 方向（水平）和 y 方向（垂直）的梯度'''
        gradient_count = []
        gradient_degree = []
        repaired_matrix_copy_x = copy.deepcopy(repaired_matrix)
        repaired_matrix_copy_y = copy.deepcopy(repaired_matrix)
        repaired_matrix = self.missing_value_repair()

        for row in range(self.l_r):
            for col in range(self.l_c):
                # if row==0 or col==0 or row==self.l_r-1  or col==self.l_c-1:
                #     continue
                '''计算 x 方向（水平)梯度'''
                average_x = self.__calculate_gradient_x_or_y(row, col, repaired_matrix, self.core_x)
                repaired_matrix_copy_x[row][col] = average_x
                '''y 方向（垂直）梯度'''
                average_y = self.__calculate_gradient_x_or_y(row, col, repaired_matrix, self.core_y)
                repaired_matrix_copy_y[row][col] = average_y

        for row in range(self.l_r):
            gradient_count.append([])
            gradient_degree.append([])
            for col in range(self.l_c):
                c = float(repaired_matrix_copy_x[row][col]) ** 2 + float(repaired_matrix_copy_y[row][col]) ** 2
                gradient_count[-1].append(f'{math.sqrt(c):.1f}')
                rad = math.atan2(float(repaired_matrix_copy_y[row][col]), float(repaired_matrix_copy_x[row][col]))
                gradient_degree[-1].append(f'{math.degrees(rad):.1f}')

        return gradient_count, gradient_degree

    def __judge_angle(self, row, col, degree, lis):
        """量化规则"""
        if -22.5 < float(degree) < 22.5 or 157.5 < float(degree) < 180:
            if float(lis[row][col - 1]) < float(degree) and float(lis[row][col + 1]) < float(degree):
                return f'{float(degree):.1f}'
            else:
                return '0.0'
        if 22.5 < float(degree) < 67.5:
            if float(lis[row - 1][col + 1]) < float(degree) and float(lis[row + 1][col - 1]) < float(degree):
                return f'{float(degree):.1f}'
            else:
                return '0.0'
        if 67.5 < float(degree) < 112.5:
            if float(lis[row - 1][col]) < float(degree) and float(lis[row + 1][col]) < float(degree):
                return f'{float(degree):.1f}'
            else:
                return '0.0'
        if 112.5 < float(degree) < 157.5:
            if float(lis[row - 1][col - 1]) < float(degree) and float(lis[row + 1][col + 1]) < float(degree):
                return f'{float(degree):.1f}'
            else:
                return '0.0'

    def non_maximum_suppression(self, gradient_degree):
        """非极大值抑制（NMS）后的梯度幅值 """
        suppression_gradient_degree = copy.deepcopy(gradient_degree)
        for row in range(self.l_r):
            for col in range(self.l_c):
                if row == 0 or col == 0 or row == self.l_r - 1 or col == self.l_c - 1:
                    continue
                judge_result = self.__judge_angle(row, col, gradient_degree[row][col], gradient_degree)
                suppression_gradient_degree[row][col] = judge_result
        return suppression_gradient_degree

    def adaptive_threshold_segmentation(self, suppression_gradient_degree):
        """自适应阈值分割函数"""
        threshold_segmentation = copy.deepcopy(suppression_gradient_degree)

        apl = 1.2
        bata = 0.5
        mean = 0
        dic_not_zero = {}  # 将非零点储存在字典中

        for row in range(self.l_r):
            for col in range(self.l_c):
                # if row==0 or col==0 or row==self.l_r-1  or col==self.l_c-1:
                #     continue
                if suppression_gradient_degree[row][col] != '0.0':
                    dic_not_zero[(row, col)] = suppression_gradient_degree[row][col]
                    mean += float(suppression_gradient_degree[row][col])

        mean = mean / len(dic_not_zero)
        standard_deviation = sum([(mean - float(i)) ** 2 for i in dic_not_zero.values()])
        standard_deviation = math.sqrt(standard_deviation / len(dic_not_zero))
        high = mean + apl * standard_deviation
        low = mean + bata * standard_deviation

        for k, v in dic_not_zero.items():
            row, col = k
            if float(v) > high:
                threshold_segmentation[row][col] = '225.0'
            if low < float(v) < high:
                threshold_segmentation[row][col] = '128.0'
            if float(v) < low:
                threshold_segmentation[row][col] = '0.0'

        return threshold_segmentation
