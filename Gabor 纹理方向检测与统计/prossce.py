import math
import copy


class MyMatrix:
    def __init__(self, lis_matrix: list):
        self.lis_matrix = lis_matrix
        self.row = len(lis_matrix)
        self.col = len(lis_matrix)

    def mirror(self, idx, size):
        """镜像填充判断是否出界"""
        if idx < 0:
            return -idx - 1
        if idx >= size:
            return 2 * size - idx - 1
        return idx

    def set_fabor_15x15_real(self, degree):
        """生成15x15Gabor核"""
        gabor_core = []
        zeta = 2.0
        gama = 0.5
        namta = 8.0
        rad = math.radians(degree)

        for row in range(-7, 8):
            gabor_core.append([])
            for col in range(-7, 8):
                x = col * math.cos(rad) + row * math.sin(rad)
                y = -col * math.sin(rad) + row * math.cos(rad)
                G_x_y = math.exp(-(x ** 2 + (gama ** 2) * (y ** 2)) / (2 * zeta ** 2)) * math.cos(
                    2 * math.pi * (x / namta))
                gabor_core[-1].append(float(f'{G_x_y:.3f}'))
        return gabor_core

    def set_fabor_15x15_false(self, degree):
        """生成15x15Gabor核"""
        gabor_core = []
        zeta = 2.0
        gama = 0.5
        namta = 8.0
        rad = math.radians(degree)

        for row in range(-7, 8):
            gabor_core.append([])
            for col in range(-7, 8):
                x = col * math.cos(rad) + row * math.sin(rad)
                y = -col * math.sin(rad) + row * math.cos(rad)
                G_x_y = math.exp(-(x ** 2 + (gama ** 2) * (y ** 2)) / (2 * zeta ** 2)) * math.sin(
                    2 * math.pi * (x / namta))
                gabor_core[-1].append(float(f'{G_x_y:.3f}'))
        return gabor_core

    def __calculation_point(self, row, col, lis_dat, gabor_core):
        """单个元素卷积计算"""
        result = 0
        for dr in range(-7, 8):
            for dc in range(-7, 8):
                nr = self.mirror(dr + row, self.row)
                nc = self.mirror(dc + col, self.col)
                result += lis_dat[nr][nc] * gabor_core[7 + dr][7 + dc]

        return float(f'{result:.3f}')

    def convolutional_calculation_all(self, core_real, core_false):
        """所有点卷积计算"""
        gabor_core_real = core_real
        gabor_core_false = core_false
        lis_matrix_m = []
        for row in range(self.row):
            lis_matrix_m.append([])
            for col in range(self.col):
                lis_matrix_real = self.__calculation_point(row, col, self.lis_matrix, gabor_core_real)
                lis_matrix_false = self.__calculation_point(row, col, self.lis_matrix, gabor_core_false)
                M = math.sqrt(lis_matrix_real * lis_matrix_real + lis_matrix_false * lis_matrix_false)
                lis_matrix_m[-1].append(float(f'{M:.3f}'))
        return lis_matrix_m

    def nms_extracts_peak_responses(self):
        """非极大值抑制（NMS）提取响应峰值"""
        lis_matrix_nms = self.convolutional_calculation_all(self.set_fabor_15x15_real(0), self.set_fabor_15x15_false(0))
        lis_matrix_nms_copy = self.convolutional_calculation_all(self.set_fabor_15x15_real(0),
                                                                 self.set_fabor_15x15_false(0))
        for row in range(self.row):
            for col in range(self.col):
                if 0 < col < self.col - 1:
                    p_i = lis_matrix_nms[row][col]  # 中间元素
                    lp_i = lis_matrix_nms_copy[row][col - 1]  # 左边元素
                    rp_i = lis_matrix_nms_copy[row][col + 1]  # 右边元素
                    if p_i < lp_i or p_i < rp_i:
                        lis_matrix_nms[row][col] = 0
        return lis_matrix_nms

    def directional_response_statistics(self):
        """方向响应统计（多方向滤波器组）"""
        dic_degree_count = {'d_0': 0, 'd_45': 0, 'd_90': 0, 'd_135': 0}

        gabor_core_real_0 = self.set_fabor_15x15_real(0)
        gabor_core_false_0 = self.set_fabor_15x15_false(0)

        gabor_core_real_45 = self.set_fabor_15x15_real(45)
        gabor_core_false_45 = self.set_fabor_15x15_false(45)

        gabor_core_real_90 = self.set_fabor_15x15_real(90)
        gabor_core_false_90 = self.set_fabor_15x15_false(90)

        gabor_core_real_135 = self.set_fabor_15x15_real(135)
        gabor_core_false_135 = self.set_fabor_15x15_false(135)

        lis_matrix_m_0 = self.convolutional_calculation_all(gabor_core_real_0, gabor_core_false_0)
        lis_matrix_m_45 = self.convolutional_calculation_all(gabor_core_real_45, gabor_core_false_45)
        lis_matrix_m_90 = self.convolutional_calculation_all(gabor_core_real_90, gabor_core_false_90)
        lis_matrix_m_135 = self.convolutional_calculation_all(gabor_core_real_135, gabor_core_false_135)

        for row in range(self.row):
            for col in range(self.col):
                dic_num = {'d_0': lis_matrix_m_0[row][col],
                           'd_45': lis_matrix_m_45[row][col],
                           'd_90': lis_matrix_m_90[row][col],
                           'd_135': lis_matrix_m_135[row][col]}

                max_direction = max([(i) for i in dic_num.items()], key=lambda l: l[1])
                dic_degree_count[max_direction[0]] = dic_degree_count[max_direction[0]] + 1

        return dic_degree_count
