import sys
from PyQt6.QtWidgets import QApplication
from ui import MyMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
