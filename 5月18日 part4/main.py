import sys
from PyQt6.QtWidgets import QApplication
from ui import MyMainwin

if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MyMainwin()
    window.show()
    sys.exit(app.exec())