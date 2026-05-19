from prossces import Task1,Task2
import open_write


if __name__ =='__main__':
    l_result=[]
    task2=Task2('地形图图幅编号-2025/sheet.txt')
    for i in task2.data_frame:
        l_result.append(task2.cuont(int(i[0])-1))
    open_write.write_result('地形图图幅编号-2025/result.txt',l_result)
