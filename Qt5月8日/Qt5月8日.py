# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
# from PyQt6.QtGui import QStandardItemModel, QStandardItem
# from PyQt6.QtCore import Qt
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("数据表格展示")
#         self.resize(700, 500)
#
#         # 创建表格视图和模型
#         self.table_view = QTableView()
#         self.model = QStandardItemModel()
#         self.table_view.setModel(self.model)
#
#         # 设置列标题
#         self.model.setHorizontalHeaderLabels(["序号", "X 坐标", "Y 坐标"])
#
#         # 读取文件并填充数据
#         self.load_data("压缩计算结果输出.txt")
#
#         # 自动调整列宽
#         self.table_view.resizeColumnsToContents()
#
#         # 布局
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)
#         layout.addWidget(self.table_view)
#
#     def load_data(self, filename):
#         """读取文本文件，将数据填入模型"""
#         try:
#             with open(filename, 'r', encoding='utf-8') as f:
#                 for line in f:
#                     line = line.strip()
#                     if not line:          # 跳过空行
#                         continue
#                     parts = line.split(',')
#                     if len(parts) != 3:
#                         continue          # 跳过格式错误行
#                     # 构造三个单元格项
#                     items = [
#                         QStandardItem(parts[0]),           # 序号（文本形式）
#                         QStandardItem(parts[1]),           # X坐标
#                         QStandardItem(parts[2])            # Y坐标
#                     ]
#                     # 可选：右对齐数字
#                     for item in items:
#                         item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
#                     self.model.appendRow(items)
#         except FileNotFoundError:
#             # 文件不存在时在表格显示提示
#             error_item = QStandardItem("错误：找不到文件 '压缩计算结果输出.txt'")
#             self.model.appendRow([error_item, QStandardItem(), QStandardItem()])
#         except Exception as e:
#             error_item = QStandardItem(f"读取错误：{str(e)}")
#             self.model.appendRow([error_item, QStandardItem(), QStandardItem()])
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

import sys
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget


class FileDataModel(QAbstractTableModel):
    """自定义模型：从文件读取数据并提供给表格视图"""

    def __init__(self, filename):
        super().__init__()
        self._data = []  # 存储二维数据 [[序号, X, Y], ...]
        self._headers = ["序号", "X 坐标", "Y 坐标"]
        self._load_file(filename)

    def _load_file(self, filename):
        """读取文件，填充 self._data"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(',')
                    if len(parts) == 3:
                        # 保持原始数据为字符串，也可转为数字
                        self._data.append([parts[0], parts[1], parts[2]])
        except FileNotFoundError:
            self._data = [["文件未找到", filename, "请检查路径"]]

    # 以下为必须重写的几个方法

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            # 返回对应行列的字符串表示
            print(f"row={index.row()}, col={index.column()}, value={self._data[index.row()][index.column()]}")
            return str(self._data[index.row()][index.column()])
        # 可选：设置文本右对齐（适合数字）
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        # 垂直表头显示行号（从1开始）
        return str(section+1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义模型展示数据")
        self.resize(700, 500)

        # 1. 创建模型，指定数据文件路径
        model = FileDataModel("压缩计算结果输出.txt")

        # 2. 创建表格视图，并设置模型
        table_view = QTableView()
        table_view.setModel(model)

        # 3. 可选：自动调整列宽
        # table_view.resizeColumnsToContents()

        # 布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(table_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
