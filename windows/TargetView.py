from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QMouseEvent, QWheelEvent, QImage, QPixmap, QPen
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem


class TargetView(QGraphicsView):
    def __init__(self, parent=None):
        super(TargetView, self).__init__()

        self.box_item_list = []
        self.last_point = None

        # self.image_item = QGraphicsPixmapItem()  # 创建像素图元

        self.scene = QGraphicsScene()  # 创建场景
        # self.scene.addItem(self.image_item)
        self.setScene(self.scene)  # 将场景添加至视图

        self.max_size = [0, 0]
        self.min_size = [400, 400]
        self.current_size = [1536, 1536]

    def wheelEvent(self, event: QWheelEvent) -> None:
        delta = event.angleDelta().y()
        if delta > 0 and self.current_size[0] < self.max_size[0] and self.current_size[1] < self.max_size[1]:
            self.scale(1.1, 1.1)
            self.current_size[0] = int(1.1 * self.current_size[0])
            self.current_size[1] = int(1.1 * self.current_size[1])
        if delta < 0 and self.current_size[0] > self.min_size[0] and self.current_size[1] > self.min_size[1]:
            self.scale(0.9, 0.9)
            self.current_size[0] = int(0.9 * self.current_size[0])
            self.current_size[1] = int(0.9 * self.current_size[1])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.last_point = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        dis_point = event.pos() - self.last_point
        self.last_point = event.pos()
        self.scene.setSceneRect(
            self.scene.sceneRect().x() - dis_point.x(), self.scene.sceneRect().y() - dis_point.y(),
            self.scene.sceneRect().width(), self.scene.sceneRect().height())
        self.scene.update()

    def set_image(self, image):
        image_item = QGraphicsPixmapItem()
        self.scene.addItem(image_item)

        show_image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(show_image)
        image_item.setPixmap(pix)
        self.max_size = [image.shape[1], image.shape[0]]

    def set_boxes(self, boxes):
        for box in boxes:
            box_item = QGraphicsRectItem()
            box_item.setPen(QPen(Qt.red, 4))
            box_item.setBrush(QBrush(Qt.NoBrush))
            box_item.setZValue(1)
            self.scene.addItem(box_item)
            box_item.hide()
            box_item.setRect(QRectF(box[0], box[1], box[2]-box[0], box[3]-box[1]))
            self.box_item_list.append(box_item)

    def show_boxes(self):
        for box_item in self.box_item_list:
            box_item.show()

    def focus_box(self, index):
        for i, box_item in enumerate(self.box_item_list):
            if i == index:
                box_item.setPen(QPen(Qt.yellow, 4))
            else:
                box_item.setPen(QPen(Qt.red, 4))

    def clear_target_view(self):
        self.box_item_list.clear()
        self.scene.clear()
