import numpy as np
import openpyxl
from openpyxl import Workbook
import os

# ---------------------------- 1. 数据读取 ----------------------------
def read_dem(filepath):
    """读取data.txt，返回40x40的numpy数组"""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                row = [float(x) for x in line.split(',')]
                data.append(row)
    return np.array(data, dtype=float)

# 原始DEM
dem_orig = read_dem('data.txt')
rows, cols = dem_orig.shape  # 40,40
g_30 = 30.0   # 原始分辨率
g_60 = 60.0   # 降分辨率后

# ---------------------------- 2. 统计（原始DEM） ----------------------------
min_elev = np.min(dem_orig)
max_elev = np.max(dem_orig)
mean_elev = np.mean(dem_orig)
# 区间统计（开区间）
count_40_50 = np.sum((dem_orig > 40) & (dem_orig < 50))
count_50_60 = np.sum((dem_orig > 50) & (dem_orig < 60))
count_60_70 = np.sum((dem_orig > 60) & (dem_orig < 70))
count_70_80 = np.sum((dem_orig > 70) & (dem_orig < 80))

print(f"原始DEM: min={min_elev:.2f}, max={max_elev:.2f}, mean={mean_elev:.2f}")
print(f"40-50: {count_40_50}, 50-60: {count_50_60}, 60-70: {count_60_70}, 70-80: {count_70_80}")

# ---------------------------- 3. 异常值检测与中值滤波 ----------------------------
# 全局最小值
global_min = min_elev
# 异常值掩码（内部点才处理，边界保持原值）
is_abnormal = (dem_orig - global_min) > 100

# 中值滤波结果，初始复制原始值
dem_median = dem_orig.copy()

# 3x3中值滤波，只处理内部点（行1-38，列1-38）且为异常值的点
for i in range(1, rows-1):
    for j in range(1, cols-1):
        if is_abnormal[i, j]:
            # 取3x3窗口（基于原始数据）
            window = dem_orig[i-1:i+2, j-1:j+2].flatten()
            median_val = np.median(window)
            dem_median[i, j] = median_val
# 边界点保持原值（包括异常边界点不处理）

# 保存result1.txt（保留1位小数）
with open('result1.txt', 'w', encoding='utf-8') as f:
    for i in range(rows):
        line = ','.join([f"{dem_median[i, j]:.1f}" for j in range(cols)])
        f.write(line + '\n')
print("中值滤波后DEM已保存至 result1.txt")

# ---------------------------- 4. 坡度角计算（基于中值滤波后DEM） ----------------------------
def calculate_slope(dem, g, rows, cols):
    """
    计算坡度角（度），边界为-1
    dem: 二维数组
    g: 格网分辨率
    返回坡度数组（与dem同尺寸）
    """
    slope = np.full_like(dem, -1.0, dtype=float)
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            # 提取3x3窗口
            z = dem[i-1:i+2, j-1:j+2]
            # 公式(1): x方向偏导
            dz_dx = ((z[0,2] + 2*z[1,2] + z[2,2]) - (z[0,0] + 2*z[1,0] + z[2,0])) / (8 * g)
            # 公式(2): y方向偏导
            dz_dy = ((z[2,0] + 2*z[2,1] + z[2,2]) - (z[0,0] + 2*z[0,1] + z[0,2])) / (8 * g)
            # 公式(3): 坡度（度）
            slope_rad = np.arctan(np.sqrt(dz_dx**2 + dz_dy**2))
            slope[i, j] = slope_rad * 180.0 / np.pi
    return slope

slope_median = calculate_slope(dem_median, g_30, rows, cols)

# 保存result2.txt
with open('result2.txt', 'w', encoding='utf-8') as f:
    for i in range(rows):
        line = ','.join([f"{slope_median[i, j]:.1f}" for j in range(cols)])
        f.write(line + '\n')
print("坡度角结果已保存至 result2.txt")

# 统计坡度角（忽略-1）
valid_slopes = slope_median[slope_median != -1]
slope_max = np.max(valid_slopes)
slope_min = np.min(valid_slopes)
slope_mean = np.mean(valid_slopes)
print(f"中值滤波后坡度角: max={slope_max:.2f}, min={slope_min:.2f}, mean={slope_mean:.2f}")

# ---------------------------- 5. 填洼计算 ----------------------------
# 找到中值滤波后DEM的最小值位置（取第一个）
min_idx = np.unravel_index(np.argmin(dem_median), dem_median.shape)
i0, j0 = min_idx
print(f"中值滤波后DEM最小值位置: ({i0}, {j0}), 高程={dem_median[i0, j0]:.2f}")

