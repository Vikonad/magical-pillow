from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QImage, QPainter, QPen, QColor, QMouseEvent, QWheelEvent, QPainterPath
from PySide6.QtCore import Qt, QPointF

import sys
from datetime import datetime

from core import SignalBus

class ImageViewer(QWidget):
    def __init__(self, layers):
        super().__init__()
        self.bus = SignalBus()
        self.bus.pen_update.connect(self.on_pen_update)
        self.bus.show_tab.connect(self.on_show_drawing_tab)
        self.bus.hide_tab.connect(self.on_hide_drawing_tab)
        self.layers = layers
        self.pen = QPen(QColor(0,0,0,255), 10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.choosenlayer = 1
        self.setStyleSheet("background-color: white;")
        self.drawing_mode = False
        self.drawing = False
        self.eraser_mode = False
        self.last_point = None


        #zooming
        self.scale = 0.5
        self.offset = QPointF(0,0)

        #panning
        self.panning = False
        self.last_pan_point = None

        self.theline = []

    def on_pen_update(self, pen):
        self.pen = pen

    def on_show_drawing_tab(self, tab):
        if tab == "Drawing":
            self.drawing_mode = True
        #for i in self.theline:
            #    painter = QPainter(self.layers[self.choosenlayer])
            #    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            #    painter.setPen(self.pen)
            #    painter.drawLine(i[0][0], i[0][1], i[1][0], i[1][1])
            #    self.update()

    def on_hide_drawing_tab(self, tab):
        if tab == "Drawing":
            self.drawing_mode = False

    def update_choosenlayer(self, index):
        self.choosenlayer = index

    def update_pen(self, pen):
        self.pen = pen

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.offset)
        painter.scale(self.scale, self.scale)
        for layer in self.layers:
            painter.drawImage(0, 0, layer.image)

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
            painter = QPainter(self.layers[self.choosenlayer].image)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.setPen(self.pen)
            painter.drawLine(self.last_point, current_point)
            self.theline.append([[self.last_point.x(), self.last_point.y()],[current_point.x(),current_point.y()]])
            self.last_point = current_point
            self.update()
        elif self.eraser_mode and self.drawing_mode:
            current_point = self._screen_to_image(event.position())
            painter = QPainter(self.layers[self.choosenlayer].image)
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.setPen(self.pen)
            painter.drawLine(self.last_point, current_point)
            self.theline.append([[self.last_point.x(), self.last_point.y()],[current_point.x(),current_point.y()]])
            self.last_point = current_point
            self.update()
        elif self.panning:
            delta = event.position() - self.last_pan_point
            self.offset += delta
            self.last_pan_point = event.position()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        now = datetime.now()
        if event.button() == Qt.LeftButton:
            self.drawing = False
            if self.drawing_mode: self.bus.send_history.emit({
                "title":"draw",
                "parameters": {
                    "pen": self.pen,
                    "line": self.theline
                },
                "date": now.strftime("%H:%M"),
                "layer": self.layers[self.choosenlayer].name
            })
        if event.button() == Qt.RightButton:
            self.eraser_mode = False
            if self.drawing_mode: self.bus.send_history.emit({
                "title":"erase",
                "parameters": {
                    "pen": self.pen,
                    "line": self.theline
                },
                "date": now.strftime("%H:%M"),
                "layer": self.layers[self.choosenlayer].name
            })
        if event.button() == Qt.MiddleButton:
            self.panning = False
        self.theline = []

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
