from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QImage, QPainter, QPen, QColor, QMouseEvent, QWheelEvent
from PySide6.QtCore import Qt, QPointF

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.layers = [QImage(300, 300, QImage.Format.Format_RGB32)]
        self.layers[0].fill(QColor("white"))
        self.pen = QPen(QColor(0,0,0,255), 10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.choosenlayer = 0
        #self.setStyleSheet("background-color: white;")
        self.drawing_mode = True
        self.drawing = False
        self.eraser_mode = False
        self.last_point = None

        #zooming
        self.scale = 0.5
        self.offset = QPointF(0,0)

        #panning
        self.panning = False
        self.last_pan_point = None

    def update_choosenlayer(self, index):
        self.choosenlayer = index

    def update_pen(self, pen):
        self.pen = pen

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.offset)
        painter.scale(self.scale, self.scale)
        for layer in self.layers:
            painter.drawImage(0, 0, layer)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton:
            self.panning = True
            self.eraser_mode = False
            self.last_pan_point = event.position()
        if event.button() == Qt.LeftButton:
            self.eraser_mode = False
            self.drawing = True
            self.last_point = self._screen_to_image(event.position())
        if event.button() == Qt.RightButton:
            self.eraser_mode = True
            self.drawing = False
            self.last_point = self._screen_to_image(event.position())

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing and self.drawing_mode:
            current_point = self._screen_to_image(event.position())
            painter = QPainter(self.layers[self.choosenlayer])
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.setPen(self.pen)
            painter.drawLine(self.last_point, current_point)
            self.last_point = current_point
            self.update()
        elif self.eraser_mode and self.drawing_mode:
            current_point = self._screen_to_image(event.position())
            painter = QPainter(self.layers[self.choosenlayer])
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.setPen(QPen(Qt.transparent, 10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.last_point, current_point)
            self.last_point = current_point
            self.update()
        elif self.panning:
            delta = event.position() - self.last_pan_point
            self.offset += delta
            self.last_pan_point = event.position()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drawing = False
        if event.button() == Qt.MiddleButton:
            self.panning = False

    def wheelEvent(self, event: QWheelEvent):
        old_mouse_img_pos = self._screen_to_image(event.position())
        delta = event.angleDelta().y()
        zoom_factor = 1.25 if delta > 0 else 0.8
        self.scale *= zoom_factor
        new_mouse_img_pos = self._screen_to_image(event.position())
        diff = new_mouse_img_pos - old_mouse_img_pos
        self.offset += diff * self.scale
        self.update()

    def _screen_to_image(self, pos):
        return (pos - self.offset) / self.scale
