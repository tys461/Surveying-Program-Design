import sys
from PyQt6.QtWidgets import QApplication
from ui import MyMianWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMianWindow()
    window.show()
    sys.exit(app.exec())
