import math

def Siq(data,Qx,Qy):
    Siq_dat = []
    for i in range(len(data)-1):
        siq=math.sqrt((float(data[i][1])-Qx)**2+(float(data[i][2])-Qy)**2)
        Siq_dat.append([data[i][0],siq,data[i][3]])
    Siq_dat.sort(key= lambda x:x[1] )
    Siq_dat=Siq_dat[0:5]
    Hq=sum([float(x[2])*1/x[1] for x in Siq_dat])/sum([1/x[1] for x in Siq_dat])
    return Hq,Siq_dat