# 检查是否为内部点（应满足，否则无法填洼）
if 1 <= i0 <= rows-2 and 1 <= j0 <= cols-2:
    # 提取3x3窗口（原始中值滤波后的值）
    window = dem_median[i0-1:i0+2, j0-1:j0+2]
    center = window[1, 1]
    neighbors = np.array([window[0,0], window[0,1], window[0,2],
                          window[1,0], window[1,2],
                          window[2,0], window[2,1], window[2,2]])
    min_neighbor = np.min(neighbors)
    # 如果中心比所有邻居都低，则填洼
    if center < np.min(neighbors):
        new_elev = min_neighbor
    else:
        # 题目要求对该最小值格网填洼，但若条件不满足，按理不应改变；此处仍按邻居最小值处理
        new_elev = min_neighbor
    # 记录填洼后的高程
    filled_elev = new_elev
    # 重新计算该点的坡度角（使用新高程，邻居不变）
    dem_filled = dem_median.copy()
    dem_filled[i0, j0] = filled_elev
    # 重新计算该点坡度（仅该点）
    # 使用calculate_slope函数计算单个点，但需要临时数组
    slope_filled = calculate_slope(dem_filled, g_30, rows, cols)[i0, j0]
else:
    # 最小值在边界，按题目说明边界不参与填洼？但题目要求对最小值格网填洼，边界无法填洼，取原值
    filled_elev = dem_median[i0, j0]
    slope_filled = slope_median[i0, j0]
    print("警告：最小值位于边界，填洼操作未执行（保持原值）")

print(f"填洼后高程: {filled_elev:.2f}, 填洼后坡度角: {slope_filled:.2f}")

# ---------------------------- 6. 降分辨率 ----------------------------
# 对原始DEM进行2x2平均池化，得到20x20
new_rows, new_cols = rows // 2, cols // 2  # 20,20
dem_lowres = np.zeros((new_rows, new_cols))
for i in range(new_rows):
    for j in range(new_cols):
        block = dem_orig[2*i:2*i+2, 2*j:2*j+2]
        dem_lowres[i, j] = np.mean(block)

# 计算降分辨率后的坡度角（分辨率g=60）
slope_lowres = calculate_slope(dem_lowres, g_60, new_rows, new_cols)

# 保存result3.txt
with open('result3.txt', 'w', encoding='utf-8') as f:
    for i in range(new_rows):
        line = ','.join([f"{slope_lowres[i, j]:.1f}" for j in range(new_cols)])
        f.write(line + '\n')
print("降分辨率坡度角已保存至 result3.txt")

# 统计坡度角（忽略-1）
valid_low = slope_lowres[slope_lowres != -1]
low_max = np.max(valid_low)
low_min = np.min(valid_low)
low_mean = np.mean(valid_low)
print(f"降分辨率后坡度角: max={low_max:.2f}, min={low_min:.2f}, mean={low_mean:.2f}")

# ---------------------------- 7. 输出到Excel ----------------------------
wb = Workbook()
ws = wb.active
ws.title = "程序正确性"

# 结果对应表格顺序
results = [
    ("data.txt中DEM的最大值", max_elev),
    ("data.txt中DEM的最小值", min_elev),
    ("data.txt中DEM的平均值", mean_elev),
    ("DEM值大于40米且小于50米的格网个数", count_40_50),
    ("DEM值大于50米且小于60米的格网个数", count_50_60),
    ("DEM值大于60米且小于70米的格网个数", count_60_70),
    ("DEM值大于70米且小于80米的格网个数", count_70_80),
    ("中值滤波后的坡度角最大值", slope_max),
    ("中值滤波后的坡度角最小值", slope_min),
    ("中值滤波后的坡度角平均值", slope_mean),
    ("对中值滤波后DEM最小值对应的格网进行填注后的高程", filled_elev),
    ("对中值滤波后DEM最小值对应的格网进行填注后的坡度角", slope_filled),
    ("降低分辨率后的坡度角最大值", low_max),
    ("降低分辨率后的坡度角最小值", low_min),
    ("降低分辨率后的坡度角平均值", low_mean),
]

# 写入Excel，第一列序号，第二列说明，第三列结果（与表2略有差异，但按要求填写）
# 表2为两列：说明和结果输出，这里直接写入
ws.append(["说明", "结果输出"])
for desc, val in results:
    ws.append([desc, val])

# 格式化数值保留两位小数（根据需要）
for row in ws.iter_rows(min_row=2, max_row=len(results)+1, min_col=2, max_col=2):
    for cell in row:
        if isinstance(cell.value, float):
            cell.number_format = '0.00'

wb.save("程序正确性.xlsx")
print("计算结果已写入 程序正确性.xlsx")

# ---------------------------- 可选：显示完成信息 ----------------------------
print("所有任务完成！生成文件：result1.txt, result2.txt, result3.txt, 程序正确性.xlsx")