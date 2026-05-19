import re
import math
from open_write import open_Latitude_longitude,open_frame_number
from table import Table


class Task1:
    def __init__(self,file):
        self.data = open_Latitude_longitude(file)
    def degree_conversion(self,input_degree):
        degree=input_degree
        degree=abs(degree)
        Degree=int(degree)
        Degree_full=(degree-Degree)*60
        Degree_minute=int(Degree_full)
        seconds=(Degree_full-Degree_minute)*60
        return f"{Degree}°{Degree_minute}'{seconds:.2f}\""


    """计算图幅编号"""
    def drawing_number(self,B,L):
        a= (B // 4) + 1
        if a<=20 and a>0:
            a=chr(a+64)
        b=(L//6)+31
        return (a,b)

    """计算行列号"""
    def frame_number(self,B,L,bB,bL):
        c=int(4/bB-(B%4//bB))
        d=int((L%6)//bL+1)
        return(f'{c:04d}',f'{d:04d}')

    def conversion(self):
        for i in self.data:
            print(f"{i[0]} 纬度：{i[1]} "
                  f"经度：{i[2]}")
            print(f"{i[0]} 纬度：{self.degree_conversion(float(i[1]))} "
                  f"经度：{self.degree_conversion(float(i[2]))}")



class Task2 (Table):
    def __init__(self,file):
        super().__init__()
        self.data_frame = open_frame_number(file)


    """根据1∶100万地形图图幅行列号a、b，计算1：100万地形图图幅的西南图廓点经纬度："""
    def __trans_row_column(self,index):
        # print(f'index:{index}')
        self.a=ord(self.data_frame[index][1][0]) - 64
        self.b=int(self.data_frame[index][1][1:3])
        # print(self.a)
        self.B100=(self.a-1)*4
        self.L100=(self.b-31)*6

        return self.B100,self.L100

    """提取比例尺代码"""
    def __draw_scale(self,index):
        s=self.data_frame[index][1][3]
        self.scale=self._scale.get(s)

        return self.scale

    """根据其比例尺地形图在1∶100万地形图中的行列号c、d，计算西南图廓点经纬度 、 """
    def __cuont_B_L(self,index):
        self.b_B=self._Bbl.get(self.scale)[1]
        self.b_L=self._Bbl.get(self.scale)[0]

        if len(self.data_frame[index][1])==10:
            c=int(self.data_frame[index][1][4:7])
            d=int(self.data_frame[index][1][7:10])
        if len(self.data_frame[index][1])==12:
            c=int(self.data_frame[index][1][4:8])
            d=int(self.data_frame[index][1][8:12])

        if self.scale != None and self.B100 != None and self.L100 != None:
            self.B1=self.B100+self.b_B*(4%self.b_B-c)
            self.L1=self.L100+self.b_L*(d-1)

        return self.B1,self.L1

    """计算其它图廓点经纬度"""
    def __other_cuont(self):
        self.B3=self.B1+self.b_B
        self.L3=self.L1+self.b_L
        self.B2=self.B1
        self.L2=self.L1+self.b_L
        self.B4=self.B1+self.b_B
        self.L4=self.L2


    def cuont(self,index):
        self.__trans_row_column(index)
        self.__draw_scale(index)
        self.__cuont_B_L(index)
        self.__other_cuont()
        dict_data={1:(f'{self.L4:.5f}',f'{self.B4:.5f}'),2:(f'{self.L2:.5f}',f'{self.B2:.5f}'),
                   3:(f'{self.L3:.5f}',f'{self.B3:.5f}'),4:(f'{self.L1:.5f}',f'{self.B1:.5f}')}

        return dict_data
