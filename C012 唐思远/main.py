from ui import MymainWindow
import sys
from PyQt6.QtWidgets import QApplication

if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MymainWindow()
    window.show()
    sys.exit(app.exec())