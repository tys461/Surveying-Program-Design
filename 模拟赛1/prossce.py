class Count:
    def __init__(self,lis):
        self.point_lis=lis
        self.mean_filtering()
    def max_min_aver(self):
        ma=max([a for i in self.point_lis for a in i])
        mi=min([a for i in self.point_lis for a in i])
        avar=sum([a for i in self.point_lis for a in i])
        avar=avar/(len(self.point_lis)*len(self.point_lis[0]))

        return f"最大值:{ma}\n 最小值:{mi}\n 平均值:{avar}\n"
    def mean_filtering(self):
        lis = self.point_lis[0:]
        result = []
        r = ''
        for row in range(len(lis)):
            result.append([])
            for colum in range(len(lis[row])):
                a=0
                for idx_row in range(-1,2,1):
                    for idx_colum in range(-1,2,1):
                        if row+idx_row<0 or row+idx_row>19 or colum+idx_colum<0 or colum+idx_colum>19:
                            a+=0
                        else:
                            a=a+lis[row+idx_row][colum+idx_colum]
                r=r+f'{a/9:.3f},'
            r = r[:-1]
            r=r+'\n'
        return r


    def median_filtering(self):
        lis=self.point_lis[0:]
        r=''
        for row in range(len(lis)):
            for colum in range(len(lis[row])):
                lis_corw=[]
                for idx_row in range(-1, 2, 1):
                    for idx_colum in range(-1, 2, 1):
                        if row+idx_row<0 or row+idx_row>19 or colum+idx_colum<0 or colum+idx_colum>19:
                            lis_corw.append(0)
                        else:
                            lis_corw.append(lis[row+idx_row][colum+idx_colum])
                lis_corw.sort()
                print(lis_corw)
                count=lis_corw[4]
                r=r+f'{count},'
            r=r[:-1]
            r+='\n'
        return r

