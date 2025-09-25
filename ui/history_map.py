import sys
import math
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QBrush, QColor, QMouseEvent
from PySide6.QtCore import QPointF, Qt


class Circle:
    def __init__(self, center: QPointF, radius: float, color: QColor):
        self.center = center
        self.radius = radius
        self.color = color
        self.highlight = False

    def contains(self, point: QPointF) -> bool:
        dx = point.x() - self.center.x()
        dy = point.y() - self.center.y()
        return (dx * dx + dy * dy) <= (self.radius * self.radius)

    def move(self, dx: float, dy: float):
        self.center.setX(self.center.x() + dx)
        self.center.setY(self.center.y() + dy)


class CircleCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clickable Circles with Panning")
        self.setFixedSize(600, 400)

        self.circles = [
            Circle(QPointF(100, 100), 10, QColor("blue")),
            Circle(QPointF(100, 130), 10, QColor("blue")),
            Circle(QPointF(100, 160), 10, QColor("blue")),
            Circle(QPointF(100, 190), 10, QColor("blue")),
            Circle(QPointF(100, 220), 10, QColor("blue")),
            Circle(QPointF(100, 250), 10, QColor("blue")),
            Circle(QPointF(160, 160), 10, QColor("green")),
            Circle(QPointF(160, 190), 10, QColor("green")),
            Circle(QPointF(160, 220), 10, QColor("green")),
            Circle(QPointF(160, 250), 10, QColor("green")),
            Circle(QPointF(130, 220), 10, QColor("orange")),
            Circle(QPointF(130, 250), 10, QColor("orange")),
            Circle(QPointF(130, 280), 10, QColor("orange")),
            Circle(QPointF(130, 310), 10, QColor("orange")),
        ]

        self.dragging = False
        self.last_mouse_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("black"))
        painter.drawLine(100,160,160,160)
        painter.drawLine(100,100,100,250)
        painter.drawLine(130,220,130,310)
        painter.drawLine(160,160,160,250)
        painter.drawLine(100,220,130,220)
        for circle in self.circles:
            brush_color = QColor("yellow") if circle.highlight else circle.color
            painter.setBrush(QBrush(brush_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(circle.center, circle.radius, circle.radius)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.position()
            self.dragging = True

            clicked = False
            for circle in self.circles:
                if circle.contains(self.last_mouse_pos):
                    circle.highlight = True
                    clicked = True
                    print(f"Clicked circle at {circle.center}")
                else:
                    circle.highlight = False

            if clicked:
                self.dragging = False  # Prevent panning if clicking on a circle

            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging and self.last_mouse_pos is not None:
            current_pos = event.position()
            dx = current_pos.x() - self.last_mouse_pos.x()
            dy = current_pos.y() - self.last_mouse_pos.y()

            for circle in self.circles:
                circle.move(dx, dy)

            self.last_mouse_pos = current_pos
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.last_mouse_pos = None
