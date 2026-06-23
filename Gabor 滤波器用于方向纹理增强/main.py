import math

size = 31
img = [[0]*size for _ in range(size)]
for i in range(size):
    for j in range(size):
        # 水平条纹：在 0~15 行
        if i < 16:
            img[i][j] = 255 if (i // 4) % 2 == 0 else 0
        else:
            # 45° 条纹
            img[i][j] = 255 if ((i+j) // 4) % 2 == 0 else 0


def generation_Gabor(size,degreed):
    half = size // 2
    rad=math.radians(degreed)
    namta=8.0
    sata=namta/math.pi
    gama=0.5

    result=[]
    for row in range(-half,half+1,1):
        result.append([])
        for col in range(-half,half+1,1):
            x=col*math.cos(rad)+row*math.sin(rad)
            y=-col*math.sin(rad)+row*math.cos(rad)

            gabor=math.exp(-(x**2+(gama**2)*(y**2))/(2*(sata**2)))*math.cos(2*math.pi*(x/namta))
            result[-1].append(float(f'{gabor:.2f}'))
    return  result

for i in generation_Gabor(15,45):
    print(i)
