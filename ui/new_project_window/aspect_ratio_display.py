from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QColor, QFontMetrics
from PySide6.QtCore import Qt

class AspectRatioCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.aspect_ratio = 1 / 1
        self.aspect_ratio_text = "1:1"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        if w / h > self.aspect_ratio:
            rect_height = h * 0.8
            rect_width = rect_height * self.aspect_ratio
        else:
            rect_width = w * 0.8
            rect_height = rect_width / self.aspect_ratio

        x = (w - rect_width) / 2
        y = (h - rect_height) / 2

        metrics = QFontMetrics(QFont("Montserrat", 20, QFont.Weight.Bold))
        text_width = metrics.horizontalAdvance(self.aspect_ratio_text)
        center_x = (self.width() - text_width) // 2
        height_text = metrics.height()/2

        painter.setPen(QPen(QColor("blue"), 3))
        painter.setBrush(QBrush(QColor("lightblue")))
        painter.drawRect(int(x), int(y), int(rect_width), int(rect_height))
        painter.setPen(QPen(QColor("black"), 3))
        painter.setFont(QFont("Montserrat", 20, QFont.Weight.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.aspect_ratio_text)

    def change_aspect_ratio(self,aspect_ratio):
        self.aspect_ratio = int(aspect_ratio[0]) / int(aspect_ratio[1])
        self.aspect_ratio_text = f"{int(aspect_ratio[0])}:{int(aspect_ratio[1])}"
        self.update()
