import math

# def point_line_distance(o,i,n):
#     l_on=math.sqrt((o[1]-n[1])*(o[1]-n[1])+(o[2]-n[2])*(o[2]-n[2]))
#     l_oi=math.sqrt((o[1]-i[1])*(o[1]-i[1])+(o[2]-i[2])*(o[2]-i[2]))
#     l_in=math.sqrt((i[1]-n[1])*(i[1]-n[1])+(i[2]-n[2])*(i[2]-n[2]))
#     p=(l_on+l_oi+l_in)/2
#     # print(p,p*(p-l_on)*(p-l_oi)*(p-l_in))
#     s=math.sqrt(p*(p-l_on)*(p-l_oi)*(p-l_in))
#     d=2*(s/l_on)
#     return d
#
#
#
# def dadt_processor(points,epsilon):
#     start=points[0]
#     end=points[-1]
#
#     d_max=0
#     idx=0
#     print(len(points))
#     for i in range(1,len(points)):
#         d=point_line_distance(start,points[i],end)
#         if d>d_max:
#             d_max=d
#             idx=points[i][0]
#     if d_max<epsilon:
#         print(d_max)
#         return [start,end]
#     else:
#         left=dadt_processor(points[:idx+1],epsilon)
#         right=dadt_processor(points[idx:],epsilon)
#         return left[:-1]+right

import math

def point_line_distance(o, i, n):
    """计算点 i 到线段 o-n 的垂直距离（海伦公式）"""
    # o, i, n 均为 [name, x, y] 格式
    xo, yo = o[1], o[2]
    xi, yi = i[1], i[2]
    xn, yn = n[1], n[2]

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
    print(stack)

    while stack:
        start, end = stack.pop()
        print(start,end)
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