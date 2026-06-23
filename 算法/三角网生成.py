def build_triangulation(points: List[Point]) -> List[Triangle]:
    # 步骤1：构建超级三角形（必须包含所有点）
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)

    dx = max_x - min_x
    dy = max_y - min_y
    d_max = max(dx, dy) * 2  # 扩大2倍确保完全包裹

    # 超级三角形的三个顶点（放在点列表末尾）
    super_p1 = Point(min_x - d_max, min_y - d_max)
    super_p2 = Point(min_x + d_max * 2, min_y - d_max)
    super_p3 = Point(min_x, min_y + d_max * 2)

    # 将超级顶点加入点列表，记录它们的索引
    pts = points + [super_p1, super_p2, super_p3]
    s_idx1, s_idx2, s_idx3 = len(points), len(points) + 1, len(points) + 2

    # 初始化三角网（仅包含超级三角形）
    triangles = [Triangle(s_idx1, s_idx2, s_idx3, True)]

    # ===== 步骤2：逐点插入（这才是你问的循环，每个点都要执行） =====
    # 只遍历原始点，不遍历超级三角形的顶点
    for i, p in enumerate(points):
        bad_triangles = []

        # (1) 找出所有外接圆包含点P的"坏三角形"
        for tri in triangles:
            if tri.is_active and is_point_in_circumcircle(p, tri, pts):
                tri.is_active = False  # 逻辑删除
                bad_triangles.append(tri)

        # (2) 寻找空腔边界（核心：使用字典统计边出现次数）
        edge_counter: Dict[Tuple[int, int], int] = {}
        for tri in bad_triangles:
            # 提取三条边，并按大小排序以保证一致性
            edges = [(tri.v0, tri.v1), (tri.v1, tri.v2), (tri.v2, tri.v0)]
            for e in edges:
                key = (min(e[0], e[1]), max(e[0], e[1]))
                edge_counter[key] = edge_counter.get(key, 0) + 1

        # 只保留出现1次的边（即空腔边界）
        boundary_edges = [key for key, cnt in edge_counter.items() if cnt == 1]

        # (3) 连接新点P与边界边，生成新三角形
        for e in boundary_edges:
            new_tri = Triangle(e[0], e[1], i, True)  # i 是当前点的索引
            triangles.append(new_tri)

    # ===== 步骤3：删除包含超级三角形顶点的三角形 =====
    final_triangles = []
    for tri in triangles:
        if (tri.is_active and
                tri.v0 not in (s_idx1, s_idx2, s_idx3) and
                tri.v1 not in (s_idx1, s_idx2, s_idx3) and
                tri.v2 not in (s_idx1, s_idx2, s_idx3)):
            final_triangles.append(tri)

    return final_triangles