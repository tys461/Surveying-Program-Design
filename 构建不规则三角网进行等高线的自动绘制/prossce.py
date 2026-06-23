import math

class Point:
    """定义点类"""
    __slots__ = ('n', 'x', 'y', 'z')
    def __init__(self,n:int,x:float,y:float,z:float):
        self.n=n
        self.x=x
        self.y=y
        self.z=z


    def __repr__(self):
        return f'n={self.n};x={self.x};y={self.y};z={self.z}'

    def __hash__(self):
        """重写哈希值"""
        return hash((self.n,self.x,self.y,self.z))

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.n == other.n


class Points:
    """定义点集类"""
    def __init__(self,lis:list[Point]):
        self.points_lis=lis

    @property
    def min_y(self):
        """寻找y值最小点,并定义为属性方法"""
        return min(self.points_lis,key=lambda p:(p.y,p.x))

    @property
    def min_z(self):
        """寻找z值最小点,并定义为属性方法"""
        return min(self.points_lis, key=lambda p: p.z)

    @property
    def max_z(self):
        """寻找z值最小点,并定义为属性方法"""
        return max(self.points_lis, key=lambda p: p.z)

    def __degree_rank(self):
        """按夹角由小到大对points_lis中的点进行排序"""
        p0=self.min_y
        point_info=[]
        for i in self.points_lis:
            if i==p0:
                continue
            """计算∆x和∆y"""
            x=i.x-p0.x
            y=i.y-p0.y
            distance=x*x+y*y
            angle=math.atan2(y,x)*(180/math.pi)
            point_info.append((i,angle,distance))

        """对点排序以角度升序为住，距离降序为辅"""
        point_info.sort(key=lambda p:(p[1],-p[2]))
        """对于夹角相同的点，剔除近点"""
        lis_result=[]
        last_angle = None
        for p,angle,distance in point_info:
            if last_angle is None or abs(angle - last_angle) > 1e-9:
                lis_result.append(p)
                last_angle = angle
        return lis_result


    def __vector_product(self,p_i,p_j,p_k):
        """计算向量的x积"""
        x_i=p_i.x ; y_i=p_i.y
        x_j=p_j.x ; y_j=p_j.y
        x_k=p_k.x ; y_k=p_k.y

        return (x_i-x_j)*(y_k-y_j)-(y_i-y_j)*(x_k-x_j)>0

    def calculate_bump_point(self):
        """计算凸包点"""
        lis_rank=self.__degree_rank()
        if len(lis_rank) < 3:
            return lis_rank

        bump_stack=[]
        for i in lis_rank:
            while len(bump_stack)>=2 and  self.__vector_product(bump_stack[-2],bump_stack[-1],i):
                bump_stack.pop()
            bump_stack.append(i)
        bump_stack.append(self.min_y)
        return bump_stack

    def __calculate_the_center_radius(self, triangle):
        A, B, C = triangle
        x1, y1 = A.x, A.y
        x2, y2 = B.x, B.y
        x3, y3 = C.x, C.y

        d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        if abs(d) < 1e-12:  # 避免退化三角形
            return (0, 0), 0

        ux = ((x1 * x1 + y1 * y1) * (y2 - y3) + (x2 * x2 + y2 * y2) * (y3 - y1) + (x3 * x3 + y3 * y3) * (y1 - y2)) / d
        uy = ((x1 * x1 + y1 * y1) * (x3 - x2) + (x2 * x2 + y2 * y2) * (x1 - x3) + (x3 * x3 + y3 * y3) * (x2 - x1)) / d
        r = math.hypot(ux - x1, uy - y1)
        return (ux, uy), r

    def __count_edge(self, triangle_T2):
        """统计各边出现的次数剔除公共边（标准化方向）"""
        dic_edge = {}
        result = []

        for triangle in triangle_T2:
            A, B, C = triangle

            # 标准化三条边：确保元组中第一个点的编号小于第二个点
            # 利用点的 n 属性（整数）进行比较
            e1 = (A, B) if A.n < B.n else (B, A)
            e2 = (A, C) if A.n < C.n else (C, A)
            e3 = (B, C) if B.n < C.n else (C, B)

            dic_edge[e1] = dic_edge.get(e1, 0) + 1
            dic_edge[e2] = dic_edge.get(e2, 0) + 1
            dic_edge[e3] = dic_edge.get(e3, 0) + 1

        # 提取只出现一次的边（边界边）
        for edge, count in dic_edge.items():
            if count == 1:
                result.append(edge)

        return result

    def __filter_triangles_by_angle(self, triangles, max_angle=160.0, min_angle=5.0):
        """
        根据角度约束过滤狭长三角形
        :param triangles: 输入的三角形列表（每个三角形是 (Point, Point, Point)）
        :param max_angle: 允许的最大角（度），默认160°
        :param min_angle: 允许的最小角（度），默认5°
        :return: 过滤后的三角形列表
        """
        valid_triangles = []

        for tri in triangles:
            A, B, C = tri

            # 1. 计算三条边长（使用 math.hypot 避免溢出且更稳定）
            a = math.hypot(B.x - C.x, B.y - C.y)  # 边 BC
            b = math.hypot(A.x - C.x, A.y - C.y)  # 边 AC
            c = math.hypot(A.x - B.x, A.y - B.y)  # 边 AB

            # 2. 防止退化三角形（面积为0）导致除零错误
            if a < 1e-12 or b < 1e-12 or c < 1e-12:
                continue  # 直接丢弃这种无效三角形

            # 3. 余弦定理求角度（注意：浮点数误差可能导致 cos 值略微超出 [-1, 1]）
            cos_A = (b * b + c * c - a * a) / (2 * b * c)
            cos_B = (a * a + c * c - b * b) / (2 * a * c)
            cos_C = (a * a + b * b - c * c) / (2 * a * b)

            # 将 cos 值强行截断到 [-1, 1] 区间，防止 math.acos 报错
            cos_A = max(-1.0, min(1.0, cos_A))
            cos_B = max(-1.0, min(1.0, cos_B))
            cos_C = max(-1.0, min(1.0, cos_C))

            # 计算角度（弧度转度）
            angle_A = math.degrees(math.acos(cos_A))
            angle_B = math.degrees(math.acos(cos_B))
            angle_C = math.degrees(math.acos(cos_C))

            # 4. 判断是否满足约束
            max_ang = max(angle_A, angle_B, angle_C)
            min_ang = min(angle_A, angle_B, angle_C)

            # 如果最大角 > 阈值 或 最小角 < 阈值，则丢弃该三角形
            if max_ang > max_angle or min_ang < min_angle:
                continue

            valid_triangles.append(tri)

        return valid_triangles
    def generate_initial_triangulation_network(self):
        bump_stack = self.calculate_bump_point()  # 现在返回的是不含重复首点的凸包
        filter_lis = [p for p in self.points_lis if p not in bump_stack]

        # 初始化 T1（连接凸包边与第一个内部点）
        T1 = []
        for i in range(len(bump_stack) - 1):
            T1.append((filter_lis[0], bump_stack[i], bump_stack[i + 1]))
        T1.append((filter_lis[0], bump_stack[-1], bump_stack[0]))  # 闭合边
        T1_check = [True] * len(T1)

        # 逐点插入
        for P in filter_lis[1:]:
            T2 = []
            for idx, tri in enumerate(T1):
                if not T1_check[idx]:
                    continue
                center, r = self.__calculate_the_center_radius(tri)
                dist = math.hypot(center[0] - P.x, center[1] - P.y)
                if dist < r:  # 在圆内 -> 坏三角形
                    T1_check[idx] = False
                    T2.append(tri)

            S = self.__count_edge(T2)  # 这里边方向需标准化
            for a, b in S:
                T1.append((P, a, b))
                T1_check.append(True)


        raw_tri = [T1[i] for i in range(len(T1)) if T1_check[i]]
        filtered = self.__filter_triangles_by_angle(raw_tri)
        return filtered

        # 提取最终有效三角形
        # return self.__filter_triangles_by_angle([T1[i] for i in range(len(T1)) if T1_check[i]])


