import sys
from PyQt6.QtWidgets import QApplication
from ui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    sys.exit(app.exec())
