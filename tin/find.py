import os
import sys

# 遍历 sys.path，找到 site-packages
for p in sys.path:
    if 'site-packages' in p:
        # 常见可能的插件目录
        candidates = [
            os.path.join(p, 'PyQt5', 'Qt', 'plugins'),
            os.path.join(p, 'PyQt5', 'Qt5', 'plugins'),
            os.path.join(p, 'PyQt5', 'plugins'),
            os.path.join(p, 'PyQt5', 'Qt', 'plugins', 'platforms'),  # 直接检查 platforms
        ]
        for cand in candidates:
            if os.path.exists(cand):
                print("找到插件目录：", cand)
                # 再检查 platforms 子目录是否存在
                platforms_dir = os.path.join(cand, 'platforms')
                if os.path.exists(platforms_dir):
                    print("  并且 platforms 子目录存在，内容：", os.listdir(platforms_dir))
                break