class ContourTracer:
    def __init__(self, points_lis, triangles):
        self.points = points_lis
        self.triangles = triangles
        # 初始化：每个三角形固定3个邻居位，默认(-1,-1)
        self.adj_list = [[(-1, -1) for _ in range(3)] for _ in range(len(triangles))]

        edge_map = {}
        for idx, tri in enumerate(self.triangles):
            A, B, C = tri
            # 标准化边，注意保存原始边序号 (0,1,2)
            edges = [(A, B, 0), (B, C, 1), (C, A, 2)]
            for p1, p2, edge_idx in edges:
                key = (min(p1.n, p2.n), max(p1.n, p2.n))
                if key not in edge_map:
                    edge_map[key] = []
                edge_map[key].append((idx, edge_idx))  # 存储 (三角形ID, 该三角形内的边序号)

        # 填充邻居：直接按索引位置赋值
        for edge, tris in edge_map.items():
            if len(tris) == 2:
                (t1_idx, e1_idx), (t2_idx, e2_idx) = tris[0], tris[1]
                # 关键修正：直接赋值给固定位置，确保 t1 的 e1 边对面是 t2，反之亦然
                self.adj_list[t1_idx][e1_idx] = (t2_idx, e2_idx)
                self.adj_list[t2_idx][e2_idx] = (t1_idx, e1_idx)
            else:
                # 边界边
                t_idx, e_idx = tris[0]
                self.adj_list[t_idx][e_idx] = (-1, -1)

        # 按边序号排序，确保 adj_list[i][0] 对应三角形的边0 (A-B)，以此类推
        # 因为上面的append顺序可能乱，重新整理一下
        for i in range(len(self.adj_list)):
            # 补全缺失的边界邻居
            while len(self.adj_list[i]) < 3:
                self.adj_list[i].append((-1, -1))

    def interpolate_point(self, p1, p2, h):
        """在边 p1-p2 上线性插值出高程为 h 的平面坐标"""
        z1, z2 = p1.z, p2.z
        if abs(z2 - z1) < 1e-12:
            return (p1.x, p1.y)  # 防止除零
        t = (h - z1) / (z2 - z1)
        return (p1.x + t * (p2.x - p1.x), p1.y + t * (p2.y - p1.y))

    def find_intersections_in_triangle(self, tri, h):
        """返回三角形中所有与等高线相交的边序号及交点坐标"""
        A, B, C = tri
        edges = [(A, B), (B, C), (C, A)]
        intersections = []
        for i, (p1, p2) in enumerate(edges):
            # 判断是否穿过 (h - z1) * (h - z2) < 0
            if (h - p1.z) * (h - p2.z) < 0:
                pt = self.interpolate_point(p1, p2, h)
                intersections.append((i, pt))
        return intersections

    def trace_contour(self, h, epsilon=1e-10):
        """追踪一条给定高程 h 的等高线"""
        # 1. 预处理：微调高程等于 h 的点，防止顶点歧义
        for p in self.points:
            if abs(p.z - h) < epsilon:
                p.z += epsilon  # 稍微扰动一下

        # 2. 初始化访问标记
        visited = [False] * len(self.triangles)
        contours = []  # 存储最终所有等高线片段

        # 3. 遍历所有三角形寻找起点
        for start_idx, tri in enumerate(self.triangles):
            if visited[start_idx]:
                continue

            # 找出该三角形内与等高线的交点
            inters = self.find_intersections_in_triangle(tri, h)
            if len(inters) < 2:
                continue  # 没有穿过，或者相切（只有一个点）

            # 准备两条边和对应的交点
            (edge_in, pt_in), (edge_out, pt_out) = inters[0], inters[1]

            # 标记起点已访问
            visited[start_idx] = True

            # ----- 开始追踪（这里处理闭曲线和开曲线） -----
            # 获取该三角形的邻居信息
            neighbors = self.adj_list[start_idx]

            # 找 entry 边对面的邻居
            next_idx, _ = neighbors[edge_in]

            # 如果 entry 边是边界（开曲线），或者顺着走能回到起点（闭曲线）
            # 我们采取一种万能的策略：分别从两条边出发走到尽头，再拼接

            # 路线1：从 pt_in 开始，沿三角网向前走（入口作为起点）
            leg1_points = []
            cur_idx = start_idx
            cur_edge = edge_in
            cur_pt = pt_in

            while True:
                # 获取当前三角形的出口（另一条边）
                cur_tri = self.triangles[cur_idx]
                cur_inters = self.find_intersections_in_triangle(cur_tri, h)
                # 找到不是 cur_edge 的那条边
                out_edge = None
                out_pt = None
                for e_idx, pt in cur_inters:
                    if e_idx != cur_edge:
                        out_edge = e_idx
                        out_pt = pt
                        break

                if out_edge is None:
                    break  # 理论上不可能

                # 记录这一段
                leg1_points.append(cur_pt)
                leg1_points.append(out_pt)  # 先存着，后续去重

                # 通过 out_edge 找邻居
                next_idx, next_edge_in = self.adj_list[cur_idx][out_edge]
                if next_idx == -1:  # 到达边界（开曲线）
                    break
                if next_idx == start_idx:  # 回到了起点（闭曲线）
                    # 闭曲线处理：直接收尾
                    contours.append(leg1_points)
                    # 把起点三角形的另一个邻居也标记一下以防重复
                    visited[start_idx] = True
                    break

                # 标记邻居，进入下一个三角形
                visited[next_idx] = True
                cur_idx = next_idx
                cur_edge = next_edge_in  # 在邻居中，这条边是 entry
                # 注意：此时的 cur_pt 应该是 out_pt，但为了查找出口，我们只需要边

            # 判断是否为开曲线（如果上一步没有返回闭曲线）
            if next_idx == -1:
                # 开曲线需要双向追溯！上面的 leg1_points 只跑了前半段
                # 重建数据：从起点反向跑另一条路
                # 先对 leg1_points 去重（因为双向搜索时，起点和终点会重叠）
                # 更稳健的做法：重新从起点出发，向另一个方向跑

                # 从起点三角形的另一条边（out_edge）出发，向另一个方向
                leg2_points = []
                cur_idx = start_idx
                cur_edge = out_edge  # 注意：反向跑时，入口变成之前的出口
                cur_pt = pt_out

                # 给起点做个标记，防止死循环，但不要覆盖 visited（因为 visited 是用于选起点的）
                temp_visited = set()
                temp_visited.add(start_idx)

                while True:
                    cur_tri = self.triangles[cur_idx]
                    cur_inters = self.find_intersections_in_triangle(cur_tri, h)
                    # 找出口（不是 cur_edge 的另一条边）
                    out_edge_2 = None
                    out_pt_2 = None
                    for e_idx, pt in cur_inters:
                        if e_idx != cur_edge:
                            out_edge_2 = e_idx
                            out_pt_2 = pt
                            break

                    if out_edge_2 is None:
                        break

                    leg2_points.append(cur_pt)
                    leg2_points.append(out_pt_2)

                    # 找邻居
                    next_idx_2, next_edge_in_2 = self.adj_list[cur_idx][out_edge_2]
                    if next_idx_2 == -1:  # 到达边界（另一头）
                        break
                    if next_idx_2 in temp_visited:  # 防止死循环
                        break

                    temp_visited.add(next_idx_2)
                    cur_idx = next_idx_2
                    cur_edge = next_edge_in_2

                # 合并两条腿：反向腿（从边界到起点） + 正向腿（从起点到边界）
                # 注意去重：将 leg2_points 反转，再拼接 leg1_points
                if leg1_points and leg2_points:
                    # leg2_points 是从起点跑到另一个边界，反转后变为 边界 -> 起点
                    # leg1_points 是从起点跑到一个边界，保持不变
                    # 合并时，去掉重复的起点（leg2[-1] 和 leg1[0] 都是起点坐标）
                    full_contour = list(reversed(leg2_points)) + leg1_points[1:]
                else:
                    full_contour = leg1_points

                contours.append(full_contour)

        # 恢复点的高程（避免影响下一次追踪）
        for p in self.points:
            if abs(p.z - (h - epsilon)) < epsilon or abs(p.z - (h + epsilon)) < epsilon:
                p.z = h

        return contours

