import math



def check_count1(I,J,dic_core,lis_input):
    up=0
    down=0
    for i in dic_core:
        c =  I- i[0] - 1
        r =  J- i[1] - 1
        if c < 0 or r < 0 or c > 9 or r > 9:
            up += 0
            down += 0
        else:
            num=lis_input[c][r]
            num=num*dic_core.get(i)
            up+=num
            down+=dic_core.get(i)
    if down==0:
        return "NaN"
    else:
        return f"{up / down:.3f}"


def check_count2(I,J,dic_core,lis_input):
    up=0
    down=0
    for i in dic_core:
        c =  I- i[0] - 1
        r =  J- i[1] - 1
        if c < 0 or r < 0 or c > 9 or r > 9:
            up += 0
            down += 0
        else:
            num=lis_input[9-c][9-r]
            num=num*dic_core.get(i)
            up+=num
            down+=dic_core.get(i)
    if down==0:
        return "NaN"
    else:
        return f"{up / down:.3f}"

def func1(lis_input,lis_core):
    lis_input=lis_input
    lis_core=lis_core
    result1=[]
    result2=[]
    dic_core={(row,colum):p for row,l in enumerate(lis_core) for colum,p in enumerate(l) }
    for I in range(len(lis_input)):
        result1.append([])
        for J in range(len(lis_input[I])):
            result1[-1].append(check_count1(I,J,dic_core,lis_input))

    for I in range(len(lis_input)):
        result2.append([])
        for J in range(len(lis_input[I])):
            result2[-1].append(check_count2(I,J,dic_core,lis_input))

    r='-----------1-----------\n'
    for i in result1:
        for l in i:
            r = r + f'{l} '
        r = r + '\n'

    r=r+'-----------2-----------\n'
    for i in result2:
        for l in i:
            r = r + f'{l} '
        r = r + '\n'

    return r
