import math
from typing import List, Tuple

Point = Tuple[float, float]


# ------------------------------------------------------------
# 辅助函数：叉积
def cross(o: Point, a: Point, b: Point) -> float:
    """向量 OA × OB，正值表示 OA 到 OB 逆时针（左转）"""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


# 距离平方（用于极角排序中的等角处理）
def dist2(a: Point, b: Point) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


# ------------------------------------------------------------
# 1. Graham Scan 算法
def graham_scan(points: List[Point]) -> List[Point]:
    """
    返回凸包顶点（逆时针顺序，不含重复起点）
    时间复杂度 O(n log n)
    """
    if len(points) <= 1:
        return points[:]

    # 找到最下最左的点作为起点
    start = min(points, key=lambda p: (p[1], p[0]))  # (x, y) 中 y 为东坐标？这里y是第二个分量？注意：我们输入是(x,y)，x北，y东，比较y即东坐标最小，然后x最小

    # 极角排序：相对于 start
    def polar_angle(p: Point) -> float:
        return math.atan2(p[1] - start[1], p[0] - start[0])

    # 按极角排序，角度相同时按距离升序（确保近点先处理）
    points_sorted = sorted(points, key=lambda p: (polar_angle(p), dist2(p, start)))

    # 构建凸包栈
    stack = []
    for p in points_sorted:
        # 当栈至少有2点时，检查最后两点与当前点的转向，若非左转则弹出
        while len(stack) >= 2 and cross(stack[-2], stack[-1], p) <= 0:
            stack.pop()
        stack.append(p)
    return stack


# ------------------------------------------------------------
# 2. Andrew 算法（单调链）
def andrew(points: List[Point]) -> List[Point]:
    """
    返回凸包顶点（逆时针顺序，不含重复起点）
    时间复杂度 O(n log n)
    """
    if len(points) <= 1:
        return points[:]

    # 按 x 坐标（北坐标）为主，y（东坐标）为辅排序
    points_sorted = sorted(points, key=lambda p: (p[0], p[1]))

    # 构建下凸包
    lower = []
    for p in points_sorted:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # 构建上凸包
    upper = []
    for p in reversed(points_sorted):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # 合并，去掉下凸包的最后一个点和上凸包的最后一个点（它们分别是起点和终点，重复）
    return lower[:-1] + upper[:-1]


# ------------------------------------------------------------
# 3. Jarvis 步进法（礼品包装）
def jarvis(points: List[Point]) -> List[Point]:
    """
    返回凸包顶点（逆时针顺序，不含重复起点）
    时间复杂度 O(nh)，h 为凸包顶点数
    """
    n = len(points)
    if n <= 1:
        return points[:]

    # 找到最左最下的点作为起点（东坐标最小，北坐标最小）
    start = min(points, key=lambda p: (p[1], p[0]))
    hull = []
    p = start
    while True:
        hull.append(p)
        # 选择下一个点 q 使得所有其他点都在 (p, q) 的左侧或共线
        # 初始候选点为任意一个不同于 p 的点
        q = None
        for r in points:
            if r == p:
                continue
            if q is None:
                q = r
            else:
                # 检查 p->r 是否在 p->q 的逆时针方向（即叉积 > 0）
                # 若共线，选择距离更远的点
                c = cross(p, q, r)
                if c > 0 or (c == 0 and dist2(p, r) > dist2(p, q)):
                    q = r
        p = q
        # 当回到起点时结束
        if p == start:
            break
    return hull


