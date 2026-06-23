import math
from dataclasses import dataclass


@dataclass(slots=True)
class Point:
    n: str
    x: float
    y: float
    z: float

    def __repr__(self):
        return f'(n={self.n},x={self.x},y={self.y},z={self.z})'

    def __eq__(self, other):
        if isinstance(Point, other):
            raise
        return self.n == other.n

    def __hash__(self):
        return (self.n, self.x, self.y, self.z)


@dataclass(slots=True)
class Triangle:
    v0: int
    v1: int
    v2: int
    p0: Point
    p1: Point
    p2: Point
    area: float = 0.0
    is_active: bool = True  # 软删除标记

    def __repr__(self):
        return f'p0={self.p0},p2={self.p1},p1={self.p2},area={self.area}'

    @property
    def aver_h(self):
        """定义三点平均高程类方法"""
        return (self.p0.z + self.p1.z + self.p2.z) / 3


class Points:
    def __init__(self, h: float, lis_point: list[Point]):
        self.base_h = h
        self.lis_points = lis_point

    def __is_point_in_circumcircle(self, p: Point, tri: Triangle, pts: list[Point]):
        """判断点p是否在三角形tri的外接圆内（含边界）"""
        A, B, C = pts[tri.v0], pts[tri.v1], pts[tri.v2]

        # 为了避免浮点数溢出，将坐标平移到A点附近
        ax, ay = A.x - p.x, A.y - p.y
        bx, by = B.x - p.x, B.y - p.y
        cx, cy = C.x - p.x, C.y - p.y

        # 计算外接圆行列式（如果 > 0 则在圆内）
        det = (ax * ax + ay * ay) * (bx * cy - by * cx) - \
              (bx * bx + by * by) * (ax * cy - ay * cx) + \
              (cx * cx + cy * cy) * (ax * by - ay * bx)

        # 由于我们确保三角形顶点是逆时针顺序，若det > 0则表示点在圆内
        # 使用极小容差处理浮点数精度
        return det > 1e-10

    def __elimination_triangulation(self, tri: Triangle, lis: list[Point]):
        A, B, C = lis[tri.v0], lis[tri.v1], lis[tri.v2]

        A_B = math.hypot((B.x - A.x), (B.y - A.y))
        A_C = math.hypot((C.x - A.x), (C.y - A.y))
        C_B = math.hypot((B.x - C.x), (B.y - C.y))

        cos_A = (A_B * A_B + A_C * A_C - C_B * C_B) / (2 * A_B * A_C)
        cos_B = (A_B * A_B + C_B * C_B - A_C * A_C) / (2 * A_B * C_B)
        cos_C = (A_C * A_C + C_B * C_B - A_B * A_B) / (2 * A_C * C_B)

        cos_A = max(-1.0, min(1.0, cos_A))
        cos_B = max(-1.0, min(1.0, cos_B))
        cos_C = max(-1.0, min(1.0, cos_C))

        angles = [math.degrees(math.acos(cos_A)),
                  math.degrees(math.acos(cos_B)),
                  math.degrees(math.acos(cos_C))]

        return not (max(angles) > 160 or min(angles) < 5)

    def __create_ccw_triangle(self, v0, v1, v2, lis_p):
        """辅助函数：创建三角形并调整为逆时针"""
        tri = Triangle(v0, v1, v2, lis_p[v0], lis_p[v1], lis_p[v2])
        p0, p1, p2 = lis_p[tri.v0], lis_p[tri.v1], lis_p[tri.v2]
        cross = (p1.x - p0.x) * (p2.y - p0.y) - (p1.y - p0.y) * (p2.x - p0.x)
        if cross < 0:
            tri.v0, tri.v1 = tri.v1, tri.v0
            tri.p0, tri.p1 = tri.p1, tri.p0
        return tri

    def build_triangulation(self):
        """构建超级三角形（包括所有点）"""

        min_x = min(p.x for p in self.lis_points)
        max_x = max(p.x for p in self.lis_points)
        min_y = min(p.y for p in self.lis_points)
        max_y = max(p.y for p in self.lis_points)

        margin = 1.0  # 与C#一致
        rect_p1 = Point('R1', min_x - margin, min_y - margin, 0)
        rect_p2 = Point('R2', min_x - margin, max_y + margin, 0)
        rect_p3 = Point('R3', max_x + margin, max_y + margin, 0)
        rect_p4 = Point('R4', max_x + margin, min_y - margin, 0)

        lis_p = self.lis_points + [rect_p1, rect_p2, rect_p3, rect_p4]
        r_idx1, r_idx2, r_idx3, r_idx4 = len(self.lis_points), len(self.lis_points) + 1, len(self.lis_points) + 2, len(
            self.lis_points) + 3

        # 两个初始三角形，顺序任意但函数会调整
        triangles = [
            self.__create_ccw_triangle(r_idx1, r_idx2, r_idx3, lis_p),
            self.__create_ccw_triangle(r_idx1, r_idx3, r_idx4, lis_p)  # 注意此顺序对应矩形对角线
        ]

        s_indices = {r_idx1, r_idx2, r_idx3, r_idx4}

        """逐点插入,只遍历原始点，不遍历超级三角形的顶点"""
        for idx, p in enumerate(self.lis_points):
            bad_triangles = []

            # 找出所有外接圆包含点P的"坏三角形"
            for tri in triangles:
                if tri.is_active and self.__is_point_in_circumcircle(p, tri, lis_p):
                    tri.is_active = False  # 逻辑删除
                    bad_triangles.append(tri)

            # 寻找空腔边界（核心：使用字典统计边出现次数）
            edge_counter: dict[tuple[int, int], int] = {}
            for tri in bad_triangles:
                edge = [(tri.v0, tri.v1), (tri.v1, tri.v2), (tri.v2, tri.v0)]
                for e in edge:
                    key = (min(e[0], e[1]), max(e[0], e[1]))
                    edge_counter[key] = edge_counter.get(key, 0) + 1
            # 只保留出现1次的边（即空腔边界）
            boundary_edges = [key for key, cnt in edge_counter.items() if cnt == 1]

            # 连接新点P与边界边，生成新三角形
            for e in boundary_edges:
                # print(e[0])
                new_tri = Triangle(e[0], e[1], idx, lis_p[e[0]], lis_p[e[1]], p, True)
                new_tri = self.__create_ccw_triangle(new_tri.v0, new_tri.v1, new_tri.v2, lis_p)
                triangles.append(new_tri)

        final_triangles = [tri for tri in triangles if tri.is_active and
                           tri.v0 not in s_indices and
                           tri.v1 not in s_indices and
                           tri.v2 not in s_indices]

        return final_triangles

    def calculate_equilibrium_elevation(self):
        """计算平均高程"""
        triangles = self.build_triangulation()
        denominator = 0
        numerators = 0
        for triangle in triangles:
            p1, p2, p3 = triangle.p0, triangle.p1, triangle.p2
            x1, y1, h1 = p1.x, p1.y, p1.z
            x2, y2, h2 = p2.x, p2.y, p2.z
            x3, y3, h3 = p3.x, p3.y, p3.z

            S_i = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2
            h_i = triangle.aver_h - self.base_h

            numerators += h_i * S_i
            denominator += S_i
            triangle.area = S_i

        H_c = numerators / denominator if denominator != 0 else 0.0

        return triangles, H_c + self.base_h

    def __calculation_volume_interpolate(self, triangle: Triangle, check):
        """当三角形顶点中2个顶点高程小于参考高程或者大于大于参考高程时的处理方法
        check=True为挖方 反之为填方
        """
        p1, p2, p3 = triangle.p0, triangle.p1, triangle.p2
        x1, y1, h1 = p1.x, p1.y, p1.z
        x2, y2, h2 = p2.x, p2.y, p2.z
        x3, y3, h3 = p3.x, p3.y, p3.z

        x_i1 = x1 + abs((self.base_h - h1) / (h2 - h1)) * (x2 - x1)
        y_i1 = y1 + abs((self.base_h - h1) / (h2 - h1)) * (y2 - y1)

        x_i2 = x1 + abs((self.base_h - h1) / (h3 - h1)) * (x3 - x1)
        y_i2 = y1 + abs((self.base_h - h1) / (h3 - h1)) * (y3 - y1)

        S = abs((x_i1 - x1) * (y_i2 - y1) - (x_i2 - x1) * (y_i1 - y1)) / 2
        h = (h1 + self.base_h * 2) / 3 - self.base_h

        if check:
            """挖方"""
            V = S * h
            return V
        else:
            """填方"""
            V = (triangle.area - S) * ((self.base_h * 2 + h2 + h3 / 4 - self.base_h))
            return V

    def calculation_volume_excavated_fill_area_triangle(self):
        """三角形的挖方体积计算"""
        triangles, H_c = self.calculate_equilibrium_elevation()
        dic_fill_cul = {'fill': [], 'cul': []}
        V_fill = 0
        V_cul = 0

        for triangle in triangles:
            p1, p2, p3 = triangle.p0, triangle.p1, triangle.p2
            x3, y3, h3 = p3.x, p3.y, p3.z

            if all([x3 < self.base_h, y3 < self.base_h, h3 < self.base_h]):
                fill = triangle.area * (self.base_h - H_c)
                V_fill += fill
                dic_fill_cul['fill'].append(fill)
                dic_fill_cul['cul'].append(0)

            else:
                cul = triangle.area * (H_c - self.base_h)
                V_cul += cul
                dic_fill_cul['cul'].append(cul)
                dic_fill_cul['fill'].append(0)

            if sum([x3 < self.base_h, y3 < self.base_h, h3 < self.base_h]) == 2:
                """布尔值相加等于二判断有两个点小于参考高程 填方"""
                fill = self.__calculation_volume_interpolate(triangle, False)
                V_fill += fill
                dic_fill_cul['fill'].append(fill)
                dic_fill_cul['cul'].append(0)

            elif sum([x3 > self.base_h, y3 > self.base_h, h3 > self.base_h]) == 2:
                """布尔值相加等于二判断有两个点大于参考高程 挖方"""
                cul = self.__calculation_volume_interpolate(triangle, True)
                V_cul += cul
                dic_fill_cul['cul'].append(cul)
                dic_fill_cul['fill'].append(0)

        return V_fill, V_cul, dic_fill_cul
