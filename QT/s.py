import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QStyle

class IconViewer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        icons = [attr for attr in dir(QStyle.StandardPixmap) if attr.startswith("SP_")]
        for i, name in enumerate(icons):
            btn = QPushButton(name)
            btn.setIcon(self.style().standardIcon(getattr(QStyle.StandardPixmap, name)))
            layout.addWidget(btn, i // 4, i % 4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = IconViewer()
    viewer.show()
    sys.exit(app.exec())