from open import Open_dat
from data import SightInfo

if __name__ == '__main__':
    data=Open_dat()
    for i in data.list_data:
        print(i)
        # SightInfo(i[1][1],i[2][1],i[3][1],i[4][1],i[1][1],i[2][2],i[3][0])
