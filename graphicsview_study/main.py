import sys
from PyQt6.QtWidgets import QApplication,QWidget,QGraphicsView,QGraphicsScene
from PyQt6.QtGui import QPen,QBrush,QColor
from window import Ui_Form
from PyQt6.QtCore import QRectF,QPointF



class Graphics(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.ui=self.setupUi(self)
        self.point=((1,1),(1.841071976,-1.724307355),(3.96379461,-4.037030357),(7.152611963,-5.227522169)
                    ,(10.7240874,-3.824442533),(12.72241294,-1.273388651),(13.06255346,2.553192172),
                    (15.99626542,5.486904137),(19.73781112,7.527747243),(17.2292748,11.18425781),
                    (13.19010615,10.88663485),(8.938349681,10.16383625),(3.538618963,8.122993149),
                    (1.242670469,4.423965019))

        self.scene=QGraphicsScene(self)
        self.scene.setSceneRect(-500,-500,5000,5000)
        self.graphicsView.setScene(self.scene)
        self.drawShpas()

    # def drawShpas(self):
    #     se=[]
    #     # self.scene.addRect(0,0,20,20,QPen(QColor(255,0,0)),QBrush(QColor(255,255,0)))
    #     # for i in range(len(self.point)):
    #     #     se.append(QPointF(i[0],i[0]))
    #
    #     for i in range(len(self.point)):
    #         if i==len(self.point)-1:
    #             pass
    #         else:
    #             self.scene.addLine(*self.point[i],*self.point[i+1], QPen(QColor(255, 0, 0)))
    #     # self.scene.addLine(0,0,5,80,QPen(QColor(255,0,0)))
    def transform_y(self, y):
        return -y
    def drawShpas(self):
        scale = 20  # 放大倍数，可根据需要调整

        # 1. 缩放并翻转 y 坐标（y 轴向上为正）
        xs = [x * scale for x, _ in self.point]
        ys = [-y * scale for _, y in self.point]  # 直接用 -y 实现 y 轴翻转

        # 2. 平移使最小坐标为 (0,0)
        min_x, min_y = min(xs), min(ys)
        shifted_points = [(x - min_x, y - min_y) for x, y in zip(xs, ys)]

        # 3. 设置场景矩形（刚好容纳所有点）
        max_x = max(x - min_x for x, _ in shifted_points)
        max_y = max(y - min_y for _, y in shifted_points)
        self.scene.setSceneRect(0, 0, max_x, max_y)  # 左下角为 (0,0)

        # 4. 绘制连线
        for i in range(len(shifted_points) - 1):
            x1, y1 = shifted_points[i]
            x2, y2 = shifted_points[i + 1]
            self.scene.addLine(x1, y1, x2, y2, QPen(QColor(255, 0, 0), 2))
if __name__=='__main__':
    app=QApplication(sys.argv)
    mywindow=Graphics()
    w=mywindow.show()
    sys.exit(app.exec())