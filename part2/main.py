from fetcher import Opne_data
from config import path
from processor import Siq


if __name__ == '__main__':
    opne_path=Opne_data(path)
    data=opne_path.open()
    reulst=Siq(data,4310,3600)
    print(reulst)

