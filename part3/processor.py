import math

def point_line_distance(o, i, n):
    """计算点 i 到线段 o-n 的垂直距离（海伦公式）"""
    # o, i, n 均为 [name, x, y] 格式
    xo, yo = float(o[1]), float(o[2])
    xi, yi = float(i[1]), float(i[2])
    xn, yn = float(n[1]), float(n[2])

    lon = math.hypot(xn - xo, yn - yo)
    if lon == 0:
        return math.hypot(xi - xo, yi - yo)

    loi = math.hypot(xi - xo, yi - yo)
    lin = math.hypot(xn - xi, yn - yi)

    s = (lon + loi + lin) / 2.0
    # 避免浮点误差导致负数
    area = math.sqrt(max(0.0, s * (s - lon) * (s - loi) * (s - lin)))
    return 2.0 * area / lon


def douglas_peucker(points, epsilon):
    """
    非递归 Douglas-Peucker 化简
    points: 列表，元素为 [name, x, y]
    epsilon: 距离阈值
    返回保留的点列表（原格式）
    """
    n = len(points)
    if n < 2:
        return points[:]

    # 标记点是否保留
    keep = [False] * n
    keep[0] = keep[-1] = True

    # 栈中存储待处理的区间 (start_idx, end_idx)
    stack = [(0, n - 1)]
    # print(stack)

    while stack:
        start, end = stack.pop()
        # print(start,end)
        if start + 1 >= end:   # 区间内无中间点
            continue

        # 找出距离线段 start->end 最远的点
        max_dist = 0.0
        max_idx = start
        for i in range(start + 1, end):
            d = point_line_distance(points[start], points[i], points[end])
            if d > max_dist:
                max_dist = d
                max_idx = i

        if max_dist >= epsilon:
            keep[max_idx] = True
            # 将两个子区间压栈（先处理左边或右边无所谓）
            stack.append((start, max_idx))
            stack.append((max_idx, end))
        # 否则该区间内所有中间点被舍弃，不做任何标记

    # 收集保留的点
    result = [points[i] for i in range(n) if keep[i]]
    return result


# 为了兼容你原来的调用名称，可以保留 dadt_processor 函数
def dadt_processor(points, epsilon):
    return douglas_peucker(points, epsilon)