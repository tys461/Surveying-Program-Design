import math


'''一'''
class point:
    def __init__(self,points):
        super().__init__()
        self.points=points
        self.cha_jin = {1 / 1000000: 6, 1 / 500000: 3, 1 / 250000: 1.5, 1 / 100000: 30 / 60,
                        1 / 50000: 15 / 60, 1 / 25000: 7 / 60 + 30 / 3600, 1 / 10000: 3 / 60 + 45 / 3600,
                        1 / 5000: 1 / 60 + 52.5 / 3600}
        self.cha_wei = {1 / 1000000: 4, 1 / 500000: 2, 1 / 250000: 1, 1 / 100000: 20 / 60,
                        1 / 50000: 10 / 60, 1 / 25000: 5 / 60, 1 / 10000: 2 / 60 + 30 / 3600,
                        1 / 5000: 1 / 60 + 15 / 3600}

        self.bi = {1/1000000:'A',1 / 500000: 'B', 1 / 250000: 'C', 1 / 100000: 'D'
                        , 1 / 50000: 'E', 1 / 25000: 'F', 1 / 10000: 'G', 1 / 5000: 'H'}

        self.result=[]
        self.txt=[]
    def __row_count(self,lat,lng):
        '''行编号'''
        self.row=int(lat/4)+1
        '''列编号'''
        self.col=int(lng/4)+31
        return [self.row,self.col]



    def __lie_hao(self,bi,lat,lng):
        # print(self.cha_jin.get(bi))
        self.hang=(4/self.cha_wei.get(bi))-int(math.fmod((lat/4),1)/self.cha_wei.get(bi))

        self.lie=int(math.fmod((lng/6),1)/self.cha_jin.get(bi)+1)
        return [int(self.hang),self.lie]

    def __ws_count(self,bi):
        self.lng_ws=(self.col-31)*6+(self.lie-1)*self.cha_jin.get(bi)
        self.lat_ws=(self.row-1)*4+((4/self.cha_wei.get(bi))-self.hang)*self.cha_wei.get(bi)
        return [self.lng_ws,self.lat_ws]


    def __min_max_wn(self,min_bi,max_bi):
        self.max_c_wn=(self.cha_wei.get(min_bi))/(self.cha_wei.get(max_bi))*(self.row-1)+1
        self.max_d_wn=(self.cha_jin.get(min_bi))/(self.cha_jin.get(max_bi))*(self.col-1)+1
        return [self.max_c_wn,self.max_d_wn]

    def __min_max_en(self,min_bi,max_bi):
        self.max_c_en = self.row*(self.cha_wei.get(min_bi)/self.cha_wei.get(max_bi))
        self.max_d_en = self.row*(self.cha_jin.get(min_bi)/self.cha_jin.get(max_bi))

        return[self.max_c_en,self.max_d_en]

    def coun_fen(self):
        '''第一题'''
        result = []
        for i in self.points:
            self.__row_count(i[2],i[1])
            self.__lie_hao(1/50000,i[2],i[1])
            if len(str(self.row)) < 3:
                if len(str(self.row)) < 2:
                    self.row = f"00{str(self.row)}"
                else:
                    self.row = f"0{str(self.row)}"
            if len(str(self.col)) < 3:
                if len(str(self.col)) < 2:
                    self.col = f"00{str(self.col)}"
                else:
                    self.col = f"0{str(self.col)}"
            a = f'{i[0]} {i[2]} {i[1]} {1/50000} {int(self.hang)}{self.lie}{self.bi.get(1/50000)}{self.row}{self.col}'
            result.append(a)
        self.txt.append(result)
        self.result.append(result)
        return result

    def coun_f(self):
        '''第二题'''
        result = []
        for i in self.points:
            if i[0]%5==0:
                self.__row_count(i[2], i[1])
                self.__lie_hao(1 /250000, i[2], i[1])
                if len(str(self.row)) < 3:
                    if len(str(self.row)) < 2:
                        self.row = f"00{str(self.row)}"
                    else:
                        self.row = f"0{str(self.row)}"
                if len(str(self.col)) < 3:
                    if len(str(self.col)) < 2:
                        self.col = f"00{str(self.col)}"
                    else:
                        self.col = f"0{str(self.col)}"
                a = f'{i[0]} {i[2]} {i[1]} {1 /250000} {int(self.hang)}{self.lie}{self.bi.get(1 / 50000)}{self.row}{self.col}'
                result.append(a)
        self.txt.append(result)
        self.result.append(result)
        return result

    def coun_n(self):
        '''第三题'''
        max_n=0
        idx=0
        for i in self.points:
            if i[2]>max_n:
                max_n=i[2]
                idx=self.points.index(i)
        self.__row_count(self.points[idx][2],self.points[idx][1])
        self.__lie_hao(1 / 5000, self.points[idx][2],self.points[idx][1])
        if len(str(self.row)) < 3:
            if len(str(self.row)) < 2:
                self.row = f"00{str(self.row)}"
            else:
                self.row = f"0{str(self.row)}"
        if len(str(self.col)) < 3:
            if len(str(self.col)) < 2:
                self.col = f"00{str(self.col)}"
            else:
                self.col = f"0{str(self.col)}"
        a = f'{self.points[idx][0]} {self.points[idx][2]} {self.points[idx][1]} {1 / 5000} {int(self.hang)}{self.lie}{self.bi.get(1 / 50000)}{self.row}{self.col}'
        self.txt.append(a)
        self.result.append(a)
        return a


    def coun_s(self):
        '''第四题'''
        max_n=100
        idx=0
        for i in self.points:
            if i[2]<max_n:
                max_n=i[2]
                idx=self.points.index(i)
        self.__row_count(self.points[idx][2],self.points[idx][1])
        self.__lie_hao(1 / 100000, self.points[idx][2],self.points[idx][1])
        if len(str(self.row)) < 3:
            if len(str(self.row)) < 2:
                self.row = f"00{str(self.row)}"
            else:
                self.row = f"0{str(self.row)}"
        if len(str(self.col)) < 3:
            if len(str(self.col)) < 2:
                self.col = f"00{str(self.col)}"
            else:
                self.col = f"0{str(self.col)}"
        a = f'{self.points[idx][0]} {self.points[idx][2]} {self.points[idx][1]} {1 / 100000} {int(self.hang)}{self.lie}{self.bi.get(1 / 50000)}{self.row}{self.col}'
        self.txt.append(a)
        self.result.append(a)
        return a


    def coun_e(self):
        '''第五题'''
        max_n=0
        idx=0
        for i in self.points:
            if i[1]>max_n:
                max_n=i[1]
                idx=self.points.index(i)
        self.__row_count(self.points[idx][2],self.points[idx][1])
        self.__lie_hao(1 / 250000, self.points[idx][2],self.points[idx][1])
        if len(str(self.row)) < 3:
            if len(str(self.row)) < 2:
                self.row = f"00{str(self.row)}"
            else:
                self.row = f"0{str(self.row)}"
        if len(str(self.col)) < 3:
            if len(str(self.col)) < 2:
                self.col = f"00{str(self.col)}"
            else:
                self.col = f"0{str(self.col)}"
        a = f'{self.points[idx][0]} {self.points[idx][2]} {self.points[idx][1]} {1 / 250000} {int(self.hang)}{self.lie}{self.bi.get(1 / 50000)}{self.row}{self.col}'
        self.txt.append(a)
        self.result.append(a)
        return a


    def coun_w(self):
        '''第六题'''
        max_n=1000
        idx=0
        for i in self.points:
            if i[1]<max_n:
                max_n=i[1]
                idx=self.points.index(i)
        self.__row_count(self.points[idx][2], self.points[idx][1])
        self.__lie_hao(1 / 250000, self.points[idx][2], self.points[idx][1])
        if len(str(self.row)) < 3:
            if len(str(self.row)) < 2:
                self.row = f"00{str(self.row)}"
            else:
                self.row = f"0{str(self.row)}"
        if len(str(self.col)) < 3:
            if len(str(self.col)) < 2:
                self.col = f"00{str(self.col)}"
            else:
                self.col = f"0{str(self.col)}"
        a = f'{self.points[idx][0]} {self.points[idx][2]} {self.points[idx][1]} {1 / 250000} {int(self.hang)}{self.lie}{self.bi.get(1 / 50000)}{self.row}{self.col}'
        self.txt.append(a)
        self.result.append(a)
        return a


    def coun_203(self):
        '''第七题'''
        result=[]
        for i in self.cha_jin:
            self.__row_count(self.points[202][2],self.points[202][1])
            self.__lie_hao(i,self.points[202][2],self.points[202][1])
            if len(str(self.row))<3:
                if len(str(self.row))<2:
                    self.row=f"00{str(self.row)}"
                else:
                    self.row = f"0{str(self.row)}"
            if len(str(self.col))<3:
                if len(str(self.col))<2:
                    self.col=f"00{str(self.col)}"
                else:
                    self.col = f"0{str(self.col)}"
            a=f'{203} {self.points[202][2]} {self.points[202][1]} {1 / 250000} {int(self.hang)}{self.lie}{self.bi.get(i)}{self.row}{self.col}'
            result.append(a)
        self.txt.append(result)
        self.result.append(result)

        return result

    def H43(self):
        a='H49C002003'





    def count(self):
        self.coun_fen()
        self.coun_f()
        self.coun_n()
        self.coun_s()
        self.coun_e()
        self.coun_w()
        self.coun_203()






#
def cuont(lis):
    li=point(lis)
    li.count()
    return li.result






